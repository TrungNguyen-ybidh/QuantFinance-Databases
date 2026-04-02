from sqlalchemy import create_engine, text
from pathlib import Path

ROOT = Path.cwd().parent

engine = create_engine(
    "mysql+pymysql://tnguyen:thyngu123@10.10.73.34:3306/finance_db"
)

