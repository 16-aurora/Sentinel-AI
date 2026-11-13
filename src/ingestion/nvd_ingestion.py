"""
Sentinel AI - NVD Data Ingestion Module

Retrieves vulnerability information from the official NVD API 2.0,
extracts CVSS metrics and saves enriched records with provenance.

Features:
- Individual CVE lookup
- CVSS 2.0, 3.0, 3.1 and 4.0 extraction
- Primary assessment selection
- Retry and timeout handling
- Rate limiting
- Incremental checkpoints and resume
- Raw response preservation
- Download metadata
"""

import os
import json
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from dotenv import load_dotenv


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = DATA_PROCESSED_DIR / "nvd_cve_enriched.csv"
RAW_JSON = DATA_RAW_DIR / "nvd_cve_records.json"
METADATA_JSON = DATA_RAW_DIR / "nvd_ingestion_metadata.json"


# ============================================================
# 2. API CONFIGURATION
# ============================================================

load_dotenv(PROJECT_ROOT / ".env")

NVD_API_URL = (
    "https://services.nvd.nist.gov/rest/json/cves/2.0"
)

NVD_API_KEY = os.getenv("NVD_API_KEY")

REQUEST_TIMEOUT = 30
REQUEST_DELAY = 6
MAX_RETRIES = 3

CHECKPOINT_EVERY = 25


# ============================================================
# 3. LOGGING
# ============================================================

logger = logging.getLogger(__name__)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
    )
    logger.addHandler(handler)

logger.setLevel(logging.INFO)


# ============================================================
# 4. HTTP SESSION
# ============================================================

def create_nvd_session() -> requests.Session:
    """Create a reusable HTTP session for NVD."""

    session = requests.Session()

    session.headers.update({
        "User-Agent": "SentinelAI/1.0"
    })

    if NVD_API_KEY:
        session.headers.update({
            "apiKey": NVD_API_KEY
        })

    return session


# ============================================================
# 5. FETCH ONE CVE
# ============================================================

def fetch_nvd_cve(
    cve_id: str,
    session: Optional[requests.Session] = None
) -> tuple[Optional[dict], str]:
    """
    Retrieve one CVE from NVD.

    Returns:
        (CVE data, status)

    Possible statuses:
        found
        not_found
        request_error
    """

    own_session = session is None

    if own_session:
        session = create_nvd_session()

    try:
        for attempt in range(1, MAX_RETRIES + 1):

            try:
                response = session.get(
                    NVD_API_URL,
                    params={"cveId": cve_id},
                    timeout=REQUEST_TIMEOUT
                )

                if response.status_code == 200:

                    results = response.json().get(
                        "vulnerabilities", []
                    )

                    if not results:
                        return None, "not_found"

                    return results[0]["cve"], "found"

                if response.status_code in (
                    403, 429, 500, 502, 503, 504
                ):

                    if attempt == MAX_RETRIES:
                        logger.error(
                            "NVD request failed for %s: HTTP %s",
                            cve_id,
                            response.status_code
                        )
                        return None, "request_error"

                    retry_after = response.headers.get(
                        "Retry-After"
                    )

                    try:
                        wait_time = float(retry_after)
                    except (TypeError, ValueError):
                        wait_time = 2 ** attempt

                    logger.warning(
                        "HTTP %s for %s. Retry %s/%s in %s seconds.",
                        response.status_code,
                        cve_id,
                        attempt,
                        MAX_RETRIES,
                        wait_time
                    )

                    time.sleep(wait_time)
                    continue

                logger.error(
                    "HTTP %s for %s",
                    response.status_code,
                    cve_id
                )

                return None, "request_error"

            except requests.RequestException as error:

                if attempt == MAX_RETRIES:
                    logger.error(
                        "Connection error for %s: %s",
                        cve_id,
                        error
                    )
                    return None, "request_error"

                wait_time = 2 ** attempt

                logger.warning(
                    "Connection error for %s. Retry in %s seconds.",
                    cve_id,
                    wait_time
                )

                time.sleep(wait_time)

    finally:
        if own_session:
            session.close()

    return None, "request_error"


# ============================================================
# 6. EXTRACT CVSS METRICS
# ============================================================


def extract_nvd_cvss(cve_data: dict) -> dict:
    """
    Extract the preferred CVSS assessment.

    Preference:
        CVSS 4.0
        CVSS 3.1
        CVSS 3.0
        CVSS 2.0

    Preserves common metrics and CVSS 4.0-specific metrics.
    """

    metrics = cve_data.get("metrics", {})

    metric_versions = [
        ("cvssMetricV40", "4.0"),
        ("cvssMetricV31", "3.1"),
        ("cvssMetricV30", "3.0"),
        ("cvssMetricV2", "2.0")
    ]

    selected_metric = None

    for metric_key, version in metric_versions:
        available_metrics = metrics.get(metric_key, [])

        if available_metrics:
            selected_metric = next(
                (
                    metric for metric in available_metrics
                    if metric.get("type") == "Primary"
                ),
                available_metrics[0]
            )
            break

    record = {
        "cvss_version": None,
        "cvss_base_score": None,
        "cvss_severity": None,
        "attack_vector": None,
        "attack_complexity": None,
        "privileges_required": None,
        "user_interaction": None,
        "scope": None,
        "confidentiality_impact": None,
        "integrity_impact": None,
        "availability_impact": None,
        "cvss_vector": None,
        "cvss_source": None,
        "cvss_assessment_type": None,

        # CVSS 4.0-specific metrics
        "cvss4_attack_requirements": None,
        "cvss4_vuln_confidentiality_impact": None,
        "cvss4_vuln_integrity_impact": None,
        "cvss4_vuln_availability_impact": None,
        "cvss4_sub_confidentiality_impact": None,
        "cvss4_sub_integrity_impact": None,
        "cvss4_sub_availability_impact": None,
        "cvss4_exploit_maturity": None,
        "cvss4_automatable": None,
        "cvss4_recovery": None,
        "cvss4_safety": None,
        "cvss4_value_density": None,
        "cvss4_vulnerability_response_effort": None,
        "cvss4_provider_urgency": None,
        "cvss4_confidentiality_requirement": None,
        "cvss4_integrity_requirement": None,
        "cvss4_availability_requirement": None,
        "cvss4_modified_attack_vector": None,
        "cvss4_modified_attack_complexity": None,
        "cvss4_modified_attack_requirements": None,
        "cvss4_modified_privileges_required": None,
        "cvss4_modified_user_interaction": None,
        "cvss4_modified_vuln_confidentiality_impact": None,
        "cvss4_modified_vuln_integrity_impact": None,
        "cvss4_modified_vuln_availability_impact": None,
        "cvss4_modified_sub_confidentiality_impact": None,
        "cvss4_modified_sub_integrity_impact": None,
        "cvss4_modified_sub_availability_impact": None
    }

    if selected_metric is None:
        return record

    data = selected_metric.get("cvssData", {})
    version = data.get("version")

    # Common metrics
    record.update({
        "cvss_version": version,
        "cvss_base_score": data.get("baseScore"),
        "cvss_severity": (
            data.get("baseSeverity")
            or selected_metric.get("baseSeverity")
        ),
        "attack_vector": data.get(
            "attackVector",
            data.get("accessVector")
        ),
        "attack_complexity": data.get(
            "attackComplexity",
            data.get("accessComplexity")
        ),
        "privileges_required": data.get(
            "privilegesRequired",
            data.get("authentication")
        ),
        "user_interaction": data.get("userInteraction"),
        "scope": data.get("scope"),
        "confidentiality_impact": (
            data.get("confidentialityImpact")
            or data.get("vulnConfidentialityImpact")
        ),
        "integrity_impact": (
            data.get("integrityImpact")
            or data.get("vulnIntegrityImpact")
        ),
        "availability_impact": (
            data.get("availabilityImpact")
            or data.get("vulnAvailabilityImpact")
        ),
        "cvss_vector": data.get("vectorString"),
        "cvss_source": selected_metric.get("source"),
        "cvss_assessment_type": selected_metric.get("type")
    })

    # CVSS 4.0-specific metrics
    if version == "4.0":

        cvss4_mapping = {
            "cvss4_attack_requirements": "attackRequirements",
            "cvss4_vuln_confidentiality_impact": "vulnConfidentialityImpact",
            "cvss4_vuln_integrity_impact": "vulnIntegrityImpact",
            "cvss4_vuln_availability_impact": "vulnAvailabilityImpact",
            "cvss4_sub_confidentiality_impact": "subConfidentialityImpact",
            "cvss4_sub_integrity_impact": "subIntegrityImpact",
            "cvss4_sub_availability_impact": "subAvailabilityImpact",
            "cvss4_exploit_maturity": "exploitMaturity",
            "cvss4_automatable": "Automatable",
            "cvss4_recovery": "Recovery",
            "cvss4_safety": "Safety",
            "cvss4_value_density": "valueDensity",
            "cvss4_vulnerability_response_effort": "vulnerabilityResponseEffort",
            "cvss4_provider_urgency": "providerUrgency",
            "cvss4_confidentiality_requirement": "confidentialityRequirement",
            "cvss4_integrity_requirement": "integrityRequirement",
            "cvss4_availability_requirement": "availabilityRequirement",
            "cvss4_modified_attack_vector": "modifiedAttackVector",
            "cvss4_modified_attack_complexity": "modifiedAttackComplexity",
            "cvss4_modified_attack_requirements": "modifiedAttackRequirements",
            "cvss4_modified_privileges_required": "modifiedPrivilegesRequired",
            "cvss4_modified_user_interaction": "modifiedUserInteraction",
            "cvss4_modified_vuln_confidentiality_impact": "modifiedVulnConfidentialityImpact",
            "cvss4_modified_vuln_integrity_impact": "modifiedVulnIntegrityImpact",
            "cvss4_modified_vuln_availability_impact": "modifiedVulnAvailabilityImpact",
            "cvss4_modified_sub_confidentiality_impact": "modifiedSubConfidentialityImpact",
            "cvss4_modified_sub_integrity_impact": "modifiedSubIntegrityImpact",
            "cvss4_modified_sub_availability_impact": "modifiedSubAvailabilityImpact"
        }

        for output_field, source_field in cvss4_mapping.items():
            record[output_field] = data.get(source_field)

    return record


# ============================================================
# 7. EXTRACT ADDITIONAL NVD INFORMATION
# ============================================================

def extract_nvd_record(
    cve_id: str,
    cve_data: Optional[dict],
    status: str
) -> dict:
    """Create one normalized record per requested CVE."""

    record = {
        "cveID": cve_id,
        "nvd_found": status == "found",
        "nvd_status": status,
        "nvd_published": None,
        "nvd_last_modified": None,
        "nvd_description": None,
        "nvd_cwe": None,
        "nvd_reference_count": 0
    }

    if cve_data is None:
        record.update(extract_nvd_cvss({}))
        return record

    record["nvd_published"] = cve_data.get("published")
    record["nvd_last_modified"] = cve_data.get(
        "lastModified"
    )

    descriptions = cve_data.get("descriptions", [])

    english_descriptions = [
        item.get("value")
        for item in descriptions
        if item.get("lang") == "en"
    ]

    if english_descriptions:
        record["nvd_description"] = english_descriptions[0]

    weaknesses = cve_data.get("weaknesses", [])

    cwe_values = []

    for weakness in weaknesses:
        for item in weakness.get("description", []):

            if item.get("lang") == "en":
                value = item.get("value")

                if value and value not in cwe_values:
                    cwe_values.append(value)

    record["nvd_cwe"] = ";".join(cwe_values) or None

    record["nvd_reference_count"] = len(
        cve_data.get("references", [])
    )

    record.update(extract_nvd_cvss(cve_data))

    return record


# ============================================================
# 8. SAVE CHECKPOINTS AND METADATA
# ============================================================

def save_ingestion_state(
    records: list,
    raw_records: dict,
    requested_count: int,
    start_time: str,
    delay: float
) -> None:
    """Persist processed data, raw responses and metadata."""

    df = pd.DataFrame(records)

    df.to_csv(
        OUTPUT_CSV,
        index=False
    )

    with RAW_JSON.open("w", encoding="utf-8") as file:
        json.dump(
            raw_records,
            file,
            ensure_ascii=False,
            indent=2
        )

    metadata = {
        "source": "National Vulnerability Database",
        "api_version": "2.0",
        "api_url": NVD_API_URL,
        "started_at_utc": start_time,
        "updated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "requested_cves": requested_count,
        "processed_records": len(df),
        "nvd_found": int(
            df["nvd_found"].sum()
        ) if not df.empty else 0,
        "not_found": int(
            (df["nvd_status"] == "not_found").sum()
        ) if not df.empty else 0,
        "request_errors": int(
            (df["nvd_status"] == "request_error").sum()
        ) if not df.empty else 0,
        "cvss_available": int(
            df["cvss_base_score"].notna().sum()
        ) if not df.empty else 0,
        "request_delay_seconds": delay,
        "api_key_configured": bool(NVD_API_KEY),
        "processed_file": str(OUTPUT_CSV.relative_to(PROJECT_ROOT)),
        "raw_file": str(RAW_JSON.relative_to(PROJECT_ROOT))
    }

    with METADATA_JSON.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2
        )

    logger.info(
        "Checkpoint saved: %s records.",
        len(df)
    )


# ============================================================
# 9. INGEST MULTIPLE CVES
# ============================================================

def ingest_cves(
    cve_ids: list,
    delay: float = REQUEST_DELAY,
    checkpoint_every: int = CHECKPOINT_EVERY,
    resume: bool = True
) -> pd.DataFrame:
    """
    Retrieve and enrich a list of CVEs.

    Existing successful and not-found records are skipped
    when resume=True. Failed requests can be retried on
    the next execution.
    """

    cve_ids = list(dict.fromkeys(cve_ids))

    start_time = datetime.now(
        timezone.utc
    ).isoformat()

    records = []
    raw_records = {}

    if resume and OUTPUT_CSV.exists():

        existing_df = pd.read_csv(OUTPUT_CSV)

        records = existing_df.to_dict("records")

        logger.info(
            "Loaded %s existing records.",
            len(records)
        )

    if resume and RAW_JSON.exists():

        with RAW_JSON.open(
            "r",
            encoding="utf-8"
        ) as file:
            raw_records = json.load(file)

    completed_ids = {
        row["cveID"]
        for row in records
        if row.get("nvd_status") in (
            "found",
            "not_found"
        )
    }

    pending_ids = [
        cve_id
        for cve_id in cve_ids
        if cve_id not in completed_ids
    ]

    logger.info(
        "Total CVEs: %s | Already completed: %s | Pending: %s",
        len(cve_ids),
        len(completed_ids),
        len(pending_ids)
    )

    session = create_nvd_session()

    try:
        for index, cve_id in enumerate(
            pending_ids,
            start=1
        ):

            logger.info(
                "Processing %s/%s: %s",
                index,
                len(pending_ids),
                cve_id
            )

            cve_data, status = fetch_nvd_cve(
                cve_id,
                session=session
            )

            record = extract_nvd_record(
                cve_id,
                cve_data,
                status
            )

            # Replace previous failed attempt if present.
            records = [
                row for row in records
                if row["cveID"] != cve_id
            ]

            records.append(record)

            raw_records[cve_id] = cve_data

            if (
                index % checkpoint_every == 0
                or index == len(pending_ids)
            ):
                save_ingestion_state(
                    records,
                    raw_records,
                    len(cve_ids),
                    start_time,
                    delay
                )

            if index < len(pending_ids):
                time.sleep(delay)

    finally:
        session.close()

    # Save even if there were no pending requests.
    save_ingestion_state(
        records,
        raw_records,
        len(cve_ids),
        start_time,
        delay
    )

    result_df = pd.DataFrame(records)

    return result_df


# ============================================================
# 10. MODULE INFORMATION
# ============================================================

def get_module_info() -> dict:
    """Return configuration and output paths."""

    return {
        "api_url": NVD_API_URL,
        "request_timeout": REQUEST_TIMEOUT,
        "request_delay": REQUEST_DELAY,
        "max_retries": MAX_RETRIES,
        "api_key_configured": bool(NVD_API_KEY),
        "output_csv": str(OUTPUT_CSV),
        "raw_json": str(RAW_JSON),
        "metadata_json": str(METADATA_JSON)
    }