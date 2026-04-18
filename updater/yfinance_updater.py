from datetime import timedelta
from config import timer, engine
import pandas as pd 
from fetchers import YFinanceFetcher
from cleaners import Cleaner
from datetime import datetime

@timer
def update_daily_data(symbols_lst, file_path, chunk_size=500):
    table = 'daily_prices'
    today = datetime.today().strftime('%Y-%m-%d')

    placeholders = ','.join(['%s'] * len(symbols_lst))
    max_dates = pd.read_sql(
        f"SELECT ticker, MAX(date) as max_date FROM daily_prices WHERE ticker IN ({placeholders}) GROUP BY ticker",
        con=engine,
        params=tuple(symbols_lst)
    )

    date_map = dict(zip(max_dates['ticker'], max_dates['max_date']))

    stale = []
    for sym in symbols_lst:
        if sym not in date_map:
            stale.append(sym)
        else:
            next_day = (pd.to_datetime(date_map[sym]) + timedelta(days=1)).strftime('%Y-%m-%d')
            if next_day <= today:
                stale.append(sym)

    if not stale:
        print("Already up to date.")
        return

    # use the earliest stale date as start, let insert_to_sql handle duplicates
    stale_dates = [pd.to_datetime(date_map[s]) for s in stale if s in date_map]
    if stale_dates:
        start = min(stale_dates).strftime('%Y-%m-%d')
    else:
        start = None  # new tickers with no data, fetch all

    print(f"Updating {len(stale)} stale tickers from {start}")

    fetcher = YFinanceFetcher(
        symbols=stale,
        root=file_path,
        chunk_size=chunk_size
    )
    df = fetcher.fetch(start_date=start)

    if df.empty:
        print("No new data to insert.")
        return

    return df