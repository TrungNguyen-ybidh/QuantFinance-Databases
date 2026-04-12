from config import engine, ROOT
import pandas as pd
import os
from dotenv import load_dotenv
from fetchers import Fetcher, FMPFetcher
from cleaners import Cleaner, FMPCleaner

def companies_info_update(symbols, api):
    file_path = f"{ROOT}/data/update"
    cleaner = Cleaner(root = file_path)
    fmp_cleaner = FMPCleaner(root=file_path)
    fetch_fmp = FMPFetcher(symbols=symbols, api_key=api)

    schema_map = {
        "profile.csv": {
        "primary_key": ["symbol"],
        "keep": [
            "symbol", "companyName", "price", "marketCap", "beta",
            "sector", "industry", "country", "cik", "isin", "cusip",
            "exchange", "ceo", "fullTimeEmployees", "ipoDate", "description"
        ],
        "rename": {
            "symbol": "ticker",
            "companyName": "company_name",
            "price": "price",
            "marketCap": "market_cap",
            "beta": "beta",
            "sector": "sector",
            "industry": "industry",
            "country": "country",
            "cik": "cik",
            "isin": "isin",
            "cusip": "cusip",
            "exchange": "exchange",
            "ceo": "ceo",
            "fullTimeEmployees": "full_time_employees",
            "ipoDate": "ipo_date",
            "description": "description"
        },
        "drop": [
            "lastDividend", "range", "change", "changePercentage",
            "volume", "averageVolume", "currency", "exchangeFullName",
            "website", "phone", "address", "city", "state", "zip",
            "image", "defaultImage", "isEtf", "isActivelyTrading",
            "isAdr", "isFund"
        ]
    }}
    
    endpoint = [{
        "endpoint": "profile",
        "params": {}
    }]

    fetch_fmp.fetch_all(file_path=file_path, endpoint_config=endpoint)
    fmp_cleaner.keep_and_rename(schema_map=schema_map)
    cleaner.insert_to_sql(table="companies", replace=False, file='profile.csv')





    


