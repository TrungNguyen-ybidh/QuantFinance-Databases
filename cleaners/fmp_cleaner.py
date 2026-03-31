import ast
import pandas as pd
from config.config import ROOT, engine
from fetchers.fetcher import Fetcher 
from sqlalchemy import text


def parse_dict_col(file_path, col=None, col_lst=None):
    fetcher = Fetcher()
    df = pd.read_csv(file_path, low_memory=False)
    if col is None and col_lst is not None:
        for col in col_lst:
            try: 
                expanded = pd.json_normalize(df[col])
                df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
            except Exception as e:
                    df[col] = df[col].apply(ast.literal_eval)
                    expanded = pd.json_normalize(df[col])
                    df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
        fetcher.save_csv(df, file_path=file_path)
        return df
    if col is not None and col_lst is None:
         try: 
            expanded = pd.json_normalize(df[col])
            df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
            return df
         except Exception as e:
            df[col] = df[col].apply(ast.literal_eval)
            expanded = pd.json_normalize(df[col])
            df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
            fetcher.save_csv(df, file_path=file_path)
            return df

def keep_and_rename(schema_map, input_file = ROOT, output_file = ROOT, action=None):
    result = {}
    fetcher = Fetcher()
    if action is None:
        for key, value in schema_map.items():
            try:
                df = pd.read_csv(f"{input_file}/{key}", low_memory=False)
                df = df[value["keep"]]
                df = df.rename(columns=schema_map[key]['rename'])
                fetcher.save_csv(df, file_path=f"{output_file}/{key}")
                result[key] = df
            except Exception as e:
                 print(f"{key} — {e}")
        return result
    elif action == 'rename':
        for key, value in schema_map.items():
            try:
                df = pd.read_csv(f"{input_file}/{key}", low_memory=False)
                df = df.rename(columns=schema_map[key][action])
                fetcher.save_csv(df, file_path=f"{output_file}/{key}")
                result[key] = df
            except Exception as e:
                print(f"{key} - {e}")
        return result
    elif action == 'drop':
        for key, value in schema_map.items():
            try:
                df = pd.read_csv(f"{input_file}/{key}", low_memory=False)
                df = df.drop(columns=schema_map[key][action])
                fetcher.save_csv(df, file_path=f"{output_file}/{key}")
                result[key] = df
            except Exception as e:
                print(f"{key} - {e}")
        return result
    elif action == 'keep':
        for key, value in schema_map.items():
            try:
                df = pd.read_csv(f"{input_file}/{key}", low_memory=False)
                df = df[value[action]]
                fetcher.save_csv(df, file_path=f"{output_file}/{key}")
                result[key] = df
            except Exception as e:
                print(f"{key} - {e}")
        return result
    
def data_cleaning(df):
    existing = pd.read_sql("SELECT ticker FROM companies", engine)
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    df_clean = df[df['ticker'].isin(existing['ticker'])].copy()
    
    for col in date_cols:
        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
    
    if 'period' in df.columns and 'date' in df.columns:
        df_clean = df_clean.drop_duplicates(subset=['ticker', 'date', 'period'], keep='first')
    elif 'date' in df.columns:
        df_clean = df_clean.drop_duplicates(subset=['ticker', 'date'], keep='first')
    else:
        df_clean = df_clean.drop_duplicates()
    
    return df_clean

def insert_to_sql(table, file=None, df=None):
    if df is None and file is not None:
        df = pd.read_csv(f"{ROOT}/data/cleanned/{file}")
        print(f"{file}: {list(df.columns)}")
        df_clean = data_cleaning(df)
    elif df is None and file is not None:
        print(f"{file}: {list(df.columns)}")
        df_clean = data_cleaning(df)

    with engine.connect() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table}"))
        conn.commit()

    df_clean.to_sql(table, engine, if_exists='append', index=False)