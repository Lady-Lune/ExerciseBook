import re
from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).parent / "data" / "daily"
OUTPUT_FILE = Path(__file__).parent / "combined_prices.csv"


def get_json_files() -> list[tuple[str, Path]]:
    """Get all JSON listing files sorted by date."""
    pattern = re.compile(r"listing-(\d{4}-\d{2}-\d{2})\.json")
    files = []

    for f in DATA_DIR.glob("listing-*.json"):
        match = pattern.match(f.name)
        if match:
            date_str = match.group(1)
            files.append((date_str, f))

    # Sort by date
    files.sort(key=lambda x: x[0])
    return files


def create_combined_file(date_str: str, file_path: Path) -> pd.DataFrame:
    """Create initial combined CSV from the first JSON file."""
    df = pd.read_json(file_path)
    combined_df = df[["id", "name", "price"]].copy()
    combined_df.columns = ["id", "name", date_str]
    combined_df[date_str] = combined_df[date_str].astype(str).str.replace(r"[^\d.]", "", regex=True).astype(float)
    combined_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Created combined file with date: {date_str}")
    return combined_df


def add_new_date(combined_df: pd.DataFrame, file_path: Path, date_str: str) -> pd.DataFrame:
    """Add new date column to combined DataFrame."""
    df_new = pd.read_json(file_path)
    df_new = df_new[["id", "price"]]
    df_new.columns = ["id", date_str]
    df_new[date_str] = df_new[date_str].astype(str).str.replace(r"[^\d.]", "", regex=True).astype(float)
    combined = combined_df.merge(df_new, on="id", how="left")
    print("\n", "*"*60,"\n", combined.head(), "\n", "*"*60)
    return combined


def update_combined_file():
    """Main function to update combined prices CSV with new dates."""
    json_files = get_json_files()
    
    if not json_files:
        print("No JSON files found.")
        return
    
    scraped_info = dict(json_files)
    
    # Check if combined file exists
    if not OUTPUT_FILE.exists():
        # Create combined file with the first JSON file
        first_date, first_file = json_files[0]
        combined = create_combined_file(first_date, first_file)
        scraped_dates = list(scraped_info.keys())[1:]  # Skip first since we just added it
    else:
        # Read existing combined file
        combined = pd.read_csv(OUTPUT_FILE)
        existing_dates = set(combined.columns[2:])  # Skip id and name
        scraped_dates = [d for d in scraped_info.keys() if d not in existing_dates]
    
    # Add missing dates
    for date in scraped_dates:
        print(f"Adding missing date: {date}")
        combined = add_new_date(combined, scraped_info[date], date)
    
    # Save updated combined file
    if scraped_dates:
        combined.to_csv(OUTPUT_FILE, index=False)
        print(f"Updated combined file with {len(scraped_dates)} new date(s).")
    else:
        print("No new dates to add.")
    
    return combined


if __name__ == "__main__":
    print(update_combined_file().head())
    print("\n", "="*60, "\n", "Combined prices updated successfully!", "\n", "="*60)



