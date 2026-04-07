import ast
import pandas as pd
from config.config import engine
from fetchers.fetcher import Fetcher 
from sqlalchemy import text
from pathlib import Path
from config.schema_config import schema_map

class Cleaner:
    """Clean FMP fundamentals data: parse dict columns, keep/rename/drop fields."""
    def __init__(self, root):
        self.root = Path(root) if root else Path.cwd().parent

    def data_cleaning(self, df, existent=True):
        if existent:
            existing = pd.read_sql("SELECT ticker FROM companies", engine)
            df_clean = df[df['ticker'].isin(existing['ticker'])].copy()
        else:
            df_clean = df.copy()

        date_cols = [col for col in df.columns if 'date' in col.lower()]
        
        for col in date_cols:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        
        if 'period' in df.columns and 'date' in df.columns:
            df_clean = df_clean.drop_duplicates(subset=['ticker', 'date', 'period'], keep='first')
        elif 'date' in df.columns:
            df_clean = df_clean.drop_duplicates(subset=['ticker', 'date'], keep='first')
        else:
            df_clean = df_clean.drop_duplicates()
        
        return df_clean

    def insert_to_sql(self, table, update=True, replace=False, file=None, df=None, conflict_cols=["ticker", "date"]):
        if df is None and file is not None:
            df = pd.read_csv(f"{self.root}/data/cleanned/{file}")
            print(f"{file}: {list(df.columns)}")
            df_clean = self.data_cleaning(df)
        elif df is not None:
            print(f"{table}: {list(df.columns)}")
            df_clean = self.data_cleaning(df)

        if replace:
            with engine.connect() as conn:
                conn.execute(text(f"TRUNCATE TABLE {table}"))
                conn.commit()
            df_clean.to_sql(table, engine, if_exists="append", index=False)
            return

        if update:
            # Skip duplicates, only insert new rows
            df_clean.to_sql("temp_staging", engine, if_exists="replace", index=False)
            cols = ", ".join(df_clean.columns)
            conflict = ", ".join(conflict_cols)
            with engine.connect() as conn:
                conn.execute(text(f"""
                    INSERT INTO {table} ({cols})
                    SELECT {cols} FROM temp_staging
                    ON CONFLICT ({conflict}) DO NOTHING
                """))
                conn.execute(text("DROP TABLE temp_staging"))
                conn.commit()
        else:
            df_clean.to_sql(table, engine, if_exists="append", index=False)


    def parse_dict_col(self, file_path=None, col=None, col_lst=None):
        file_path = file_path or self.root
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

    
class FMPCleaner(Cleaner):
    def __init__(self, root):
        super().__init__(root)

    def keep_and_rename(self, schema_map=None, input_file=None, action=None):
        input_file = input_file or self.root
        output_file = Path(f"{input_file}/cleanned")
        output_file.mkdir(exist_ok=True)
        result = {}
        fetcher = Fetcher()

        for key, value in schema_map.items():
            try:
                df = pd.read_csv(f"{input_file}/{key}", low_memory=False)

                if action is None:
                    # default: keep columns then rename
                    df = df[value["keep"]]
                    df = df.rename(columns=value["rename"])
                elif action == "keep":
                    df = df[value["keep"]]
                elif action == "rename":
                    df = df.rename(columns=value["rename"])
                elif action == "drop":
                    df = df.drop(columns=value["drop"])

                fetcher.save_csv(df, file_path=f"{output_file}/{key}")
                result[key] = df
            except Exception as e:
                print(f"{key} — {e}")

        return result