"""
Sentinel AI - Risk Alerts Engine

Generates explainable cybersecurity prioritization alerts.
These alerts do not indicate confirmed active attacks.
"""

import pandas as pd


class RiskAlertEngine:
    """Generate risk alerts from scored vulnerabilities."""

    REQUIRED_COLUMNS = [
        "cveID",
        "risk_score",
        "risk_level",
        "knownRansomwareCampaignUse"
    ]

    def generate_alerts(self, data):

        missing = [
            column for column in self.REQUIRED_COLUMNS
            if column not in data.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        result = data.copy()

        known_values = (
            result["knownRansomwareCampaignUse"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        if not known_values.isin(["known", "unknown"]).all():
            raise ValueError("Unexpected ransomware association values.")

        result["alert_type"] = "NONE"
        result["alert_message"] = ""

        critical = result["risk_level"] == "CRITICAL"
        ransomware = known_values == "known"

        result.loc[
            critical & ~ransomware,
            "alert_type"
        ] = "CRITICAL_RISK"

        result.loc[
            critical & ~ransomware,
            "alert_message"
        ] = "Critical technical risk requiring prioritization."

        result.loc[
            ~critical & ransomware,
            "alert_type"
        ] = "RANSOMWARE_ASSOCIATION"

        result.loc[
            ~critical & ransomware,
            "alert_message"
        ] = "Known ransomware campaign association."

        result.loc[
            critical & ransomware,
            "alert_type"
        ] = "CRITICAL_RANSOMWARE"

        result.loc[
            critical & ransomware,
            "alert_message"
        ] = (
            "Critical technical risk with known ransomware "
            "campaign association."
        )

        result["has_alert"] = result["alert_type"] != "NONE"

        return result
