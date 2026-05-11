<div align="center">

# finance-db

**A MySQL data warehouse for quantitative research on U.S. equities and macro markets.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-9.4-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

## Overview

`finance-db` is a Python ETL stack that ingests fundamentals, market data, valuations, and macro series into a single MySQL warehouse (`finance_db`, **31 tables**). It's designed as the foundational data layer for systematic trading research — factor modeling, backtesting, and signal generation — with a strict separation between fetch, transform, and load.

**Sources:** FMP (fundamentals, ratings, DCF) · yfinance (daily OHLCV) · FRED (macro series).

## Architecture

```
   ┌─────────┐   ┌──────────┐   ┌────────┐
   │   FMP   │   │ yfinance │   │  FRED  │
   └────┬────┘   └────┬─────┘   └────┬───┘
        │             │              │
        ▼             ▼              ▼
   ┌─────────────────────────────────────┐
   │   fetchers/   →   API → DataFrame   │
   ├─────────────────────────────────────┤
   │   cleaners/   →   normalize, cast   │
   ├─────────────────────────────────────┤
   │   pipeline/   →   stage → INSERT    │   (only layer with DB side effects)
   └────────────────────┬────────────────┘
                        ▼
              ┌──────────────────────┐
              │   MySQL: finance_db  │
              │   31 tables · Docker │
              └──────────────────────┘
```

The pipeline layer writes every batch to a `temp_staging` table, then runs `INSERT IGNORE ... SELECT` into the target. Conflict resolution comes from each table's PK/UNIQUE constraints — there is no upsert, rows are append-only by natural key.

## Module Layout

| Module | Role |
|---|---|
| `pipeline/` | Orchestrators — the only layer that writes to the DB |
| `fetchers/` | API clients (FMP, yfinance, FRED) returning DataFrames or CSVs |
| `cleaners/` | Schema mapping, type casting, deduplication, staging-table writes |
| `updater/` | Incremental delta logic for FMP and yfinance refreshes |
| `config/` | SQLAlchemy engine, FMP schema map, paths |
| `sql/` | `mysqldump --no-data` snapshot of the live schema |

Entry points:
- `python -m pipeline.fmp_pipeline` — fundamentals + daily prices
- `python -m pipeline.macro_pipeline` — FRED macro series
- `python -m pipeline.sector_pipeline` — sector return aggregates
- `python -m pipeline.asset_class_pipeline` — cross-asset returns

## Schema at a Glance

All 31 tables fall into two grain families:

**Ticker-keyed** (PK `(ticker, date)` or `(ticker, date, period)`, FK → `companies(ticker)`):

| Domain | Tables |
|---|---|
| Identity & quotes | `companies`, `quotes`, `daily_prices` |
| Statements | `income_stmt`, `balance_sheet`, `cashflow` |
| Growth | `growth`, `income_stmt_growth`, `balance_sheet_growth`, `cashflow_growth` |
| Valuation | `ratios`, `metrics`, `ev`, `dcf`, `dcf_levered`, `ratings`, `scores` |
| Analyst / payout | `estimates`, `dividends` |

**Aggregate / time-series** (PK `(date)`, no FK):

| Domain | Tables |
|---|---|
| Macro | `macro_daily`, `macro_monthly`, `macro_quarterly` |
| Sector returns | `sector_returns_daily`, `sector_returns_monthly`, `sector_returns_quarterly` |
| Asset-class returns | `asset_class_returns_daily`, `asset_class_returns_monthly`, `asset_class_returns_quarterly` |
| Factor proxies | `factors_daily`, `factors_monthly`, `factors_quarterly` |

`companies` is the single dimension table; every ticker-keyed fact table joins through it. Type conventions: USD amounts use `double`; returns / ratios on aggregate tables use `decimal`.

Full DDL: [`sql/finance_db_schema.sql`](sql/finance_db_schema.sql).

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (for the MySQL container)
- API keys: [FMP](https://financialmodelingprep.com/), [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)

### Setup

```bash
# 1. Clone and install (editable, per pyproject.toml)
git clone https://github.com/TrungNguyen-ybidh/finance-db.git
cd finance-db
pip install -e .

# 2. Configure API keys
cat > .env <<EOF
FMP_api=your_fmp_key
FRED_api=your_fred_key
EOF

# 3. Start MySQL
docker run -d --name finance-db \
  -e MYSQL_ROOT_PASSWORD=yourpassword \
  -e MYSQL_DATABASE=finance_db \
  -p 3306:3306 mysql:9.4

# 4. Load the schema
mysql -h 127.0.0.1 -u root -p finance_db < sql/finance_db_schema.sql

# 5. Run a pipeline
python -m pipeline.fmp_pipeline
```

DB credentials are currently hardcoded in [`config/config.py`](config/config.py); `.env` only carries API keys.

### Smoke test

```bash
python -c "import pipeline.fmp_pipeline, pipeline.macro_pipeline, \
  pipeline.sector_pipeline, pipeline.asset_class_pipeline, \
  cleaners, fetchers, updater, config"
```

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| Database | MySQL 9.4 (Docker) |
| DB access | SQLAlchemy, PyMySQL |
| Data | pandas, NumPy, PyArrow |
| APIs | FMP (`requests`), `yfinance`, `fredapi` |
| Config | `python-dotenv` |

## Roadmap

- [ ] Move DB credentials out of `config/config.py` into `.env`
- [ ] Docker Compose for one-command bring-up
- [ ] Upsert support (`ON DUPLICATE KEY UPDATE`) for restatements
- [ ] Scheduler (Airflow / Prefect) for daily refresh
- [ ] Options and ETF coverage
- [ ] Read-only API layer over the warehouse

---

<div align="center">

*Built as the data foundation for systematic trading research.*

</div>
