schema_map = {
    "profile.csv": {
        "primary_key": ["symbol"],
        "keep": [
            "symbol", "companyName", "price", "marketCap", "beta",
            "sector", "industry", "country", "cik", "isin", "cusip",
            "exchange", "ceo", "fullTimeEmployees", "ipoDate", "description"
        ],
        "drop": [
            "lastDividend", "range", "change", "changePercentage",
            "volume", "averageVolume", "currency", "exchangeFullName",
            "website", "phone", "address", "city", "state", "zip",
            "image", "defaultImage", "isEtf", "isActivelyTrading",
            "isAdr", "isFund"
        ]
    },

    "quote.csv": {
        "primary_key": ["symbol"],
        "keep": [
            "symbol", "name", "price", "marketCap",
            "yearHigh", "yearLow", "priceAvg50", "priceAvg200", "volume"
        ],
        "drop": [
            "changePercentage", "change", "dayLow", "dayHigh",
            "exchange", "open", "previousClose", "timestamp"
        ]
    },

    "financial-scores.csv": {
        "primary_key": ["symbol"],
        "keep": [
            "symbol", "altmanZScore", "piotroskiScore",
            "workingCapital", "totalAssets", "retainedEarnings",
            "ebit", "marketCap", "totalLiabilities", "revenue"
        ],
        "drop": [
            "reportedCurrency"
        ]
    },

    "discounted-cash-flow.csv": {
        "primary_key": ["symbol", "date"],
        "keep": [
            "symbol", "date", "dcf", "Stock Price"
        ],
        "drop": []
    },

    "levered-discounted-cash-flow.csv": {
        "primary_key": ["symbol", "date"],
        "keep": [
            "symbol", "date", "dcf", "Stock Price"
        ],
        "drop": []
    },

    # ======================== TIME-SERIES STATEMENTS ========================
    # PK: (symbol, date, period)

    "income-statement.csv": {
        "primary_key": ["symbol", "date", "period"],
        "keep": [
            "date", "symbol", "fiscalYear", "period",
            "revenue", "costOfRevenue", "grossProfit",
            "researchAndDevelopmentExpenses",
            "sellingGeneralAndAdministrativeExpenses",
            "operatingExpenses", "operatingIncome",
            "interestIncome", "interestExpense",
            "depreciationAndAmortization",
            "ebitda", "ebit",
            "incomeBeforeTax", "incomeTaxExpense", "netIncome",
            "eps", "epsDiluted",
            "weightedAverageShsOut", "weightedAverageShsOutDil"
        ],
        "drop": [
            "reportedCurrency", "cik", "filingDate", "acceptedDate",
            "generalAndAdministrativeExpenses",
            "sellingAndMarketingExpenses", "otherExpenses",
            "costAndExpenses", "netInterestIncome",
            "nonOperatingIncomeExcludingInterest",
            "totalOtherIncomeExpensesNet",
            "netIncomeFromContinuingOperations",
            "netIncomeFromDiscontinuedOperations",
            "otherAdjustmentsToNetIncome",
            "netIncomeDeductions", "bottomLineNetIncome"
        ]
    },

    "balance-sheet-statement.csv": {
        "primary_key": ["symbol", "date", "period"],
        "keep": [
            "date", "symbol", "fiscalYear", "period",
            "cashAndCashEquivalents", "shortTermInvestments",
            "cashAndShortTermInvestments",
            "netReceivables", "inventory",
            "totalCurrentAssets",
            "propertyPlantEquipmentNet",
            "goodwill", "intangibleAssets",
            "longTermInvestments", "taxAssets",
            "totalNonCurrentAssets", "totalAssets",
            "accountPayables", "accruedExpenses",
            "shortTermDebt", "deferredRevenue",
            "totalCurrentLiabilities",
            "longTermDebt",
            "totalNonCurrentLiabilities", "totalLiabilities",
            "retainedEarnings", "additionalPaidInCapital",
            "totalStockholdersEquity", "totalEquity",
            "totalDebt", "netDebt"
        ],
        "drop": [
            "reportedCurrency", "cik", "filingDate", "acceptedDate",
            "accountsReceivables", "otherReceivables",
            "prepaids", "otherCurrentAssets",
            "goodwillAndIntangibleAssets",
            "otherNonCurrentAssets", "otherAssets",
            "totalPayables", "otherPayables",
            "capitalLeaseObligationsCurrent", "taxPayables",
            "otherCurrentLiabilities",
            "capitalLeaseObligationsNonCurrent",
            "deferredRevenueNonCurrent",
            "deferredTaxLiabilitiesNonCurrent",
            "otherNonCurrentLiabilities",
            "otherLiabilities", "capitalLeaseObligations",
            "treasuryStock", "preferredStock", "commonStock",
            "accumulatedOtherComprehensiveIncomeLoss",
            "otherTotalStockholdersEquity",
            "minorityInterest",
            "totalLiabilitiesAndTotalEquity",
            "totalInvestments"
        ]
    },

    "cash-flow-statement.csv": {
        "primary_key": ["symbol", "date", "period"],
        "keep": [
            "date", "symbol", "fiscalYear", "period",
            "netIncome", "depreciationAndAmortization",
            "stockBasedCompensation", "deferredIncomeTax",
            "changeInWorkingCapital",
            "netCashProvidedByOperatingActivities",
            "investmentsInPropertyPlantAndEquipment",
            "acquisitionsNet",
            "purchasesOfInvestments", "salesMaturitiesOfInvestments",
            "netCashProvidedByInvestingActivities",
            "netDebtIssuance",
            "commonStockRepurchased", "netDividendsPaid",
            "netCashProvidedByFinancingActivities",
            "operatingCashFlow", "capitalExpenditure", "freeCashFlow",
            "incomeTaxesPaid", "interestPaid"
        ],
        "drop": [
            "reportedCurrency", "cik", "filingDate", "acceptedDate",
            "accountsReceivables", "inventory", "accountsPayables",
            "otherWorkingCapital", "otherNonCashItems",
            "otherInvestingActivities",
            "longTermNetDebtIssuance", "shortTermNetDebtIssuance",
            "netStockIssuance", "netCommonStockIssuance",
            "commonStockIssuance", "netPreferredStockIssuance",
            "commonDividendsPaid", "preferredDividendsPaid",
            "otherFinancingActivities",
            "effectOfForexChangesOnCash", "netChangeInCash",
            "cashAtEndOfPeriod", "cashAtBeginningOfPeriod"
        ]
    },

    # ======================== TIME-SERIES METRICS & RATIOS ========================
    # PK: (symbol, date, period)

    "key-metrics.csv": {
        "primary_key": ["symbol", "date", "period"],
        "keep": [
            "symbol", "date", "fiscalYear", "period",
            "marketCap", "enterpriseValue",
            "evToSales", "evToEBITDA", "evToFreeCashFlow",
            "netDebtToEBITDA", "currentRatio", "incomeQuality",
            "grahamNumber",
            "workingCapital", "investedCapital",
            "returnOnAssets", "returnOnEquity",
            "returnOnInvestedCapital", "returnOnCapitalEmployed",
            "earningsYield", "freeCashFlowYield",
            "researchAndDevelopementToRevenue",
            "stockBasedCompensationToRevenue",
            "capexToRevenue",
            "daysOfSalesOutstanding", "daysOfPayablesOutstanding",
            "daysOfInventoryOutstanding", "cashConversionCycle",
            "freeCashFlowToEquity", "freeCashFlowToFirm",
            "tangibleAssetValue", "netCurrentAssetValue"
        ],
        "drop": [
            "reportedCurrency",
            "evToOperatingCashFlow",
            "grahamNetNet",
            "taxBurden", "interestBurden",
            "operatingReturnOnAssets", "returnOnTangibleAssets",
            "capexToOperatingCashFlow", "capexToDepreciation",
            "salesGeneralAndAdministrativeToRevenue",
            "intangiblesToTotalAssets",
            "averageReceivables", "averagePayables", "averageInventory",
            "operatingCycle"
        ]
    },

    "ratios.csv": {
        "primary_key": ["symbol", "date", "period"],
        "keep": [
            "symbol", "date", "fiscalYear", "period",
            # --- Margins ---
            "grossProfitMargin", "ebitMargin", "ebitdaMargin",
            "operatingProfitMargin", "netProfitMargin",
            # --- Turnover ---
            "receivablesTurnover", "payablesTurnover",
            "inventoryTurnover", "fixedAssetTurnover", "assetTurnover",
            # --- Liquidity ---
            "currentRatio", "quickRatio",
            # --- Leverage ---
            "debtToEquityRatio", "debtToAssetsRatio",
            "financialLeverageRatio", "interestCoverageRatio",
            # --- Valuation ---
            "priceToEarningsRatio", "priceToBookRatio",
            "priceToSalesRatio", "priceToFreeCashFlowRatio",
            "enterpriseValueMultiple",
            # --- Cash flow quality ---
            "operatingCashFlowSalesRatio",
            "freeCashFlowOperatingCashFlowRatio",
            # --- Dividend ---
            "dividendPayoutRatio", "dividendYield",
            # --- Tax ---
            "effectiveTaxRate"
        ],
        "drop": [
            "reportedCurrency",
            # --- Redundant margins ---
            "pretaxProfitMargin",
            "continuousOperationsProfitMargin",
            "bottomLineProfitMargin",
            # --- Redundant leverage ---
            "debtToCapitalRatio", "longTermDebtToCapitalRatio",
            "solvencyRatio", "cashRatio",
            # --- Redundant valuation ---
            "priceToEarningsGrowthRatio",
            "forwardPriceToEarningsGrowthRatio",
            "priceToOperatingCashFlowRatio",
            "priceToFairValue", "debtToMarketCap",
            # --- Redundant coverage ---
            "workingCapitalTurnoverRatio",
            "operatingCashFlowRatio",
            "debtServiceCoverageRatio",
            "shortTermOperatingCashFlowCoverageRatio",
            "operatingCashFlowCoverageRatio",
            "capitalExpenditureCoverageRatio",
            "dividendPaidAndCapexCoverageRatio",
            # --- Per-share (derivable from statements) ---
            "revenuePerShare", "netIncomePerShare",
            "interestDebtPerShare", "cashPerShare",
            "bookValuePerShare", "tangibleBookValuePerShare",
            "shareholdersEquityPerShare",
            "operatingCashFlowPerShare", "capexPerShare",
            "freeCashFlowPerShare",
            # --- DuPont sub-components ---
            "netIncomePerEBT", "ebtPerEbit",
            # --- Redundant ---
            "dividendYieldPercentage", "dividendPerShare"
        ]
    },

    "financial-growth.csv": {
        "primary_key": ["symbol", "date", "period"],
        "keep": [
            "symbol", "date", "fiscalYear", "period",
            "revenueGrowth", "grossProfitGrowth",
            "operatingIncomeGrowth", "netIncomeGrowth",
            "epsdilutedGrowth", "ebitdaGrowth",
            "operatingCashFlowGrowth", "freeCashFlowGrowth",
            # --- Multi-year CAGRs (not easily derivable) ---
            "threeYRevenueGrowthPerShare",
            "fiveYRevenueGrowthPerShare",
            "tenYRevenueGrowthPerShare",
            "threeYNetIncomeGrowthPerShare",
            "fiveYNetIncomeGrowthPerShare",
            "tenYNetIncomeGrowthPerShare",
            "threeYOperatingCFGrowthPerShare",
            "fiveYOperatingCFGrowthPerShare",
            "tenYOperatingCFGrowthPerShare"
        ],
        "drop": [
            "reportedCurrency",
            "ebitgrowth", "epsgrowth",
            "weightedAverageSharesGrowth",
            "weightedAverageSharesDilutedGrowth",
            "dividendsPerShareGrowth",
            "receivablesGrowth", "inventoryGrowth",
            "assetGrowth", "bookValueperShareGrowth",
            "debtGrowth", "rdexpenseGrowth", "sgaexpensesGrowth",
            "growthCapitalExpenditure",
            "tenYShareholdersEquityGrowthPerShare",
            "fiveYShareholdersEquityGrowthPerShare",
            "threeYShareholdersEquityGrowthPerShare",
            "tenYDividendperShareGrowthPerShare",
            "fiveYDividendperShareGrowthPerShare",
            "threeYDividendperShareGrowthPerShare",
            "tenYBottomLineNetIncomeGrowthPerShare",
            "fiveYBottomLineNetIncomeGrowthPerShare",
            "threeYBottomLineNetIncomeGrowthPerShare"
        ]
    },

    "enterprise-values.csv": {
        "primary_key": ["symbol", "date"],
        "keep": [
            "symbol", "date", "stockPrice", "numberOfShares",
            "marketCapitalization",
            "minusCashAndCashEquivalents", "addTotalDebt",
            "enterpriseValue"
        ],
        "drop": []
    },

    # ======================== EVENT / IRREGULAR TIME-SERIES ========================
    # PK: (symbol, date)

    "analyst-estimates.csv": {
        "primary_key": ["symbol", "date"],
        "keep": [
            "symbol", "date",
            "revenueAvg", "ebitdaAvg", "netIncomeAvg", "epsAvg",
            "numAnalystsRevenue", "numAnalystsEps"
        ],
        "drop": [
            "revenueLow", "revenueHigh",
            "ebitdaLow", "ebitdaHigh",
            "ebitLow", "ebitHigh", "ebitAvg",
            "netIncomeLow", "netIncomeHigh",
            "sgaExpenseLow", "sgaExpenseHigh", "sgaExpenseAvg",
            "epsHigh", "epsLow"
        ]
    },

    "dividends.csv": {
        "primary_key": ["symbol", "date"],
        "keep": [
            "symbol", "date",
            "adjDividend", "dividend", "yield", "frequency"
        ],
        "drop": [
            "recordDate", "paymentDate", "declarationDate"
        ]
    },

    "ratings-historical.csv": {
        "primary_key": ["symbol", "date"],
        "keep": [
            "symbol", "date", "rating", "overallScore",
            "discountedCashFlowScore", "returnOnEquityScore",
            "returnOnAssetsScore", "debtToEquityScore",
            "priceToEarningsScore", "priceToBookScore"
        ],
        "drop": []
    },

    # ======================== SEGMENTATION ========================
    # PK: (symbol, date)
    # NOTE: parse the 'data' JSON column into individual segment columns

    "revenue-geographic-segmentation.csv": {
        "primary_key": ["symbol", "date"],
        "keep": [
            "symbol", "date", "fiscalYear", "data"
        ],
        "drop": [
            "period", "reportedCurrency"
        ],
        "note": "Parse 'data' dict into columns: CHINA, TAIWAN, UNITED_STATES, OTHER_AMERICAS, etc."
    },

    "revenue-product-segmentation.csv": {
        "primary_key": ["symbol", "date"],
        "keep": [
            "symbol", "date", "fiscalYear", "data"
        ],
        "drop": [
            "period", "reportedCurrency"
        ],
        "note": "Parse 'data' dict into columns: Data_Center, Gaming, Automotive, Professional_Visualization, OEM_And_Other"
    },
}