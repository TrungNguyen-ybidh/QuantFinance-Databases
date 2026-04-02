<div align="center">

# QuantFinance-Databases

**A centralized financial data warehouse for quantitative research and algorithmic trading**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

*Aggregating equity fundamentals, market data, and macroeconomic indicators across U.S. equities into a unified, queryable data warehouse.*

---

</div>

## Overview

**QuantFinance-Databases** is a systematic financial data infrastructure that ingests, cleans, and stores multi-source financial data into a MySQL data warehouse containerized with Docker. It serves as the foundational data layer for quantitative research, factor modeling, and algorithmic trading strategies.

The pipeline aggregates data from **5 financial APIs** — FMP, SEC EDGAR, Polygon, yfinance, and FRED — providing comprehensive coverage of equity fundamentals, historical price data, and macroeconomic indicators for U.S. equities.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                │
│  ┌─────────┐ ┌───────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐  │
│  │   FMP   │ │ SEC EDGAR │ │ Polygon │ │ yfinance │ │   FRED   │  │
│  └────┬────┘ └─────┬─────┘ └────┬────┘ └─────┬────┘ └────┬─────┘  │
│       │             │            │             │            │        │
│       ▼             ▼            ▼             ▼            ▼        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     FETCHERS (Python ETL)                    │   │
│  │          API clients  ·  rate limiting  ·  pagination        │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                             │                                       │
│                             ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     CLEANERS (Transform)                     │   │
│  │      normalization  ·  type casting  ·  deduplication        │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                             │                                       │
│                             ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              MySQL DATA WAREHOUSE (Docker)                   │   │
│  │   equities · financials · prices · macro · SEC filings       │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Coverage

| Domain | Source | Data Type |
|---|---|---|
| **Equity Fundamentals** | FMP API | Income statements, balance sheets, cash flow statements, key metrics, company profiles |
| **SEC Filings** | SEC EDGAR | 10-K, 10-Q filings and structured financial data |
| **Market Data** | Polygon, yfinance | Historical OHLCV price data, splits, dividends |
| **Macroeconomic Indicators** | FRED API | GDP, CPI, unemployment, interest rates, yield curves |

## Project Structure

```
QuantFinance-Databases/
├── fetchers/           # API client modules for each data source
├── cleaners/           # Data transformation and normalization scripts
├── config/             # Database connection settings and API configurations
├── data/               # Local data staging directory
├── test/               # Test notebooks and validation scripts
├── finance-db.sql      # MySQL schema definition
├── pyproject.toml      # Package configuration
└── requirement.txt     # Python dependencies
```

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Docker** (for MySQL container)
- API keys for: [FMP](https://financialmodelingprep.com/), [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/TrungNguyen-ybidh/QuantFinance-Databases.git
   cd QuantFinance-Databases
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   FMP_api=your_fmp_api_key
   FRED_api=your_fred_api_key
   ```

4. **Start the MySQL container**
   ```bash
   docker run -d --name finance-db \
     -e MYSQL_ROOT_PASSWORD=yourpassword \
     -e MYSQL_DATABASE=finance_db \
     -p 3306:3306 \
     mysql:8.0
   ```

5. **Initialize the database schema**
   ```bash
   mysql -h 127.0.0.1 -u root -p finance_db < finance-db.sql
   ```

6. **Run the ETL pipeline**

   Use the fetcher modules to ingest data and the cleaner modules to transform it into the warehouse.

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Database** | MySQL 8.0 |
| **ORM / DB Access** | SQLAlchemy, PyMySQL |
| **Containerization** | Docker |
| **Data Processing** | pandas, NumPy, PyArrow |
| **Visualization** | matplotlib, seaborn |
| **API Clients** | requests, httpx, yfinance, fredapi, edgartools |
| **Config Management** | python-dotenv |

## Key Dependencies

Core libraries powering the pipeline:

- `SQLAlchemy` — Database ORM and connection management
- `pandas` / `PyArrow` — High-performance data manipulation
- `yfinance` — Yahoo Finance market data
- `fredapi` — Federal Reserve Economic Data
- `edgartools` — SEC EDGAR filings parser
- `httpx` / `requests` — Async and sync HTTP clients for API calls
- `python-dotenv` — Environment variable management

## Roadmap

- [ ] Add Docker Compose for one-command deployment
- [ ] Implement incremental data loading (upsert logic)
- [ ] Add Airflow/Prefect orchestration for scheduled ETL runs
- [ ] Expand coverage to ETFs and options data
- [ ] Build a REST API layer for querying the warehouse

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.

## License

This project is open source. See the repository for license details.

---

<div align="center">

**Built for quantitative research and algorithmic trading.**

</div>
=======
# finance-db

`finance-db` is a Python data pipeline project for collecting, cleaning, and loading financial market data.

The project currently focuses on:
- Fetching company fundamentals and ratios from Financial Modeling Prep (FMP)
- Fetching macroeconomic series from FRED
- Fetching market price data from Yahoo Finance
- Standardizing CSV schemas for downstream analysis and SQL loading

## Project Structure

- `fetchers/`: data ingestion modules (`FMP`, `FRED`, `Yahoo Finance`)
- `cleaners/`: data cleaning and schema transformation logic
- `config/`: endpoint lists, schema maps, utility helpers, and SQL engine config
- `data/raw/`: raw pulled datasets from APIs
- `data/cleanned/`: cleaned/renamed datasets
- `test/`: notebooks for exploratory testing and validation

## Requirements

- Python 3.10+ recommended
- Access to:
  - FMP API key
  - FRED API key (for macro series)
  - MySQL database (if using SQL loading utilities)

## Installation

```bash
cd /Users/tnguyen287/Documents/finance-db
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirement.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
FMP_api=your_fmp_api_key
FRED_api=your_fred_api_key
```

> `fetchers/fetching_fmp.py` reads `FMP_api` from `.env`.  
> Other modules may accept API keys as function arguments.

## Quick Start

### 1) Fetch FMP data

```python
import os
import pandas as pd
from dotenv import load_dotenv
from fetchers.fetching_fmp import fetch_fmp_data

load_dotenv()
api_key = os.getenv("FMP_api")

symbols = pd.read_csv("data/symbols_filtered.csv")["symbol"].dropna().unique().tolist()
fetch_fmp_data(symbols=symbols, api_key=api_key)
```

This writes endpoint CSVs into `data/raw/` (for example: `income-statement.csv`, `ratios.csv`, `profile.csv`).

### 2) Fetch Yahoo Finance OHLCV data

```python
import pandas as pd
from fetchers.fetch_yf import fetch_yf

symbols = ["AAPL", "MSFT", "GOOGL"]
price_df = fetch_yf(symbols, interval="1d", period="1y")
price_df.to_csv("data/raw/yf_prices.csv", index=False)
```

### 3) Fetch FRED macro data

```python
import os
from dotenv import load_dotenv
from fetchers.fetch_fred import fetch_macro_data

load_dotenv()
series_map = {
    "GDP": "gdp",
    "CPIAUCSL": "cpi",
    "FEDFUNDS": "fed_funds_rate",
}

macro_df = fetch_macro_data(series_map, api_key=os.getenv("FRED_api"))
macro_df.to_csv("data/macro_data/macro_series.csv", index=False)
```

### 4) Apply schema cleaning / renaming

```python
from cleaners.fmp_cleaner import keep_and_rename
from config.schema_config import schema_map

keep_and_rename(
    schema_map=schema_map,
    input_file="data/raw",
    output_file="data/cleanned",
    action=None,  # keep + rename based on schema_map
)
```

## SQL Loading Notes

`cleaners/fmp_cleaner.py` includes `insert_to_sql(...)`, which:
- reads cleaned CSVs,
- deduplicates and type-cleans key columns,
- truncates target MySQL table,
- appends cleaned data.

Before using SQL utilities, review and update connection settings in `config/config.py`.

## Packaging

This project is configured as a setuptools package via `pyproject.toml`:

```bash
pip install -e .
```

## Development Notes

- There is a typo in directory naming: `data/cleanned/` (double `n`) is used in code and data paths; keep it consistent unless you rename all references.
- `requirement.txt` contains both runtime and notebook/dev dependencies.
- Notebook-based testing is available in `test/`.

## Roadmap Ideas

- Add CLI entry points for fetch/clean/load jobs
- Add `.env.example` and move secrets out of source-controlled config
- Add unit tests for schema transformations
- Add incremental loading strategy instead of table truncation

