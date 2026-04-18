import pandas as pd
from fredapi import Fred
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

API_KEY = "d24b966a5c95b4b3182c261ce74e1224"
fred = Fred(api_key=API_KEY)

# ============================================================
# CONFIGURATION
# ============================================================
# Change this to whatever FRED series you want
# Examples:
#   "SP500"     -> S&P 500 index
#   "DGS10"     -> 10-Year Treasury Yield
#   "FEDFUNDS"  -> Federal Funds Rate
#   "NASDAQCOM" -> NASDAQ Composite
#   "DJIA"      -> Dow Jones Industrial Average
#   "GDP"       -> Gross Domestic Product
#   "CPIAUCSL"  -> Consumer Price Index
#   "UNRATE"    -> Unemployment Rate
#   "DEXUSEU"   -> USD/EUR Exchange Rate
#   "GOLDAMGBD228NLBM" -> Gold Price (London)

SERIES_ID = "BAMLC0A0CM"

# ============================================================
# PULL THE RAW DATA
# ============================================================
# This pulls every available observation for the series.
# The result is a pandas Series with a DatetimeIndex.
raw_data = fred.get_series(SERIES_ID)

# Drop any NaN or missing values.
# FRED uses "." for missing data, fredapi converts those to NaN automatically.
raw_data = raw_data.dropna()

# Convert to a DataFrame so it's easier to work with
df = pd.DataFrame({
    "date": raw_data.index,
    "value": raw_data.values
})
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# ============================================================
# GRAB METADATA ABOUT THE SERIES
# ============================================================
# This tells you what the series actually is — title, units,
# frequency, seasonal adjustment, etc.
series_info = fred.get_series_info(SERIES_ID)

print("=" * 60)
print(f"Series ID:    {SERIES_ID}")
print(f"Title:        {series_info['title']}")
print(f"Units:        {series_info['units']}")
print(f"Frequency:    {series_info['frequency']}")
print(f"Seasonal Adj: {series_info['seasonal_adjustment']}")
print(f"First Date:   {df['date'].iloc[0].strftime('%Y-%m-%d')}")
print(f"Last Date:    {df['date'].iloc[-1].strftime('%Y-%m-%d')}")
print(f"Total Points: {len(df)}")
print(f"Latest Value: {df['value'].iloc[-1]:.2f}")
print("=" * 60)

# ============================================================
# DEFINE THE PERFORMANCE PERIODS
# ============================================================
# relativedelta handles months/years properly (accounts for
# different month lengths, leap years, etc.)
# timedelta only works for days/weeks.

periods = {
    "1 Week":    {"weeks": 1},
    "1 Month":   {"months": 1},
    "3 Months":  {"months": 3},
    "6 Months":  {"months": 6},
    "YTD":       "ytd",               # special case, handled separately
    "1 Year":    {"years": 1},
    "2 Years":   {"years": 2},
    "3 Years":   {"years": 3},
    "5 Years":   {"years": 5},
    "10 Years":  {"years": 10},
    "20 Years":  {"years": 20},
    "Max":       "max",               # special case, handled separately
}

# ============================================================
# HELPER: FIND THE CLOSEST AVAILABLE DATE
# ============================================================
# FRED data has gaps (weekends, holidays, missing days).
# So if you ask for "the value on 2024-01-01" and that's a
# holiday, there's no data point. This function finds the
# closest date that actually has data, looking backward.
#
# tolerance_days controls how far back we're willing to look.
# If the closest data point is more than tolerance_days away,
# we consider it unavailable.

def get_closest_value(df, target_date, tolerance_days=10):
    """
    Given a target date, find the closest observation on or
    before that date within the tolerance window.
    
    Returns (date, value) or (None, None) if nothing found.
    """
    # Filter to rows on or before the target date
    mask = df["date"] <= target_date
    subset = df[mask]
    
    if subset.empty:
        return None, None
    
    # Get the most recent row before/on the target date
    closest_row = subset.iloc[-1]
    
    # Check if it's within tolerance
    days_diff = (target_date - closest_row["date"]).days
    if days_diff > tolerance_days:
        return None, None
    
    return closest_row["date"], closest_row["value"]


# ============================================================
# COMPUTE PERFORMANCE FOR EACH PERIOD
# ============================================================
latest_date = df["date"].iloc[-1]
latest_value = df["value"].iloc[-1]

print("\nPERFORMANCE SUMMARY")
print("-" * 60)
print(f"{'Period':<12} {'Start Date':<12} {'Start Val':>12} {'End Val':>12} {'Return':>10}")
print("-" * 60)

results = []

for label, offset in periods.items():
    
    # --- Handle special cases ---
    
    if offset == "ytd":
        # YTD = from the last trading day of the previous year
        year_start = datetime(latest_date.year, 1, 1)
        # Go back one day to get Dec 31 of previous year,
        # then find closest trading day
        target_date = year_start - timedelta(days=1)
        past_date, past_value = get_closest_value(df, target_date)
        
    elif offset == "max":
        # Max = from the very first data point
        past_date = df["date"].iloc[0]
        past_value = df["value"].iloc[0]
        
    else:
        # --- Standard period ---
        # Use relativedelta for months/years, timedelta for weeks/days
        if "weeks" in offset:
            target_date = latest_date - timedelta(weeks=offset["weeks"])
        elif "months" in offset:
            target_date = latest_date - relativedelta(months=offset["months"])
        elif "years" in offset:
            target_date = latest_date - relativedelta(years=offset["years"])
        
        past_date, past_value = get_closest_value(df, target_date)
    
    # --- Calculate the return ---
    
    if past_date is not None and past_value is not None and past_value != 0:
        pct_return = ((latest_value - past_value) / past_value) * 100
        
        results.append({
            "period": label,
            "start_date": past_date,
            "start_value": past_value,
            "end_date": latest_date,
            "end_value": latest_value,
            "pct_return": pct_return
        })
        
        print(f"{label:<12} {past_date.strftime('%Y-%m-%d'):<12} {past_value:>12.2f} {latest_value:>12.2f} {pct_return:>+10.2f}%")
    else:
        # Not enough history for this period
        results.append({
            "period": label,
            "start_date": None,
            "start_value": None,
            "end_date": latest_date,
            "end_value": latest_value,
            "pct_return": None
        })
        
        print(f"{label:<12} {'N/A':<12} {'N/A':>12} {latest_value:>12.2f} {'N/A':>10}")

print("-" * 60)


# ============================================================
# ANNUALIZED RETURNS (for periods > 1 year)
# ============================================================
# Simple percentage return doesn't tell the full story for
# multi-year periods. A 100% return over 10 years is very
# different from 100% over 1 year.
#
# Annualized return formula:
#   annualized = ((end / start) ^ (1 / years)) - 1
#
# This gives you the equivalent yearly return if the growth
# had been perfectly steady.

print("\nANNUALIZED RETURNS (periods > 1 year)")
print("-" * 40)

for r in results:
    if r["start_date"] is None or r["pct_return"] is None:
        continue
    
    # Calculate the number of years between start and end
    days_held = (r["end_date"] - r["start_date"]).days
    years_held = days_held / 365.25
    
    if years_held < 1.0:
        continue  # skip sub-1-year periods
    
    total_return_decimal = r["pct_return"] / 100  # e.g., 0.50 for 50%
    
    # Annualized return
    annualized = ((1 + total_return_decimal) ** (1 / years_held)) - 1
    annualized_pct = annualized * 100
    
    print(f"{r['period']:<12} {annualized_pct:>+8.2f}% per year  (over {years_held:.1f} years)")

print("-" * 40)


# ============================================================
# DRAWDOWN FROM ALL-TIME HIGH
# ============================================================
# This tells you how far the current value is from the
# highest value the series has ever reached.

all_time_high = df["value"].max()
all_time_high_date = df.loc[df["value"].idxmax(), "date"]
drawdown = ((latest_value - all_time_high) / all_time_high) * 100

print(f"\nALL-TIME HIGH")
print(f"  Peak Value: {all_time_high:.2f} on {all_time_high_date.strftime('%Y-%m-%d')}")
print(f"  Current:    {latest_value:.2f}")
print(f"  Drawdown:   {drawdown:+.2f}%")


# ============================================================
# VOLATILITY (ANNUALIZED STANDARD DEVIATION)
# ============================================================
# Volatility = how much the daily returns bounce around.
# Higher volatility = more risk.
#
# We compute daily percentage changes, then take the standard
# deviation, then annualize it by multiplying by sqrt(252)
# because there are roughly 252 trading days in a year.

daily_returns = df["value"].pct_change().dropna()

vol_1y = daily_returns.tail(252).std() * (252 ** 0.5) * 100   # last 1 year
vol_3y = daily_returns.tail(756).std() * (252 ** 0.5) * 100   # last 3 years
vol_all = daily_returns.std() * (252 ** 0.5) * 100            # all time

print(f"\nANNUALIZED VOLATILITY")
print(f"  1-Year:  {vol_1y:.2f}%")
print(f"  3-Year:  {vol_3y:.2f}%")
print(f"  All-Time: {vol_all:.2f}%")


# ============================================================
# EXPORT TO CSV (OPTIONAL)
# ============================================================
# If you want to save the results for later use

results_df = pd.DataFrame(results)
results_df.to_csv(f"{SERIES_ID}_performance.csv", index=False)
print(f"\nResults saved to {SERIES_ID}_performance.csv")

# Also save the raw data if you want it
df.to_csv(f"{SERIES_ID}_raw_data.csv", index=False)
print(f"Raw data saved to {SERIES_ID}_raw_data.csv")