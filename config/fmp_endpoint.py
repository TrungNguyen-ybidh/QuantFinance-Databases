fmp_endpoints = [
    # --- Company Profile --- 
    {
        "endpoint": "profile",
        "params": {}

    },

    # --- Quote ---
    {
        "endpoint": "quote",
        "params": {}
    },

    # --- Core Statements ---
    {
        "endpoint": "income-statement",
        "params": {"period": "quarter", "limit": 30}
    },
    {
        "endpoint": "balance-sheet-statement",
        "params": {"period": "quarter", "limit": 30}
    },
    {
        "endpoint": "cash-flow-statement",
        "params": {"period": "quarter", "limit": 30}
    },

    # --- Metrics & Ratios ---
    {
        "endpoint": "key-metrics",
        "params": {"limit": 30}
    },
    {
        "endpoint": "ratios",
        "params": { "limit": 30}
    },

     {
        "endpoint": "financial-scores",
        "params": {}
    },

    # --- Valuation ---
    {
        "endpoint": "enterprise-values",
        "params": {"period": "annual", "limit": 30}
    },
    {
        "endpoint": "discounted-cash-flow",
        "params": {}
    },
    {
        "endpoint": "levered-discounted-cash-flow",
        "params": {}
    },

    # --- Growth ---
    {
        "endpoint": "income-statement-growth",
        "params": {"period": "annual", "limit": 30}
    },
    {
        "endpoint": "balance-sheet-statement-growth",
        "params": {"period": "annual", "limit": 30}
    },
    {
        "endpoint": "cash-flow-statement-growth",
        "params": {"period": "annual", "limit": 30}
    },
    {
        "endpoint": "financial-growth",
        "params": {"period": "annual", "limit": 30}
    },

    # --- Segmentation ---
    {
        "endpoint": "revenue-product-segmentation",
        "params": {"period": "annual", "limit": 30}
    },
    {
        "endpoint": "revenue-geographic-segmentation",
        "params": {"period": "annual", "limit": 30}
    },

    # --- Dividends ---
    {
        "endpoint": "dividends",
        "params": {"limit": 20}
    },

    # --- Analyst --- 
     {
        "endpoint": "analyst-estimates",
        "params": {"period": "annual", "limit": 10, "page":0}
    },

     {
        "endpoint": "ratings-historical",
        "params": {"limit": 1}
    },
]

fmp_update_endpoints = [
    # --- Quote (snapshot, no history) ---
    {
        "endpoint": "quote",
        "params": {}
    },

    # --- Core Statements ---
    # Quarterly: limit=4 grabs ~1 year of quarters, enough to catch
    # the latest release + any prior-quarter restatements
    {
        "endpoint": "income-statement",
        "params": {"period": "quarter", "limit": 1}
    },
    {
        "endpoint": "balance-sheet-statement",
        "params": {"period": "quarter", "limit": 1}
    },
    {
        "endpoint": "cash-flow-statement",
        "params": {"period": "quarter", "limit": 1}
    },

    # --- Metrics & Ratios ---
    # These default to annual when no period is specified.
    # limit=2 catches the latest + one prior (for revision checks)
    {
        "endpoint": "key-metrics",
        "params": {"limit": 2}
    },
    {
        "endpoint": "ratios",
        "params": {"limit": 2}
    },

    # --- Financial Scores (snapshot, no history) ---
    {
        "endpoint": "financial-scores",
        "params": {}
    },

    # --- Valuation ---
    # Annual: limit=2 for latest + prior year
    {
        "endpoint": "enterprise-values",
        "params": {"period": "annual", "limit": 1}
    },
    # DCF endpoints are point-in-time snapshots
    {
        "endpoint": "discounted-cash-flow",
        "params": {}
    },
    {
        "endpoint": "levered-discounted-cash-flow",
        "params": {}
    },

    # --- Growth ---
    # Annual: limit=2 for latest + prior year
    {
        "endpoint": "income-statement-growth",
        "params": {"period": "annual", "limit": 1}
    },
    {
        "endpoint": "balance-sheet-statement-growth",
        "params": {"period": "annual", "limit": 1}
    },
    {
        "endpoint": "cash-flow-statement-growth",
        "params": {"period": "annual", "limit": 1}
    },
    {
        "endpoint": "financial-growth",
        "params": {"period": "annual", "limit": 1}
    },

    # --- Segmentation ---
    # Annual: limit=2 for latest + prior year
    {
        "endpoint": "revenue-product-segmentation",
        "params": {"period": "annual", "limit": 1}
    },
    {
        "endpoint": "revenue-geographic-segmentation",
        "params": {"period": "annual", "limit": 1}
    },

    # --- Dividends ---
    # limit=4 covers roughly the last year of quarterly dividends
    {
        "endpoint": "dividends",
        "params": {"limit": 1}
    },

    # --- Analyst ---
    {
        "endpoint": "analyst-estimates",
        "params": {"period": "annual", "limit": 1, "page": 0}
    },

    # Ratings: already limit=1, perfect for updates
    {
        "endpoint": "ratings-historical",
        "params": {"limit": 1}
    },
]