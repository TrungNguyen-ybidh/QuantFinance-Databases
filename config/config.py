from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://tnguyen:thyngu123@192.168.1.26:3306/finance_db"
)


with engine.connect() as conn:
    result = conn.execute(text("SHOW TABLES;"))
    for row in result:
        print(row)