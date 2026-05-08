"""Fetch asset-class ETF prices via yfinance and refresh asset_class_returns_* tables."""
import pandas as pd
import yfinance as yf

from cleaners import Cleaner
from config import engine, ROOT


ASSET_TICKERS = {
    "BTC-USD": "bitcoin",
    "VNQ": "real_estate",
    "AGG": "us_agg_bonds",
    "IWF": "large_cap_growth",
    "IWD": "large_cap_value",
    "IWM": "small_cap",
    "TLT": "long_term_treasury",
    "RSP": "equal_weight_sp500",
    "EEM": "emerging_markets",
    "SHY": "short_term_treasury",
    "EFA": "intl_developed",
    "GLD": "gold",
    "USO": "oil",
    "SPY": "us_large_cap",
    "HYG": "high_yield_bonds",
}


def _daily_pct_change(tickers, start=None, end=None):
    raw = yf.download(list(tickers), start=start, end=end, progress=False, auto_adjust=True)
    closes = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]]
    closes = closes.sort_index()
    rets = closes.pct_change().mul(100).round(3)
    rets.columns = [tickers[t] for t in rets.columns]
    return rets.reset_index().rename(columns={"Date": "date"})


def build_asset_class_returns(start=None, end=None):
    daily = _daily_pct_change(ASSET_TICKERS, start=start, end=end)
    monthly = daily.set_index("date").resample("ME").first().reset_index()
    quarterly = daily.set_index("date").resample("QE").first().reset_index()
    return daily, monthly, quarterly


def update_asset_class_tables(start=None, end=None):
    cleaner = Cleaner(root=ROOT)
    daily, monthly, quarterly = build_asset_class_returns(start=start, end=end)
    cleaner.insert_to_sql(table="asset_class_returns_daily", df=daily)
    cleaner.insert_to_sql(table="asset_class_returns_monthly", df=monthly)
    cleaner.insert_to_sql(table="asset_class_returns_quarterly", df=quarterly)
    print(f"asset_class_returns: daily={len(daily)} monthly={len(monthly)} quarterly={len(quarterly)}")


if __name__ == "__main__":
    update_asset_class_tables()
