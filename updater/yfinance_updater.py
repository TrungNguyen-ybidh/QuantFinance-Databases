from datetime import timedelta
from config import timer, engine
import pandas as pd 
from fetchers import YFinanceFetcher
from cleaners import Cleaner

@timer
def update_daily_data(symbols_lst, file_path):
    table = 'daily_prices'

    date = pd.read_sql(
        'SELECT MAX(date) as date FROM daily_prices',
        con=engine
    )['date'].iloc[0]

    next_day = (pd.to_datetime(date) + timedelta(days=1)).strftime('%Y-%m-%d')

    fetcher = YFinanceFetcher(
        symbols=symbols_lst,
        root=file_path,
        chunk_size=500
    )
    df = fetcher.fetch(start_date=next_day)

    if df.empty:
        print("No new data to insert.")
        return

    clean = Cleaner(root=file_path)
    clean.insert_to_sql(table=table, df=df)