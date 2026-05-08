/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `asset_class_returns_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asset_class_returns_daily` (
  `date` date NOT NULL,
  `bitcoin` decimal(10,4) DEFAULT NULL,
  `real_estate` decimal(10,4) DEFAULT NULL,
  `us_agg_bonds` decimal(10,4) DEFAULT NULL,
  `large_cap_growth` decimal(10,4) DEFAULT NULL,
  `large_cap_value` decimal(10,4) DEFAULT NULL,
  `small_cap` decimal(10,4) DEFAULT NULL,
  `long_term_treasury` decimal(10,4) DEFAULT NULL,
  `equal_weight_sp500` decimal(10,4) DEFAULT NULL,
  `emerging_markets` decimal(10,4) DEFAULT NULL,
  `short_term_treasury` decimal(10,4) DEFAULT NULL,
  `intl_developed` decimal(10,4) DEFAULT NULL,
  `gold` decimal(10,4) DEFAULT NULL,
  `oil` decimal(10,4) DEFAULT NULL,
  `us_large_cap` decimal(10,4) DEFAULT NULL,
  `high_yield_bonds` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `asset_class_returns_monthly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asset_class_returns_monthly` (
  `date` date NOT NULL,
  `bitcoin` decimal(10,4) DEFAULT NULL,
  `real_estate` decimal(10,4) DEFAULT NULL,
  `us_agg_bonds` decimal(10,4) DEFAULT NULL,
  `large_cap_growth` decimal(10,4) DEFAULT NULL,
  `large_cap_value` decimal(10,4) DEFAULT NULL,
  `small_cap` decimal(10,4) DEFAULT NULL,
  `long_term_treasury` decimal(10,4) DEFAULT NULL,
  `equal_weight_sp500` decimal(10,4) DEFAULT NULL,
  `emerging_markets` decimal(10,4) DEFAULT NULL,
  `short_term_treasury` decimal(10,4) DEFAULT NULL,
  `intl_developed` decimal(10,4) DEFAULT NULL,
  `gold` decimal(10,4) DEFAULT NULL,
  `oil` decimal(10,4) DEFAULT NULL,
  `us_large_cap` decimal(10,4) DEFAULT NULL,
  `high_yield_bonds` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `asset_class_returns_quarterly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asset_class_returns_quarterly` (
  `date` date NOT NULL,
  `bitcoin` decimal(10,4) DEFAULT NULL,
  `real_estate` decimal(10,4) DEFAULT NULL,
  `us_agg_bonds` decimal(10,4) DEFAULT NULL,
  `large_cap_growth` decimal(10,4) DEFAULT NULL,
  `large_cap_value` decimal(10,4) DEFAULT NULL,
  `small_cap` decimal(10,4) DEFAULT NULL,
  `long_term_treasury` decimal(10,4) DEFAULT NULL,
  `equal_weight_sp500` decimal(10,4) DEFAULT NULL,
  `emerging_markets` decimal(10,4) DEFAULT NULL,
  `short_term_treasury` decimal(10,4) DEFAULT NULL,
  `intl_developed` decimal(10,4) DEFAULT NULL,
  `gold` decimal(10,4) DEFAULT NULL,
  `oil` decimal(10,4) DEFAULT NULL,
  `us_large_cap` decimal(10,4) DEFAULT NULL,
  `high_yield_bonds` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `balance_sheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `balance_sheet` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `period` varchar(10) NOT NULL,
  `cash` double DEFAULT NULL,
  `short_term_investments` double DEFAULT NULL,
  `cash_and_short_term_investments` double DEFAULT NULL,
  `net_receivables` double DEFAULT NULL,
  `inventory` double DEFAULT NULL,
  `total_current_assets` double DEFAULT NULL,
  `ppe_net` double DEFAULT NULL,
  `goodwill` double DEFAULT NULL,
  `intangible_assets` double DEFAULT NULL,
  `long_term_investments` double DEFAULT NULL,
  `tax_assets` double DEFAULT NULL,
  `total_non_current_assets` double DEFAULT NULL,
  `total_assets` double DEFAULT NULL,
  `accounts_payable` double DEFAULT NULL,
  `accrued_expenses` double DEFAULT NULL,
  `short_term_debt` double DEFAULT NULL,
  `deferred_revenue` double DEFAULT NULL,
  `total_current_liabilities` double DEFAULT NULL,
  `long_term_debt` double DEFAULT NULL,
  `total_non_current_liabilities` double DEFAULT NULL,
  `total_liabilities` double DEFAULT NULL,
  `retained_earnings` double DEFAULT NULL,
  `additional_paid_in_capital` double DEFAULT NULL,
  `stockholders_equity` double DEFAULT NULL,
  `total_equity` double DEFAULT NULL,
  `total_debt` double DEFAULT NULL,
  `net_debt` double DEFAULT NULL,
  `filing_date` datetime DEFAULT NULL,
  `accepted_date` datetime DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`,`period`),
  CONSTRAINT `balance_sheet_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `balance_sheet_growth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `balance_sheet_growth` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `period` varchar(10) NOT NULL,
  `growth_total_assets` double DEFAULT NULL,
  `growth_total_liabilities` double DEFAULT NULL,
  `growth_total_equity` double DEFAULT NULL,
  `growth_total_debt` double DEFAULT NULL,
  `growth_net_debt` double DEFAULT NULL,
  `growth_total_current_assets` double DEFAULT NULL,
  `growth_total_current_liabilities` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`,`period`),
  CONSTRAINT `balance_sheet_growth_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `cashflow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashflow` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `period` varchar(10) NOT NULL,
  `net_income` double DEFAULT NULL,
  `depreciation_amortization` double DEFAULT NULL,
  `stock_based_compensation` double DEFAULT NULL,
  `deferred_income_tax` double DEFAULT NULL,
  `change_in_working_capital` double DEFAULT NULL,
  `cash_from_operations` double DEFAULT NULL,
  `ppe_investments` double DEFAULT NULL,
  `acquisitions_net` double DEFAULT NULL,
  `purchases_of_investments` double DEFAULT NULL,
  `sales_of_investments` double DEFAULT NULL,
  `cash_from_investing` double DEFAULT NULL,
  `net_debt_issuance` double DEFAULT NULL,
  `stock_repurchased` double DEFAULT NULL,
  `dividends_paid` double DEFAULT NULL,
  `cash_from_financing` double DEFAULT NULL,
  `operating_cash_flow` double DEFAULT NULL,
  `capex` double DEFAULT NULL,
  `free_cash_flow` double DEFAULT NULL,
  `income_taxes_paid` double DEFAULT NULL,
  `interest_paid` double DEFAULT NULL,
  `filing_date` datetime DEFAULT NULL,
  `accepted_date` datetime DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`,`period`),
  CONSTRAINT `cashflow_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `cashflow_growth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashflow_growth` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `period` varchar(10) NOT NULL,
  `growth_operating_cash_flow` double DEFAULT NULL,
  `growth_free_cash_flow` double DEFAULT NULL,
  `growth_capex` double DEFAULT NULL,
  `growth_net_change_in_cash` double DEFAULT NULL,
  `growth_dividends_paid` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`,`period`),
  CONSTRAINT `cashflow_growth_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `ticker` varchar(10) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `market_cap` double DEFAULT NULL,
  `beta` double DEFAULT NULL,
  `sector` varchar(100) DEFAULT NULL,
  `industry` varchar(150) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `cik` int DEFAULT NULL,
  `isin` varchar(20) DEFAULT NULL,
  `cusip` varchar(20) DEFAULT NULL,
  `exchange` varchar(20) DEFAULT NULL,
  `ceo` varchar(100) DEFAULT NULL,
  `full_time_employees` bigint DEFAULT NULL,
  `ipo_date` date DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `daily_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_prices` (
  `date` datetime NOT NULL,
  `ticker` varchar(10) NOT NULL,
  `close` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `open` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  PRIMARY KEY (`date`,`ticker`),
  KEY `ticker` (`ticker`),
  CONSTRAINT `daily_prices_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `dcf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dcf` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `dcf` double DEFAULT NULL,
  `stock_price` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  CONSTRAINT `dcf_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `dcf_levered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dcf_levered` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `levered_dcf` double DEFAULT NULL,
  `stock_price` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  CONSTRAINT `dcf_levered_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `dividends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dividends` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `adj_dividend` double DEFAULT NULL,
  `dividend` double DEFAULT NULL,
  `dividend_yield` double DEFAULT NULL,
  `frequency` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  CONSTRAINT `dividends_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `estimates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimates` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `est_revenue_avg` double DEFAULT NULL,
  `est_ebitda_avg` double DEFAULT NULL,
  `est_net_income_avg` double DEFAULT NULL,
  `est_eps_avg` double DEFAULT NULL,
  `num_analysts_revenue` int DEFAULT NULL,
  `num_analysts_eps` int DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  CONSTRAINT `estimates_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `ev`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ev` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `stock_price` double DEFAULT NULL,
  `shares_outstanding` double DEFAULT NULL,
  `market_cap` double DEFAULT NULL,
  `minus_cash` double DEFAULT NULL,
  `plus_total_debt` double DEFAULT NULL,
  `enterprise_value` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  CONSTRAINT `ev_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `factors_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factors_daily` (
  `date` date NOT NULL,
  `market_excess_return` decimal(10,4) DEFAULT NULL,
  `size_factor` decimal(10,4) DEFAULT NULL,
  `value_factor` decimal(10,4) DEFAULT NULL,
  `profitability_factor` decimal(10,4) DEFAULT NULL,
  `inveatment_factor` decimal(10,4) DEFAULT NULL,
  `risk_free_rate` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `factors_monthly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factors_monthly` (
  `date` date NOT NULL,
  `market_excess_return` decimal(10,4) DEFAULT NULL,
  `size_factor` decimal(10,4) DEFAULT NULL,
  `value_factor` decimal(10,4) DEFAULT NULL,
  `profitability_factor` decimal(10,4) DEFAULT NULL,
  `inveatment_factor` decimal(10,4) DEFAULT NULL,
  `risk_free_rate` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `factors_quarterly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factors_quarterly` (
  `date` date NOT NULL,
  `market_excess_return` decimal(10,4) DEFAULT NULL,
  `size_factor` decimal(10,4) DEFAULT NULL,
  `value_factor` decimal(10,4) DEFAULT NULL,
  `profitability_factor` decimal(10,4) DEFAULT NULL,
  `inveatment_factor` decimal(10,4) DEFAULT NULL,
  `risk_free_rate` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `growth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `growth` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `revenue_growth` double DEFAULT NULL,
  `gross_profit_growth` double DEFAULT NULL,
  `operating_income_growth` double DEFAULT NULL,
  `net_income_growth` double DEFAULT NULL,
  `eps_diluted_growth` double DEFAULT NULL,
  `ebitda_growth` double DEFAULT NULL,
  `operating_cf_growth` double DEFAULT NULL,
  `fcf_growth` double DEFAULT NULL,
  `revenue_cagr_3y` double DEFAULT NULL,
  `revenue_cagr_5y` double DEFAULT NULL,
  `revenue_cagr_10y` double DEFAULT NULL,
  `net_income_cagr_3y` double DEFAULT NULL,
  `net_income_cagr_5y` double DEFAULT NULL,
  `net_income_cagr_10y` double DEFAULT NULL,
  `operating_cf_cagr_3y` double DEFAULT NULL,
  `operating_cf_cagr_5y` double DEFAULT NULL,
  `operating_cf_cagr_10y` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  CONSTRAINT `growth_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `income_stmt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `income_stmt` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `period` varchar(10) NOT NULL,
  `revenue` double DEFAULT NULL,
  `cost_of_revenue` double DEFAULT NULL,
  `gross_profit` double DEFAULT NULL,
  `rd_expenses` double DEFAULT NULL,
  `sga_expenses` double DEFAULT NULL,
  `operating_expenses` double DEFAULT NULL,
  `operating_income` double DEFAULT NULL,
  `interest_income` double DEFAULT NULL,
  `interest_expense` double DEFAULT NULL,
  `depreciation_amortization` double DEFAULT NULL,
  `ebitda` double DEFAULT NULL,
  `ebit` double DEFAULT NULL,
  `income_before_tax` double DEFAULT NULL,
  `income_tax_expense` double DEFAULT NULL,
  `net_income` double DEFAULT NULL,
  `eps` double DEFAULT NULL,
  `eps_diluted` double DEFAULT NULL,
  `shares_outstanding` double DEFAULT NULL,
  `shares_outstanding_diluted` double DEFAULT NULL,
  `filing_date` datetime DEFAULT NULL,
  `accepted_date` datetime DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`,`period`),
  CONSTRAINT `income_stmt_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `income_stmt_growth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `income_stmt_growth` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `period` varchar(10) NOT NULL,
  `growth_revenue` double DEFAULT NULL,
  `growth_gross_profit` double DEFAULT NULL,
  `growth_operating_income` double DEFAULT NULL,
  `growth_net_income` double DEFAULT NULL,
  `growth_ebitda` double DEFAULT NULL,
  `growth_eps` double DEFAULT NULL,
  `growth_eps_diluted` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`,`period`),
  CONSTRAINT `income_stmt_growth_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `macro_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `macro_daily` (
  `date` date NOT NULL,
  `inflation_exp` decimal(10,4) DEFAULT NULL,
  `ted_spread` decimal(10,4) DEFAULT NULL,
  `interest_rate` decimal(10,4) DEFAULT NULL,
  `yield_curve` decimal(10,4) DEFAULT NULL,
  `wti` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `macro_monthly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `macro_monthly` (
  `date` date NOT NULL,
  `pmi` decimal(12,4) DEFAULT NULL,
  `sahm_rule` decimal(10,4) DEFAULT NULL,
  `recession` decimal(10,4) DEFAULT NULL,
  `retail_sales` decimal(12,4) DEFAULT NULL,
  `core_cpi` decimal(10,4) DEFAULT NULL,
  `unrate` decimal(10,4) DEFAULT NULL,
  `fedfunds` decimal(10,4) DEFAULT NULL,
  `headline_cpi` decimal(10,4) DEFAULT NULL,
  `consumer_sentiment` decimal(10,4) DEFAULT NULL,
  `industrial_production` decimal(10,4) DEFAULT NULL,
  `m2` decimal(12,4) DEFAULT NULL,
  `pce` decimal(12,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `macro_quarterly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `macro_quarterly` (
  `date` date NOT NULL,
  `potential_gdp` decimal(14,4) DEFAULT NULL,
  `nominal_gdp` decimal(14,4) DEFAULT NULL,
  `real_gdp` decimal(14,4) DEFAULT NULL,
  `fedfunds` decimal(10,4) DEFAULT NULL,
  `yield_curve` decimal(10,4) DEFAULT NULL,
  `hy_spread` decimal(10,4) DEFAULT NULL,
  `wti` decimal(10,4) DEFAULT NULL,
  `unrate` decimal(10,4) DEFAULT NULL,
  `sahm_rule` decimal(10,4) DEFAULT NULL,
  `recession` decimal(10,4) DEFAULT NULL,
  `headline_cpi` decimal(10,4) DEFAULT NULL,
  `core_cpi` decimal(10,4) DEFAULT NULL,
  `pce` decimal(12,4) DEFAULT NULL,
  `m2` decimal(12,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metrics` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `market_cap` double DEFAULT NULL,
  `enterprise_value` double DEFAULT NULL,
  `ev_to_sales` double DEFAULT NULL,
  `ev_to_ebitda` double DEFAULT NULL,
  `ev_to_fcf` double DEFAULT NULL,
  `net_debt_to_ebitda` double DEFAULT NULL,
  `current_ratio` double DEFAULT NULL,
  `income_quality` double DEFAULT NULL,
  `graham_number` double DEFAULT NULL,
  `working_capital` double DEFAULT NULL,
  `invested_capital` double DEFAULT NULL,
  `roa` double DEFAULT NULL,
  `roe` double DEFAULT NULL,
  `roic` double DEFAULT NULL,
  `roce` double DEFAULT NULL,
  `earnings_yield` double DEFAULT NULL,
  `fcf_yield` double DEFAULT NULL,
  `rd_to_revenue` double DEFAULT NULL,
  `sbc_to_revenue` double DEFAULT NULL,
  `capex_to_revenue` double DEFAULT NULL,
  `days_sales_outstanding` double DEFAULT NULL,
  `days_payables_outstanding` double DEFAULT NULL,
  `days_inventory_outstanding` double DEFAULT NULL,
  `cash_conversion_cycle` double DEFAULT NULL,
  `fcf_to_equity` double DEFAULT NULL,
  `fcf_to_firm` double DEFAULT NULL,
  `tangible_asset_value` double DEFAULT NULL,
  `net_current_asset_value` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  CONSTRAINT `metrics_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `quotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quotes` (
  `ticker` varchar(10) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `market_cap` double DEFAULT NULL,
  `year_high` double DEFAULT NULL,
  `year_low` double DEFAULT NULL,
  `price_avg_50` double DEFAULT NULL,
  `price_avg_200` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  PRIMARY KEY (`ticker`),
  CONSTRAINT `quotes_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `rating` varchar(10) DEFAULT NULL,
  `overall_score` int DEFAULT NULL,
  `dcf_score` int DEFAULT NULL,
  `roe_score` int DEFAULT NULL,
  `roa_score` int DEFAULT NULL,
  `de_score` int DEFAULT NULL,
  `pe_score` int DEFAULT NULL,
  `pb_score` int DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  KEY `idx_ratings_date` (`date`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `ratios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratios` (
  `ticker` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `fiscal_year` varchar(10) DEFAULT NULL,
  `gross_margin` double DEFAULT NULL,
  `ebit_margin` double DEFAULT NULL,
  `ebitda_margin` double DEFAULT NULL,
  `operating_margin` double DEFAULT NULL,
  `net_margin` double DEFAULT NULL,
  `receivables_turnover` double DEFAULT NULL,
  `payables_turnover` double DEFAULT NULL,
  `inventory_turnover` double DEFAULT NULL,
  `fixed_asset_turnover` double DEFAULT NULL,
  `asset_turnover` double DEFAULT NULL,
  `current_ratio` double DEFAULT NULL,
  `quick_ratio` double DEFAULT NULL,
  `debt_to_equity` double DEFAULT NULL,
  `debt_to_assets` double DEFAULT NULL,
  `financial_leverage` double DEFAULT NULL,
  `interest_coverage` double DEFAULT NULL,
  `pe_ratio` double DEFAULT NULL,
  `pb_ratio` double DEFAULT NULL,
  `ps_ratio` double DEFAULT NULL,
  `p_to_fcf` double DEFAULT NULL,
  `ev_multiple` double DEFAULT NULL,
  `ocf_to_sales` double DEFAULT NULL,
  `fcf_to_ocf` double DEFAULT NULL,
  `dividend_payout_ratio` double DEFAULT NULL,
  `dividend_yield` double DEFAULT NULL,
  `effective_tax_rate` double DEFAULT NULL,
  PRIMARY KEY (`ticker`,`date`),
  CONSTRAINT `ratios_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scores` (
  `ticker` varchar(10) NOT NULL,
  `altman_z_score` double DEFAULT NULL,
  `piotroski_score` int DEFAULT NULL,
  `working_capital` double DEFAULT NULL,
  `total_assets` double DEFAULT NULL,
  `retained_earnings` double DEFAULT NULL,
  `ebit` double DEFAULT NULL,
  `market_cap` double DEFAULT NULL,
  `total_liabilities` double DEFAULT NULL,
  `revenue` double DEFAULT NULL,
  PRIMARY KEY (`ticker`),
  CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `companies` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `sector_returns_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sector_returns_daily` (
  `date` date NOT NULL,
  `utilities` decimal(10,4) DEFAULT NULL,
  `consumer_staples` decimal(10,4) DEFAULT NULL,
  `financials` decimal(10,4) DEFAULT NULL,
  `communication_services` decimal(10,4) DEFAULT NULL,
  `technology` decimal(10,4) DEFAULT NULL,
  `materials` decimal(10,4) DEFAULT NULL,
  `energy` decimal(10,4) DEFAULT NULL,
  `real_estate` decimal(10,4) DEFAULT NULL,
  `consumer_discretionary` decimal(10,4) DEFAULT NULL,
  `industrials` decimal(10,4) DEFAULT NULL,
  `healthcare` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `sector_returns_monthly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sector_returns_monthly` (
  `date` date NOT NULL,
  `utilities` decimal(10,4) DEFAULT NULL,
  `consumer_staples` decimal(10,4) DEFAULT NULL,
  `financials` decimal(10,4) DEFAULT NULL,
  `communication_services` decimal(10,4) DEFAULT NULL,
  `technology` decimal(10,4) DEFAULT NULL,
  `materials` decimal(10,4) DEFAULT NULL,
  `energy` decimal(10,4) DEFAULT NULL,
  `real_estate` decimal(10,4) DEFAULT NULL,
  `consumer_discretionary` decimal(10,4) DEFAULT NULL,
  `industrials` decimal(10,4) DEFAULT NULL,
  `healthcare` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `sector_returns_quarterly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sector_returns_quarterly` (
  `date` date NOT NULL,
  `utilities` decimal(10,4) DEFAULT NULL,
  `consumer_staples` decimal(10,4) DEFAULT NULL,
  `financials` decimal(10,4) DEFAULT NULL,
  `communication_services` decimal(10,4) DEFAULT NULL,
  `technology` decimal(10,4) DEFAULT NULL,
  `materials` decimal(10,4) DEFAULT NULL,
  `energy` decimal(10,4) DEFAULT NULL,
  `real_estate` decimal(10,4) DEFAULT NULL,
  `consumer_discretionary` decimal(10,4) DEFAULT NULL,
  `industrials` decimal(10,4) DEFAULT NULL,
  `healthcare` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

