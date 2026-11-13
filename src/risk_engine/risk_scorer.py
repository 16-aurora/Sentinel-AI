"""
Sentinel AI - Risk Scorer V2

Heuristic cybersecurity risk prioritization.

Components:
- Technical severity (CVSS): 65%
- Known ransomware association: 25%

Unknown ransomware association is treated as missing
evidence, never as evidence of absence.

Scores are not calibrated probabilities.
"""

import pandas as pd


class RiskScorer:
    """Calculate explainable cybersecurity risk scores."""

    def __init__(
        self,
        cvss_weight=0.65,
        ransomware_weight=0.25
    ):
        if cvss_weight < 0 or ransomware_weight < 0:
            raise ValueError("Weights cannot be negative.")

        if cvss_weight + ransomware_weight <= 0:
            raise ValueError("At least one weight must be positive.")

        self.cvss_weight = cvss_weight
        self.ransomware_weight = ransomware_weight

    @staticmethod
    def classify_risk(score):
        """Classify a risk score into four categories."""

        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        return "LOW"

    def calculate(self, data, reference_date=None):
        """
        Calculate heuristic risk scores.

        Required columns:
        - cvss_base_score
        - knownRansomwareCampaignUse

        reference_date is retained for interface compatibility.
        Temporal urgency is not included in V2.
        """

        required = [
            "cvss_base_score",
            "knownRansomwareCampaignUse"
        ]

        missing = [
            column for column in required
            if column not in data.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        result = data.copy()

        cvss = pd.to_numeric(
            result["cvss_base_score"],
            errors="coerce"
        )

        if cvss.isna().any():
            raise ValueError("CVSS scores contain invalid values.")

        if ((cvss < 0) | (cvss > 10)).any():
            raise ValueError("CVSS scores must be between 0 and 10.")

        association = (
            result["knownRansomwareCampaignUse"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        valid_associations = association.isin(["known", "unknown"])

        if not valid_associations.all():
            raise ValueError(
                "Unexpected ransomware association values."
            )

        result["risk_cvss_component"] = cvss / 10.0

        result["risk_ransomware_component"] = (
            association.map({
                "known": 1.0,
                "unknown": float("nan")
            })
        )

        result["risk_ransomware_confirmed"] = (
            association == "known"
        )

        weighted_sum = (
            result["risk_cvss_component"] * self.cvss_weight
            + result["risk_ransomware_component"].fillna(0)
            * self.ransomware_weight
        )

        available_weight = (
            self.cvss_weight
            + result["risk_ransomware_component"]
            .notna()
            .astype(float) * self.ransomware_weight
        )

        result["risk_score"] = (
            weighted_sum / available_weight * 100
        )

        result["risk_level"] = result["risk_score"].apply(
            self.classify_risk
        )

        result["risk_engine_version"] = "2.0"

        return result
