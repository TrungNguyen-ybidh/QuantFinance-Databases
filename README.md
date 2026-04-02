<div align="center">

# QuantFinance-Databases

**A centralized financial data warehouse for quantitative research and algorithmic trading**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-9.4-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

*Aggregating equity fundamentals, market data, valuation models, and macroeconomic indicators across U.S. equities into a unified, queryable data warehouse.*

---

</div>

## Overview

**QuantFinance-Databases** is a systematic financial data infrastructure that ingests, cleans, and stores multi-source financial data into a MySQL data warehouse containerized with Docker. It serves as the foundational data layer for quantitative research, factor modeling, and algorithmic trading strategies.

The pipeline aggregates data from **5 financial APIs** — FMP, SEC EDGAR, Polygon, yfinance, and FRED — and organizes it across **20 normalized tables** covering company profiles, financial statements, valuation models, growth metrics, analyst estimates, and more.

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
│  │              20 tables · finance_db schema                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Database Schema

The `finance_db` database contains **20 tables** organized into 6 domains. All financial tables reference `companies` as the central dimension table via foreign key on `ticker`.

### Entity-Relationship Overview

```
                          ┌──────────────┐
                          │  companies   │  (central dimension)
                          │   PK: ticker │
                          └──────┬───────┘
                                 │
          ┌──────────┬───────────┼───────────┬──────────┐
          │          │           │           │          │
          ▼          ▼           ▼           ▼          ▼
    ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
    │  income  │ │balance │ │cashflow│ │ ratios │ │  dcf   │
    │  _stmt   │ │_sheet  │ │        │ │        │ │        │
    └──────────┘ └────────┘ └────────┘ └────────┘ └────────┘
        │            │           │
        ▼            ▼           ▼
    ┌──────────┐ ┌────────┐ ┌────────┐
    │  income  │ │balance │ │cashflow│    ┌────────┐ ┌────────┐
    │  _stmt   │ │_sheet  │ │_growth │    │profile │ │ quotes │
    │  _growth │ │_growth │ │        │    └────────┘ └────────┘
    └──────────┘ └────────┘ └────────┘
```

### Table Reference

#### Company & Profile

| Table | PK | Description |
|---|---|---|
| `companies` | `ticker` | Central dimension table — name, sector, industry, exchange, CIK, ISIN, CUSIP, CEO, employees, IPO date |
| `profile` | `ticker` | Extended company profile with price, market cap, beta, description |
| `quotes` | `ticker` | Real-time snapshot — price, market cap, 52-week high/low, 50/200-day MA, volume |

#### Financial Statements

| Table | PK | Description |
|---|---|---|
| `income_stmt` | `ticker, date, period` | Revenue, COGS, gross profit, R&D, SG&A, operating income, EBITDA, EBIT, net income, EPS, shares outstanding |
| `balance_sheet` | `ticker, date, period` | Cash, receivables, inventory, PP&E, goodwill, total assets/liabilities, debt, equity |
| `cashflow` | `ticker, date, period` | Operating/investing/financing cash flows, free cash flow, CapEx, D&A, SBC, taxes and interest paid |

#### Growth & Trends

| Table | PK | Description |
|---|---|---|
| `growth` | `ticker, date, period` | Revenue/net income/EPS/EBITDA/FCF growth rates + 3Y, 5Y, 10Y CAGRs |
| `income_stmt_growth` | `ticker, date, period` | Period-over-period growth for revenue, gross profit, operating income, net income, EPS |
| `balance_sheet_growth` | `ticker, date, period` | Growth in total assets, liabilities, equity, debt, current assets/liabilities |
| `cashflow_growth` | `ticker, date, period` | Growth in operating CF, FCF, CapEx, dividends paid |

#### Valuation & Ratios

| Table | PK | Description |
|---|---|---|
| `ratios` | `ticker, date, period` | Profitability margins, turnover ratios, liquidity, leverage, P/E, P/B, P/S, EV multiples, dividend yield, tax rate |
| `metrics` | `ticker, date, period` | EV/Sales, EV/EBITDA, EV/FCF, ROA, ROE, ROIC, ROCE, Graham number, earnings yield, FCF yield, cash conversion cycle |
| `ev` | `ticker, date` | Enterprise value breakdown — stock price, shares outstanding, market cap, cash, debt |
| `dcf` | `ticker, date` | Discounted cash flow intrinsic value vs. stock price |
| `dcf_levered` | `ticker, date` | Levered DCF valuation vs. stock price |
| `scores` | `ticker` | Altman Z-Score and Piotroski F-Score with underlying components |
| `ratings` | `ticker, date` | Composite rating with sub-scores for DCF, ROE, ROA, D/E, P/E, P/B |

#### Estimates & Dividends

| Table | PK | Description |
|---|---|---|
| `estimates` | `ticker, date` | Consensus analyst estimates — revenue, EBITDA, net income, EPS, analyst count |
| `dividends` | `ticker, date` | Historical dividends, adjusted dividends, yield, and payment frequency |

#### Revenue Segmentation

| Table | PK | Description |
|---|---|---|
| `revenue_geographic_segmentation` | `ticker, date` | Revenue breakdown by geography (stored as JSON) |
| `revenue_product_segmentation` | `ticker, date` | Revenue breakdown by product/service line (stored as JSON) |

## Data Coverage

| Domain | Source | Examples |
|---|---|---|
| **Equity Fundamentals** | FMP API | Income statements, balance sheets, cash flow, key metrics, ratios |
| **Valuation Models** | FMP API | DCF (standard + levered), enterprise value, analyst estimates, ratings |
| **Growth Analytics** | FMP API | Period-over-period growth, 3/5/10Y CAGRs across financials |
| **Quality Scores** | FMP API | Altman Z-Score, Piotroski F-Score |
| **Segmentation** | FMP API | Revenue by geography and product (JSON) |
| **SEC Filings** | SEC EDGAR | 10-K, 10-Q structured financial data |
| **Market Data** | Polygon, yfinance | Historical OHLCV, dividends, splits, real-time quotes |
| **Macroeconomic** | FRED API | GDP, CPI, unemployment, interest rates, yield curves |

## Project Structure

```
QuantFinance-Databases/
├── fetchers/           # API client modules for each data source
├── cleaners/           # Data transformation and normalization scripts
├── config/             # Database connection settings and API configurations
├── data/               # Local data staging directory
├── test/               # Test notebooks and validation scripts
├── finance-db.sql      # MySQL schema definition (20 tables)
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
     mysql:9.4
   ```

5. **Initialize the database schema**
   ```bash
   mysql -h 127.0.0.1 -u root -p finance_db < finance-db.sql
   ```

6. **Run the ETL pipeline**

   Use the fetcher modules to ingest data and the cleaner modules to transform and load into the warehouse.

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Database** | MySQL 9.4 |
| **ORM / DB Access** | SQLAlchemy, PyMySQL |
| **Containerization** | Docker |
| **Data Processing** | pandas, NumPy, PyArrow |
| **Visualization** | matplotlib, seaborn |
| **API Clients** | requests, httpx, yfinance, fredapi, edgartools |
| **Config Management** | python-dotenv |

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