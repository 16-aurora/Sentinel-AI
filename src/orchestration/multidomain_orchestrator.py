import csv
import math
from pathlib import Path
from collections import Counter


DOMAIN_CONFIG = {
    "cybersecurity": {
        "file": "data/processed/sentinel_integrated_intelligence_v2.csv",
        "expected_rows": 1768,
        "required_columns": [
            "cveID", "risk_score", "risk_level",
            "risk_score_interpretation"
        ],
        "score_column": "risk_score",
        "category_column": "risk_level",
        "key_columns": ["cveID"],
        "unit": "CVE / vulnerability"
    },
    "climate": {
        "file": "data/processed/climate/eu27_climate_exposure_index_v1.csv",
        "expected_rows": 297,
        "required_columns": [
            "country_code", "year",
            "climate_exposure_index",
            "climate_exposure_category"
        ],
        "score_column": "climate_exposure_index",
        "category_column": "climate_exposure_category",
        "key_columns": ["country_code", "year"],
        "unit": "Country-year"
    },
    "economy": {
        "file": "data/processed/economy/eu27_economic_risk_assessment_v1.csv",
        "expected_rows": 297,
        "required_columns": [
            "country_code", "year",
            "economic_risk_score",
            "economic_risk_category"
        ],
        "score_column": "economic_risk_score",
        "category_column": "economic_risk_category",
        "key_columns": ["country_code", "year"],
        "unit": "Country-year"
    }
}


class MultidomainOrchestrator:

    def __init__(self, project_root):
        self.project_root = Path(project_root)

    def _load_domain(self, domain):

        config = DOMAIN_CONFIG[domain]
        path = self.project_root / config["file"]

        result = {
            "domain": domain,
            "status": "UNAVAILABLE",
            "file": config["file"],
            "unit": config["unit"],
            "records": 0,
            "score_column": config["score_column"],
            "category_column": config["category_column"],
            "categories": {},
            "score_min": None,
            "score_max": None,
            "score_mean": None,
            "error": None
        }

        if not path.exists():
            result["error"] = "Dataset file not found."
            return result

        try:
            with open(path, encoding="utf-8-sig", newline="") as file:
                reader = csv.DictReader(file)
                columns = reader.fieldnames or []

                missing = [
                    col for col in config["required_columns"]
                    if col not in columns
                ]

                if missing:
                    result["status"] = "SCHEMA_ERROR"
                    result["error"] = (
                        "Missing required columns: " + ", ".join(missing)
                    )
                    return result

                rows = list(reader)

            if len(rows) != config["expected_rows"]:
                result["status"] = "REVIEW"
                result["error"] = (
                    f"Expected {config['expected_rows']} records; "
                    f"found {len(rows)}."
                )
                return result

            scores = []
            categories = Counter()
            seen_keys = set()

            for row_number, row in enumerate(rows, start=2):

                # Validate record identity.
                key = tuple(
                    (row.get(column) or "").strip()
                    for column in config["key_columns"]
                )

                if any(not value for value in key):
                    result["status"] = "DATA_ERROR"
                    result["error"] = (
                        f"Empty record key at CSV row {row_number}."
                    )
                    return result

                if key in seen_keys:
                    result["status"] = "DATA_ERROR"
                    result["error"] = (
                        f"Duplicate record key at CSV row {row_number}."
                    )
                    return result

                seen_keys.add(key)

                # Validate category.
                category = (row.get(config["category_column"]) or "").strip()

                if not category:
                    result["status"] = "DATA_ERROR"
                    result["error"] = (
                        f"Empty category at CSV row {row_number}."
                    )
                    return result

                categories[category] += 1

                # Validate numeric score.
                raw_score = (row.get(config["score_column"]) or "").strip()

                if not raw_score:
                    result["status"] = "DATA_ERROR"
                    result["error"] = (
                        f"Empty score at CSV row {row_number}."
                    )
                    return result

                try:
                    score = float(raw_score)
                except (ValueError, TypeError):
                    result["status"] = "DATA_ERROR"
                    result["error"] = (
                        f"Invalid score at CSV row {row_number}."
                    )
                    return result

                if not math.isfinite(score):
                    result["status"] = "DATA_ERROR"
                    result["error"] = (
                        f"Non-finite score at CSV row {row_number}."
                    )
                    return result

                if not 0 <= score <= 100:
                    result["status"] = "DATA_ERROR"
                    result["error"] = (
                        f"Score outside 0-100 range at CSV row {row_number}."
                    )
                    return result

                scores.append(score)

            result.update({
                "status": "AVAILABLE",
                "records": len(rows),
                "categories": dict(categories),
                "score_min": round(min(scores), 2),
                "score_max": round(max(scores), 2),
                "score_mean": round(sum(scores) / len(scores), 2),
                "error": None
            })

            return result

        except OSError as error:
            result["status"] = "READ_ERROR"
            result["error"] = str(error)
            return result

    def run(self):

        domains = {
            name: self._load_domain(name)
            for name in DOMAIN_CONFIG
        }

        available = sum(
            result["status"] == "AVAILABLE"
            for result in domains.values()
        )

        return {
            "system": "Sentinel AI",
            "orchestrator_version": "2.0",
            "domains_available": available,
            "domains_total": len(domains),
            "system_status": (
                "OPERATIONAL"
                if available == len(domains)
                else "PARTIAL"
            ),
            "domains": domains
        }
