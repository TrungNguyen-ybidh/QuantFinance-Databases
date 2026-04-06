from fetchers.fetcher import FMPFetcher
from cleaners.cleaner import Cleaner, FMPCleaner
from config.config import engine
from config.fmp_endpoint import fmp_update_endpoints
from config.schema_config import schema_map
import pandas as pd 
import os 
from dotenv import load_dotenv
import glob


def fmp_pipeline(file_path, fetch_all=True):
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
    # --- Setup ---
    symbols = pd.read_sql('SELECT ticker FROM companies', con=engine)['ticker'].tolist()
    load_dotenv()
    api = os.getenv('FMP_api')

    fmp = FMPFetcher(symbols, api)
    fmp_clean = FMPCleaner(root=file_path)
    clean = Cleaner(root=file_path)

    # --- Fetch data from FMP API ---
    if fetch_all:
        fmp.fetch_all(file_path=file_path, endpoint_config=fmp_update_endpoints)
    else:
        fmp.fetch_endpoints(enpoint_lst=fmp_update_endpoints, file_path=file_path)

    # --- Clean and rename columns ---
    fmp_clean.keep_and_rename(schema_map=schema_map, input_file=file_path)

    # --- Load each cleaned file into its matching table ---
    files = glob.glob(f"{file_path}/cleaned/*.csv")

    for file in files:
        filename = os.path.basename(file)

        # Skip files that don't have a table mapping
        if filename not in FILE_TO_TABLE:
            print(f"Skipping {filename} — no table mapping found")
            continue

        table = FILE_TO_TABLE[filename]

        # Read and clean
        df = pd.read_csv(file)
        clean.data_cleaning(df, existent=False)

        # Get the latest date per ticker already in the table
        existing = pd.read_sql(f'''
            SELECT ticker, MAX(date) as max_date
            FROM {table}
            GROUP BY ticker
        ''', con=engine)

        # Keep only rows that are new
        merged = df.merge(existing, on='ticker', how='left')
        new_data = merged[
            (merged['max_date'].isna()) | (merged['date'] > merged['max_date'])
        ]
        new_data = new_data.drop(columns=['max_date'])

        # Insert
        if not new_data.empty:
            clean.insert_to_sql(table=table, df=new_data)
            print(f"Inserted {len(new_data)} rows into {table}")
        else:
            print(f"No new data for {table}")