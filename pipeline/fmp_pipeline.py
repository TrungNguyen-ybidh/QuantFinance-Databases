from fetchers.fetcher import FMPFetcher
from cleaners.cleaner import Cleaner, FMPCleaner
from config.config import engine, ROOT
from config.fmp_config import fmp_update_endpoints, schema_map
from updater import update_daily_data, companies_info_update
import pandas as pd
import os
import glob
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


def update_pipeline(file_path):
    # --- Setup ---
    symbols = pd.read_sql("SELECT ticker FROM companies", con=engine)["ticker"].tolist()
    load_dotenv()
    api = os.getenv("FMP_api")

    fmp = FMPFetcher(symbols, api)
    fmp_clean = FMPCleaner(root=file_path)
    clean = Cleaner(root=file_path)


    # --- Fetch data from FMP API ---
    fmp.fetch_all(file_path=file_path, endpoint_config=fmp_update_endpoints)
    # --- Clean and rename columns ---
    fmp_clean.keep_and_rename(schema_map=schema_map, input_file=file_path)

    # --- Load each cleaned file into its matching table ---
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

            if not new_data.empty:
                clean.insert_to_sql(table=table, df=new_data)
                print(f"Inserted {len(new_data)} rows into {table}")
            else:
                print(f"No new data for {table}")

        except Exception as e:
            print(f"Failed on {filename}: {e}")
            continue

    # --- Clean up temp files ---
    clean.clean_dir()

    # --- Update daily prices ---
    update_daily_data(symbols, file_path=file_path)

    # --- Clean up temp files ---
    clean.clean_dir()


if __name__ == "__main__":
    update_pipeline(file_path=f"{ROOT}/data/update")