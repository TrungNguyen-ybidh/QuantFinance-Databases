"""Fetch sector-ETF prices via yfinance and refresh sector_returns_* tables.

Sector tickers below are the SPDR Select Sector ETFs (the standard set used to
proxy GICS sectors). Adjust the mapping if a different ETF universe is desired.
"""
import yfinance as yf
import pandas as pd

from cleaners import Cleaner
from config import engine, ROOT


SECTOR_TICKERS = {
    "XLU": "utilities",
    "XLP": "consumer_staples",
    "XLF": "financials",
    "XLC": "communication_services",
    "XLK": "technology",
    "XLB": "materials",
    "XLE": "energy",
    "XLRE": "real_estate",
    "XLY": "consumer_discretionary",
    "XLI": "industrials",
    "XLV": "healthcare",
}


def _daily_pct_change(tickers, start=None, end=None):
    """Download daily closes for `tickers` and return a (date, name1, name2, ...)
    DataFrame of percent-change returns."""
    raw = yf.download(list(tickers), start=start, end=end, progress=False, auto_adjust=True)
    closes = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]]
    closes = closes.sort_index()
    rets = closes.pct_change().mul(100).round(3)
    rets.columns = [tickers[t] for t in rets.columns]
    return rets.reset_index().rename(columns={"Date": "date"})


def build_sector_returns(start=None, end=None):
    daily = _daily_pct_change(SECTOR_TICKERS, start=start, end=end)
    monthly = daily.set_index("date").resample("ME").first().reset_index()
    quarterly = daily.set_index("date").resample("QE").first().reset_index()
    return daily, monthly, quarterly


def update_sector_tables(start=None, end=None):
    cleaner = Cleaner(root=ROOT)
    daily, monthly, quarterly = build_sector_returns(start=start, end=end)
    cleaner.insert_to_sql(table="sector_returns_daily", df=daily)
    cleaner.insert_to_sql(table="sector_returns_monthly", df=monthly)
    cleaner.insert_to_sql(table="sector_returns_quarterly", df=quarterly)
    print(f"sector_returns: daily={len(daily)} monthly={len(monthly)} quarterly={len(quarterly)}")


if __name__ == "__main__":
    update_sector_tables()
