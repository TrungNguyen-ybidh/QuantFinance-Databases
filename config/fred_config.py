"""
FRED Series Map Configuration
G10 Currency Countries + US-Specific Extras
"""

# --- G10 Currency Countries ---
G10_COUNTRIES = {
    "US": "United States",
    "CA": "Canada",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "IT": "Italy",
    "NL": "Netherlands",
    "BE": "Belgium",
    "SE": "Sweden",
    "JP": "Japan",
    "CH": "Switzerland",
    "AU": "Australia",
    "NO": "Norway",
    "NZ": "New Zealand",
}


# =============================================================================
# SHARED G10 TABLES — All 14 countries
# =============================================================================

# --- Real GDP (Quarterly) ---
MACRO_GDP = {
    "US": "GDPC1",
    "CA": "NAEXKP01CAQ189S",
    "GB": "NGDPRSAXDCGBQ",
    "DE": "CLVMNACSCAB1GQDE",
    "FR": "CLVMNACSCAB1GQFR",
    "IT": "CLVMNACSCAB1GQIT",
    "NL": "CLVMNACSCAB1GQNL",
    "BE": "CLVMNACSCAB1GQBE",
    "SE": "CLVMNACSCAB1GQSE",
    "JP": "NAEXKP01JPQ189S",
    "CH": "CLVMNACSAB1GQCH",  
    "AU": "NGDPRSAXDCAUQ",
    "NO": "CLVMNACSCAB1GQNO",
    "NZ": "NAEXKP01NZQ189S",
}

# --- CPI Inflation YoY % (Annual, World Bank) ---
MACRO_CPI = {
    "US": "FPCPITOTLZGUSA",
    "CA": "FPCPITOTLZGCAN",
    "GB": "NAEXKP01GBQ661S",
    "DE": "FPCPITOTLZGDEU",
    "FR": "FPCPITOTLZGFRA",
    "IT": "FPCPITOTLZGITA",
    "NL": "FPCPITOTLZGNLD",
    "BE": "FPCPITOTLZGBEL",
    "SE": "FPCPITOTLZGSWE",
    "JP": "FPCPITOTLZGJPN",
    "CH": "CLVMNACSCAB1GQCH", 
    "AU": "NAEXKP01AUQ661S",
    "NO": "FPCPITOTLZGNOR",
    "NZ": "FPCPITOTLZGNZL",
}

# --- Unemployment Rate (Monthly, OECD Harmonized) ---
# Pattern: LRHUTTTT + 2-letter code + M156S
MACRO_UNEMPLOYMENT = {
    "US": "LRHUTTTTUSM156S",
    "CA": "LRHUTTTTCAM156S",
    "GB": "LRHUTTTTGBM156S",
    "DE": "LRHUTTTTDEM156S",
    "FR": "LRHUTTTTFRM156S",
    "IT": "LRHUTTTTITM156S",
    "NL": "LRHUTTTTNLM156S",
    "BE": "LRHUTTTTBEM156S",
    "SE": "LRHUTTTTSEM156S",
    "JP": "LRHUTTTTJPM156S",
    "CH": "LRHUTTTTCHM156S",
    "AU": "LRHUTTTTAUM156S",
    "NO": "LRHUTTTTNOM156S",
    "NZ": "LRHUTTTTNZM156S",
}

# --- 10Y Government Bond Yield (Monthly, OECD) ---
# Pattern: IRLTLT01 + 2-letter code + M156N
MACRO_BOND_10Y = {
    "US": "IRLTLT01USM156N",
    "CA": "IRLTLT01CAM156N",
    "GB": "IRLTLT01GBM156N",
    "DE": "IRLTLT01DEM156N",
    "FR": "IRLTLT01FRM156N",
    "IT": "IRLTLT01ITM156N",
    "NL": "IRLTLT01NLM156N",
    "BE": "IRLTLT01BEM156N",
    "SE": "IRLTLT01SEM156N",
    "JP": "IRLTLT01JPM156N",
    "CH": "IRLTLT01CHM156N",
    "AU": "IRLTLT01AUM156N",
    "NO": "IRLTLT01NOM156N",
    "NZ": "IRLTLT01NZM156N",
}

# =============================================================================
# US GDP & FISCAL
# =============================================================================
US_GDP = {
    "GDP":       "nominal_gdp",                # Nominal GDP (Quarterly)
    "GDPC1":     "real_gdp",                   # Real GDP (Quarterly)
    "GDPPOT":    "real_potential_gdp",          # Real Potential GDP - CBO (Quarterly)
    "GFDEBTN":   "federal_debt",               # Gross Federal Debt (Quarterly)
    "GFDEGDQ188S": "federal_debt_pct_gdp",     # Gross Federal Debt as % of GDP (Quarterly)
    "NGDPSAXDCUSQ": "nominal_gdp_imf",         # Nominal GDP - IMF (Quarterly)
}


# =============================================================================
# US CPI
# =============================================================================
US_CPI = {
    "CPIAUCSL":              "cpi_all_items",          # CPI All Urban Consumers: All Items (Monthly)
    "CPILFESL":              "cpi_core",               # CPI All Items Less Food & Energy (Monthly)
    "MEDCPIM158SFRBCLE":     "median_cpi",             # Median CPI - Cleveland Fed (Monthly)
    "CORESTICKM159SFRBATL":  "sticky_cpi_less_food_energy",  # Sticky Price CPI Less Food & Energy (Monthly)
    "CPALTT01USM661S":       "cpi_all_items_oecd",     # CPI All Items Total - OECD (Monthly)
}


# =============================================================================
# US UNEMPLOYMENT
# =============================================================================
US_UNEMPLOYMENT = {
    "UNRATE":    "unemployment_rate",           # U-3 Headline (Monthly)
    "LNS14024887": "unemployment_16_24",        # Unemployment Rate 16-24 Yrs (Monthly)
    "NROU":      "noncyclical_unemployment",    # Noncyclical Rate of Unemployment - CBO (Quarterly)
    "LNS14024230": "unemployment_20_over",      # Unemployment Rate 20 Yrs & Over (Monthly)
    "UNEMPLOY":  "unemployment_level",          # Unemployment Level - thousands (Monthly)
}


# =============================================================================
# US INTEREST RATES
# =============================================================================
US_INTEREST_RATES = {
    "FEDFUNDS":              "fed_funds_effective",     # Federal Funds Effective Rate (Monthly)
    "IORB":                  "iorb_rate",               # Interest Rate on Reserve Balances (Daily→Monthly)
    "REAINTRATREARAT10Y":    "real_interest_rate_10y",  # 10-Year Real Interest Rate - Cleveland Fed (Monthly)
    "DGS1MO":                "treasury_1m",             # 1-Month Treasury (Daily→Monthly)
    "DGS3MO":                "treasury_3m",             # 3-Month Treasury (Daily→Monthly)
    "DGS1":                  "treasury_1y",             # 1-Year Treasury (Daily→Monthly)
    "DGS2":                  "treasury_2y",             # 2-Year Treasury (Daily→Monthly)
    "DGS5":                  "treasury_5y",             # 5-Year Treasury (Daily→Monthly)
    "DGS10":                 "treasury_10y",            # 10-Year Treasury (Daily→Monthly)
    "DGS30":                 "treasury_30y",            # 30-Year Treasury (Daily→Monthly)
    "T10Y2Y":                "yield_spread_10y2y",      # 10Y-2Y Spread (Daily→Monthly)
    "T10Y3M":                "yield_spread_10y3m",      # 10Y-3M Spread (Daily→Monthly)
    "DFEDTARU":              "fed_funds_upper",         # Fed Funds Target Upper Limit (Daily→Monthly)
    "DFEDTARL":              "fed_funds_lower",         # Fed Funds Target Lower Limit (Daily→Monthly)
    "BAMLH0A0HYM2":         "hy_oas_spread",           # ICE BofA High Yield OAS (Daily→Monthly)
    "AAA":                   "aaa_corporate_yield",     # Moody's AAA Corporate Bond Yield (Monthly)
    "BAA":                   "baa_corporate_yield",     # Moody's BAA Corporate Bond Yield (Monthly)
}


# =============================================================================
# HELPER — Build series_map for FREDFetcher
# =============================================================================

def build_g10_series_map(indicator_map, col_prefix):
    """
    Convert a G10 indicator dict into a FREDFetcher-compatible series_map.
    
    Example:
        build_g10_series_map(MACRO_GDP, "real_gdp")
        → {"GDPC1": "us_real_gdp", "NAEXKP01CAQ189S": "ca_real_gdp", ...}
    """
    return {
        series_id: f"{country.lower()}_{col_prefix}"
        for country, series_id in indicator_map.items()
    }
