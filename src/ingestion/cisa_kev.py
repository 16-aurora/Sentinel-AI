"""
CISA KEV Data Ingestion Module.

Downloads the official CISA Known Exploited Vulnerabilities
catalog and stores the original data locally.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import requests


CISA_KEV_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/"
    "known_exploited_vulnerabilities.json"
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

CATALOG_FILE = RAW_DATA_DIR / "cisa_kev.json"
METADATA_FILE = RAW_DATA_DIR / "cisa_kev_metadata.json"


def download_catalog() -> tuple[dict, bytes]:
    """Download the official CISA KEV catalog."""

    print("Connecting to CISA KEV...")

    response = requests.get(
        CISA_KEV_URL,
        timeout=30,
        headers={"User-Agent": "SentinelAI/0.1"}
    )

    response.raise_for_status()

    catalog = response.json()

    if not isinstance(catalog, dict):
        raise ValueError("Invalid catalog format.")

    if not isinstance(catalog.get("vulnerabilities"), list):
        raise ValueError("Missing vulnerabilities list.")

    print("Catalog downloaded successfully.")

    return catalog, response.content


def save_catalog(catalog: dict, original_content: bytes) -> None:
    """Save the original catalog and its metadata."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    CATALOG_FILE.write_bytes(original_content)

    metadata = {
        "source": "CISA Known Exploited Vulnerabilities Catalog",
        "source_url": CISA_KEV_URL,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "catalog_version": catalog.get("catalogVersion"),
        "catalog_release_date": catalog.get("dateReleased"),
        "vulnerability_count": len(catalog["vulnerabilities"]),
        "stored_file": str(CATALOG_FILE.relative_to(PROJECT_ROOT))
    }

    METADATA_FILE.write_text(
        json.dumps(metadata, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Catalog saved: {CATALOG_FILE}")
    print(f"Metadata saved: {METADATA_FILE}")


def main() -> None:
    """Run the ingestion process."""

    try:
        catalog, original_content = download_catalog()
        save_catalog(catalog, original_content)

        print("\n========== INGESTION SUMMARY ==========")
        print(f"Catalog version: {catalog.get('catalogVersion')}")
        print(f"Release date: {catalog.get('dateReleased')}")
        print(f"Total vulnerabilities: {len(catalog['vulnerabilities'])}")
        print("Status: SUCCESS")
        print("=======================================")

    except requests.RequestException as error:
        print(f"Network error: {error}")

    except (ValueError, json.JSONDecodeError) as error:
        print(f"Invalid catalog: {error}")

    except OSError as error:
        print(f"File error: {error}")


if __name__ == "__main__":
    main()