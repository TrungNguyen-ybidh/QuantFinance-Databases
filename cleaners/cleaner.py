"""Generic and FMP-specific data cleaners + DB load helpers."""
import ast
import shutil
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from config import engine
from fetchers.fetcher import Fetcher


class Cleaner:
    """Clean tabular data and load it into MySQL."""

    def __init__(self, root):
        self.root = Path(root) if root else Path.cwd().parent

    # ---------- transformations ---------- #

    def ff_factor_clean(self, df, monthly=False, quarterly=False):
        """Normalize Fama-French factor exports. Caller passes index=False on save."""
        df.columns = df.columns.str.lower()
        df_clean = df.rename(columns={
            "unnamed: 0": "date",
            "mkt-rf": "market_excess_return",
            "smb": "size_factor",
            "hml": "value_factor",
            "rmw": "profitability_factor",
            "cma": "investment_factor",
            "rf": "risk_free_rate",
        })
        df_clean["date"] = pd.to_datetime(df_clean["date"].astype(str), format="%Y%m%d")

        if monthly or quarterly:
            df_clean = df_clean.set_index("date")
            rule = "ME" if monthly else "QE"
            return df_clean.resample(rule).sum().round(2).reset_index()

        return df_clean

    def data_cleaning(self, df, existent=False):
        """Parse date columns and drop duplicates on the natural key."""
        if existent:
            existing = pd.read_sql("SELECT ticker FROM companies", engine)
            df_clean = df[df["ticker"].isin(existing["ticker"])].copy()
        else:
            df_clean = df.copy()

        for col in [c for c in df_clean.columns if "date" in c.lower()]:
            df_clean[col] = pd.to_datetime(df_clean[col], errors="coerce")

        has = lambda c: c in df_clean.columns
        if has("ticker") and has("date") and has("period"):
            return df_clean.drop_duplicates(subset=["ticker", "date", "period"], keep="first")
        if has("ticker") and has("date"):
            return df_clean.drop_duplicates(subset=["ticker", "date"], keep="first")
        if has("date"):
            return df_clean.drop_duplicates(subset=["date"], keep="first")
        return df_clean.drop_duplicates()

    # ---------- DB load ---------- #

    def insert_to_sql(self, table, df=None, file=None, *,
                      mode="update", clean=True, exist=False):
        """Load `df` (or a CSV at `file`) into `table`.

        mode:
          "update"  -> INSERT IGNORE via temp_staging (skip duplicates;
                       conflict resolution uses the table's PK/UNIQUE keys).
          "replace" -> TRUNCATE then append.
          "append"  -> plain df.to_sql append (caller handles duplicates).
        """
        if df is None and file is not None:
            path = self.root / ("cleaned" if clean else "") / file
            df = pd.read_csv(path)
            print(f"{file}: {list(df.columns)}")
        elif df is not None:
            print(f"{table}: {list(df.columns)}")
        else:
            raise ValueError("Provide either df or file")

        df_clean = self.data_cleaning(df, existent=exist) if clean else df

        if mode == "replace":
            with engine.connect() as conn:
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
                conn.execute(text(f"TRUNCATE TABLE {table}"))
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
                df_clean.dropna(subset=["date"]).to_sql(table, conn, if_exists="append", index=False)
                conn.commit()
            return

        if mode == "append":
            df_clean.to_sql(table, engine, if_exists="append", index=False)
            return

        # default: update via INSERT IGNORE
        df_clean.to_sql("temp_staging", engine, if_exists="replace", index=False)
        cols = ", ".join(f"`{c}`" for c in df_clean.columns)
        with engine.connect() as conn:
            conn.execute(text(f"INSERT IGNORE INTO {table} ({cols}) SELECT {cols} FROM temp_staging"))
            conn.execute(text("DROP TABLE temp_staging"))
            conn.commit()

    # ---------- helpers ---------- #

    def parse_dict_col(self, file_path=None, col=None, col_lst=None):
        """Expand JSON/dict-valued columns in-place. Saves back to disk."""
        file_path = file_path or self.root
        df = pd.read_csv(file_path, low_memory=False)

        cols = col_lst if col_lst else ([col] if col else [])
        if not cols:
            return df

        for c in cols:
            try:
                expanded = pd.json_normalize(df[c])
            except Exception:
                expanded = pd.json_normalize(df[c].apply(ast.literal_eval))
            df = pd.concat([df.drop(columns=[c]), expanded], axis=1)

        Fetcher().save_csv(df, file_path=file_path)
        return df

    def clean_dir(self):
        cleaned = self.root / "cleaned"
        if cleaned.exists():
            shutil.rmtree(cleaned)
            print(f"Removed {cleaned}")


class FMPCleaner(Cleaner):
    """FMP-specific column filtering/renaming via schema_map."""

    def keep_and_rename(self, schema_map, input_file=None, action=None):
        input_dir = Path(input_file) if input_file else Path(self.root)
        output_dir = input_dir / "cleaned"
        output_dir.mkdir(exist_ok=True)
        result = {}
        fetcher = Fetcher()

        for filename, spec in schema_map.items():
            try:
                df = pd.read_csv(input_dir / filename, low_memory=False)
                if action is None:
                    df = df[spec["keep"]].rename(columns=spec["rename"])
                elif action == "keep":
                    df = df[spec["keep"]]
                elif action == "rename":
                    df = df.rename(columns=spec["rename"])
                elif action == "drop":
                    df = df.drop(columns=spec["drop"])
                fetcher.save_csv(df, file_path=str(output_dir / filename))
                result[filename] = df
            except Exception as e:
                print(f"{filename} — {e}")

        return result
