from fetchers.fetcher import FMPFetcher
from cleaners.cleaner import Cleaner, FMPCleaner
from config.config import engine, ROOT
from config.fmp_config import fmp_update_endpoints, schema_map
from updater import update_daily_data
import pandas as pd
import os
import glob
import tempfile
import shutil
from dotenv import load_dotenv

FILE_TO_TABLE = {
    "enterprise-values.csv": "ev",
    "cash-flow-statement.csv": "cashflow",
    "income-statement-growth.csv": "income_stmt_growth",
    "key-metrics.csv": "metrics",
    "cash-flow-statement-growth.csv": "cashflow_growth",
    "balance-sheet-statement.csv": "balance_sheet",
    "income-statement.csv": "income_stmt",
    "levered-discounted-cash-flow.csv": "dcf_levered",
    "balance-sheet-statement-growth.csv": "balance_sheet_growth",
    "financial-growth.csv": "growth",
    "discounted-cash-flow.csv": "dcf",
    "dividends.csv": "dividends",
    "analyst-estimates.csv": "estimates",
}


def verify_inserts(table, fetched_df, before_count, conflict_cols=("ticker", "date")):
    """Confirm fetched (ticker, date) pairs are present in the table after insert.
    Returns (inserted_count, missing_count)."""
    pairs = fetched_df[list(conflict_cols)].drop_duplicates()
    if "date" in pairs.columns:
        pairs["date"] = pd.to_datetime(pairs["date"]).dt.strftime("%Y-%m-%d")

    tickers = tuple(pairs["ticker"].unique().tolist())
    if not tickers:
        return 0, 0

    where = "ticker IN %(tickers)s"
    params = {"tickers": tickers}
    if "date" in pairs.columns:
        where += " AND date >= %(min_date)s"
        params["min_date"] = pairs["date"].min()

    cols = ", ".join(conflict_cols)
    db_rows = pd.read_sql(
        f"SELECT {cols} FROM {table} WHERE {where}", con=engine, params=params
    )
    if "date" in db_rows.columns:
        db_rows["date"] = pd.to_datetime(db_rows["date"]).dt.strftime("%Y-%m-%d")

    db_set = set(map(tuple, db_rows[list(conflict_cols)].values))
    fetched_set = set(map(tuple, pairs[list(conflict_cols)].values))
    inserted = fetched_set & db_set
    missing = fetched_set - db_set

    after_count = pd.read_sql(
        f"SELECT COUNT(*) AS n FROM {table}", con=engine
    )["n"].iloc[0]

    print(f"[{table}] row delta: +{after_count - before_count} | "
          f"fetched {len(fetched_set)} pairs — "
          f"{len(inserted)} in DB, {len(missing)} missing")
    return len(inserted), len(missing)


def update_fmp_tables(symbols, file_path):
    """Fetch FMP endpoints and append only rows with date > MAX(date) per ticker."""
    load_dotenv()
    api = os.getenv("FMP_api")

    fmp = FMPFetcher(symbols, api)
    fmp_clean = FMPCleaner(root=file_path)
    clean = Cleaner(root=file_path)

    fmp.fetch_all(file_path=file_path, endpoint_config=fmp_update_endpoints)
    fmp_clean.keep_and_rename(schema_map=schema_map, input_file=file_path)

    files = glob.glob(f"{file_path}/cleaned/*.csv")

    for file in files:
        filename = os.path.basename(file)
        if filename not in FILE_TO_TABLE:
            print(f"Skipping {filename} — no table mapping found")
            continue

        table = FILE_TO_TABLE[filename]

        try:
            df = pd.read_csv(file)
            existing = pd.read_sql(
                f"SELECT ticker, MAX(date) as max_date FROM {table} GROUP BY ticker",
                con=engine,
            )
            merged = df.merge(existing, on="ticker", how="left")
            merged["date"] = pd.to_datetime(merged["date"])
            merged["max_date"] = pd.to_datetime(merged["max_date"])
            new_data = merged[
                (merged["max_date"].isna()) | (merged["date"] > merged["max_date"])
            ].drop(columns=["max_date"])

            if new_data.empty:
                print(f"No new data for {table}")
                continue

            before = pd.read_sql(
                f"SELECT COUNT(*) AS n FROM {table}", con=engine
            )["n"].iloc[0]

            clean.insert_to_sql(table=table, df=new_data)
            verify_inserts(table, new_data, before)

        except Exception as e:
            print(f"Failed on {filename}: {e}")
            continue


def update_daily_prices(symbols, file_path):
    """Pull yfinance daily prices from min(MAX(date)) across tickers,
    INSERT IGNORE into daily_prices, then verify against the DB."""
    before = pd.read_sql(
        "SELECT COUNT(*) AS n FROM daily_prices", con=engine
    )["n"].iloc[0]

    df = update_daily_data(symbols, file_path=file_path)
    if df is None or df.empty:
        print("No new daily price data to insert.")
        return

    df.columns = [c.lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "ticker"])

    Cleaner(root=file_path).insert_to_sql(table="daily_prices", df=df)
    verify_inserts("daily_prices", df, before)


def update_pipeline(run_fmp=False, run_daily=True):
    """Run the configured update steps inside a temp working dir.

    For now `update_pipeline()` only refreshes daily_prices. Flip
    `run_fmp=True` once that path is verified to also refresh FMP tables.
    """
    symbols = pd.read_sql("SELECT ticker FROM companies", con=engine)["ticker"].tolist()
    print(f"Loaded {len(symbols)} tickers from companies table")

    os.makedirs(f"{ROOT}/data", exist_ok=True)
    tmp_dir = tempfile.mkdtemp(prefix="pipeline_", dir=f"{ROOT}/data")
    print(f"Created temp dir: {tmp_dir}")

    try:
        if run_fmp:
            update_fmp_tables(symbols, file_path=tmp_dir)
        if run_daily:
            update_daily_prices(symbols, file_path=tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print(f"Removed temp dir: {tmp_dir}")


if __name__ == "__main__":
    update_pipeline(run_fmp=False, run_daily=True)
