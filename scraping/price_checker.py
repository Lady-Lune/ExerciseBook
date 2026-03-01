from pathlib import Path
import pandas as pd


COMBINED_FILE = Path(__file__).parent / "combined_prices.csv"


def check_price_drops():
    """Check for significant price drops between the last two dates."""
    # Check if file exists
    if not COMBINED_FILE.exists():
        print(f"Error: {COMBINED_FILE} not found.")
        quit()
    
    # Read the combined prices CSV
    df = pd.read_csv(COMBINED_FILE)
    
    # Get the last two date columns (skip id and name)
    date_columns = df.columns[2:]
    if len(date_columns) < 2:
        print("Not enough date columns to compare prices.")
        quit()
    
    old_date = date_columns[-2]
    new_date = date_columns[-1]
    
    # Calculate difference
    df["price_diff"] = df[new_date].astype(float) - df[old_date].astype(float)
    df["pct_change"] = (df["price_diff"] / df[old_date].astype(float)) * 100
    
    # Find items with price drop of 10% or more
    drops = df[df["pct_change"] <= -10].copy()
    
    if drops.empty:
        print("No significant price drops found.")
    else:
        print(f"\n{'='*60}")
        print(f"Items with 10%+ price drop ({old_date} → {new_date}):")
        print(f"{'='*60}\n")
        
        for _, row in drops.iterrows():
            print(f"📉 {row['name']}")
            print(f"   Old price: ${row[old_date]:.2f}")
            print(f"   New price: ${row[new_date]:.2f}")
            print(f"   Change: {row['pct_change']:.1f}%\n")
    
    return df


if __name__ == "__main__":
    check_price_drops()
