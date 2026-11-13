"""
CISA KEV Feature Engineering Module.

Transforms processed vulnerability records into
analytical features for future Machine Learning models.
"""

from pathlib import Path
import ast

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "cisa_kev_processed.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = OUTPUT_DIR / "cisa_kev_features.csv"
CWE_OUTPUT_FILE = OUTPUT_DIR / "cisa_cwe_features_linked.csv"

# Set a fixed reference date for reproducible experiments.
REFERENCE_DATE = pd.Timestamp.now(tz="UTC").normalize()


def load_data() -> pd.DataFrame:
    """Load the processed CISA dataset."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("The processed dataset is empty.")

    required_columns = [
        "cveID",
        "vendorProject",
        "product",
        "dateAdded",
        "dueDate",
        "knownRansomwareCampaignUse",
        "forensicTriage",
        "cwes",
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    return df


def create_features(
    df: pd.DataFrame,
    reference_date: pd.Timestamp = REFERENCE_DATE
) -> pd.DataFrame:
    """Generate temporal, categorical and contextual features."""

    df = df.copy()

    # Convert dates to UTC
    df["dateAdded"] = pd.to_datetime(
        df["dateAdded"], errors="coerce", utc=True
    )

    df["dueDate"] = pd.to_datetime(
        df["dueDate"], errors="coerce", utc=True
    )

    reference_date = pd.Timestamp(reference_date)

    if reference_date.tzinfo is None:
        reference_date = reference_date.tz_localize("UTC")
    else:
        reference_date = reference_date.tz_convert("UTC")

    reference_date = reference_date.normalize()

    # Temporal features
    df["days_since_added"] = (
        reference_date - df["dateAdded"]
    ).dt.days

    df["days_until_due"] = (
        df["dueDate"] - reference_date
    ).dt.days

    df["added_year"] = df["dateAdded"].dt.year.astype("Int64")
    df["added_month"] = df["dateAdded"].dt.month.astype("Int64")
    df["added_quarter"] = df["dateAdded"].dt.quarter.astype("Int64")

    # Deadline indicators
    df["deadline_overdue"] = (
        df["days_until_due"] < 0
    ).astype("int8")

    df["days_past_due"] = (
        -df["days_until_due"]
    ).clip(lower=0)

    df["deadline_urgency"] = pd.cut(
        df["days_until_due"],
        bins=[-float("inf"), -1, 30, float("inf")],
        labels=["Overdue", "Due_soon", "Due_later"]
    )

    # Vulnerability age categories
    df["vulnerability_age_category"] = pd.cut(
        df["days_since_added"],
        bins=[-float("inf"), 90, 365, float("inf")],
        labels=["Recent", "Intermediate", "Old"]
    )

    age_mapping = {
        "Recent": 0,
        "Intermediate": 1,
        "Old": 2
    }

    df["vulnerability_age_encoded"] = (
        df["vulnerability_age_category"]
        .map(age_mapping)
        .astype("Int8")
    )

    # Ransomware binary encoding
    ransomware_mapping = {
        "Known": 1,
        "Unknown": 0
    }

    df["ransomware_known"] = (
        df["knownRansomwareCampaignUse"]
        .map(ransomware_mapping)
        .astype("Int8")
    )

    # Forensic triage binary encoding
    forensic_mapping = {
        "Yes": 1,
        "No": 0
    }

    df["has_forensic_triage"] = (
        df["forensicTriage"]
        .str.strip()
        .map(forensic_mapping)
        .astype("Int8")
    )

    # Additional explicit binary feature names
    df["ransomware_encoded"] = df["ransomware_known"]
    df["forensic_triage_encoded"] = df["has_forensic_triage"]

    # Experimental frequency encoding
    # Descriptive only: do not use directly in model training.
    vendor_frequency = df["vendorProject"].value_counts()
    product_frequency = df["product"].value_counts()

    df["vendor_frequency"] = (
        df["vendorProject"].map(vendor_frequency)
    )

    df["product_frequency"] = (
        df["product"].map(product_frequency)
    )

    return df


def create_cwe_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """Create a separate multilabel CWE feature matrix."""

    df = df.copy()

    def parse_cwe(value):
        if pd.isna(value):
            return []
        parsed = ast.literal_eval(value) if isinstance(value, str) else value
        if not isinstance(parsed, list):
            raise ValueError("Invalid CWE list format.")
        return parsed

    cwe_lists = df["cwes"].apply(parse_cwe)

    mlb = MultiLabelBinarizer()
    encoded = mlb.fit_transform(cwe_lists)

    encoded_df = pd.DataFrame(
        encoded,
        columns=[f"cwe_{cwe}" for cwe in mlb.classes_],
        index=df.index
    )

    linked_df = pd.concat(
        [df[["cveID"]].copy(), encoded_df],
        axis=1
    )

    return linked_df


def save_features(
    df: pd.DataFrame,
    cwe_df: pd.DataFrame
) -> None:
    """Save the main and CWE feature datasets."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    cwe_df.to_csv(
        CWE_OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Main feature dataset saved: {OUTPUT_FILE}")
    print(f"CWE feature dataset saved: {CWE_OUTPUT_FILE}")


def main() -> None:
    try:
        print("Loading processed vulnerability data...")

        df = load_data()

        print("Generating analytical features...")

        features_df = create_features(df)

        print("Generating multilabel CWE features...")

        cwe_df = create_cwe_features(df)

        save_features(features_df, cwe_df)

        print("\n========== FEATURE ENGINEERING REPORT ==========")
        print(f"Total records: {len(features_df)}")
        print(f"Main dataset columns: {len(features_df.columns)}")
        print(f"CWE feature columns: {len(cwe_df.columns) - 1}")
        print(f"Reference date: {REFERENCE_DATE.date()}")
        print("\nFEATURE ENGINEERING: SUCCESS")
        print("================================================")

    except (OSError, ValueError, SyntaxError) as error:
        print(f"Feature engineering error: {error}")


if __name__ == "__main__":
    main()