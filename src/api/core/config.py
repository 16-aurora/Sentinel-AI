"""Central configuration for Sentinel AI API."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

API_TITLE = "Sentinel AI API"

API_DESCRIPTION = (
    "REST API for multidomain risk intelligence: "
    "cybersecurity, climate and economy."
)

API_VERSION = "1.0.0"

VALID_DOMAINS = (
    "cybersecurity",
    "climate",
    "economy",
)
