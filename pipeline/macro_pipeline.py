"""Fetch FRED macro series and refresh macro_daily/monthly/quarterly tables."""
import os
import pandas as pd
from dotenv import load_dotenv

from fetchers import FREDFetcher
from cleaners import Cleaner
from config import engine, ROOT


DAILY_SERIES = {
    "T10YIE": "inflation_exp",
    "TEDRATE": "ted_spread",
    "DFF": "interest_rate",
    "T10Y2Y": "yield_curve",
    "DCOILWTICO": "wti",
}

MONTHLY_SERIES = {
    "MANEMP": "pmi",
    "SAHMREALTIME": "sahm_rule",
    "USREC": "recession",
    "RETAILSMNSA": "retail_sales",
    "CPILFESL": "core_cpi",
    "UNRATE": "unrate",
    "FEDFUNDS": "fedfunds",
    "CPIAUCSL": "headline_cpi",
    "UMCSENT": "consumer_sentiment",
    "INDPRO": "industrial_production",
    "M2SL": "m2",
    "PCEPI": "pce",
}

QUARTERLY_NATIVE = {
    "GDPPOT": "potential_gdp",
    "GDP": "nominal_gdp",
    "GDPC1": "real_gdp",
}

# Series re-sampled into the quarterly table from monthly/daily sources.
MONTHLY_TO_QUARTERLY = {
    "UNRATE": "unrate",
    "SAHMREALTIME": "sahm_rule",
    "USREC": "recession",
    "CPIAUCSL": "headline_cpi",
    "CPILFESL": "core_cpi",
    "PCEPI": "pce",
    "M2SL": "m2",
    "FEDFUNDS": "fedfunds",
}

DAILY_TO_QUARTERLY = {
    "T10Y2Y": "yield_curve",
    "BAMLH0A0HYM2": "hy_spread",
    "DCOILWTICO": "wti",
}

QUARTERLY_COLUMNS = [
    "date", "potential_gdp", "nominal_gdp", "real_gdp",
    "fedfunds", "yield_curve", "hy_spread", "wti",
    "unrate", "sahm_rule", "recession",
    "headline_cpi", "core_cpi", "pce", "m2",
]


def _fred():
    load_dotenv()
    return FREDFetcher(api_key=os.getenv("FRED_api"), root=ROOT)


def build_macro_daily():
    df = _fred().fetch(DAILY_SERIES)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def build_macro_monthly(start_year=1990):
    df = _fred().fetch(MONTHLY_SERIES)
    df["date"] = pd.to_datetime(df["date"])
    if start_year is not None:
        df = df[df["date"].dt.year >= start_year]
    return df.sort_values("date").reset_index(drop=True)


def _resample_quarterly(series_map):
    df = _fred().fetch(series_map)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date").resample("QE").first().reset_index()


def build_macro_quarterly():
    native = _fred().fetch(QUARTERLY_NATIVE)
    native["date"] = pd.to_datetime(native["date"])
    monthly = _resample_quarterly(MONTHLY_TO_QUARTERLY)
    daily = _resample_quarterly(DAILY_TO_QUARTERLY)

    for d in (native, monthly, daily):
        d["year"] = d["date"].dt.year
        d["quarter"] = d["date"].dt.quarter

    merged = native.merge(daily, on=["year", "quarter"], how="outer", suffixes=("", "_d"))
    merged = merged.merge(monthly, on=["year", "quarter"], how="outer", suffixes=("", "_m"))
    merged = merged.drop(columns=[c for c in merged.columns if c.startswith("date_")])

    # drop rows where most columns are missing (legacy heuristic from notebook)
    nulls_per_row = merged.set_index("date").isnull().sum(axis=1)
    bad_years = set(nulls_per_row[nulls_per_row >= 13].index.year[:-2])
    merged = merged[~merged["date"].dt.year.isin(bad_years)]

    return merged[QUARTERLY_COLUMNS].reset_index(drop=True)


def update_macro_tables():
    """Refresh macro_daily, macro_monthly, macro_quarterly from FRED."""
    cleaner = Cleaner(root=ROOT)
    daily = build_macro_daily()
    monthly = build_macro_monthly()
    quarterly = build_macro_quarterly()

    cleaner.insert_to_sql(table="macro_daily", df=daily)
    cleaner.insert_to_sql(table="macro_monthly", df=monthly)
    cleaner.insert_to_sql(table="macro_quarterly", df=quarterly)
    print(f"macro_daily: {len(daily)} rows | macro_monthly: {len(monthly)} | macro_quarterly: {len(quarterly)}")


if __name__ == "__main__":
    update_macro_tables()
