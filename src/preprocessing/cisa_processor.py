"""
CISA KEV Data Processing Module.

Loads the original CISA catalog, validates its structure
and generates a clean tabular dataset.
"""

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "cisa_kev.json"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "cisa_kev_processed.csv"


def load_catalog() -> dict:
    """Load the original CISA catalog."""

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"CISA catalog not found: {RAW_FILE}"
        )

    with RAW_FILE.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    if not isinstance(catalog.get("vulnerabilities"), list):
        raise ValueError("Invalid vulnerabilities structure.")

    return catalog


def create_dataframe(catalog: dict) -> pd.DataFrame:
    """Convert vulnerabilities into a DataFrame."""

    df = pd.DataFrame(catalog["vulnerabilities"])

    if df.empty:
        raise ValueError("The catalog contains no vulnerabilities.")

    return df

def analyze_data(df: pd.DataFrame) -> None:
    """Display basic data quality information."""

    print("\n========== DATA QUALITY REPORT ==========")

    print(f"Total records: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    print("\nMissing values:")
    print(df.isnull().sum())

    # Check duplicated vulnerability identifiers
    duplicated_cves = df["cveID"].duplicated().sum()

    print("\nDuplicate CVE identifiers:")
    print(duplicated_cves)

    # Check duplicated complete records using CVE identifiers
    print("\nUnique CVE identifiers:")
    print(df["cveID"].nunique())

    print("\nAvailable columns:")
    print(list(df.columns))

    print("==========================================\n")

def process_catalog() -> pd.DataFrame:
    """Execute the complete processing workflow."""

    print("Loading CISA catalog...")

    catalog = load_catalog()

    print("Creating DataFrame...")

    df = create_dataframe(catalog)

    analyze_data(df)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Processed dataset saved: {OUTPUT_FILE}")
    print(f"Final record count: {len(df)}")

    return df


def main() -> None:
    try:
        process_catalog()
        print("\nCISA DATA PROCESSING: SUCCESS")

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Processing error: {error}")


if __name__ == "__main__":
    main()