"""
Sentinel AI - Risk Explainer V2

Provides human-readable explanations for risk scores.
"""

import pandas as pd


class RiskExplainer:
    """Explain risk scores and their contributing signals."""

    REQUIRED_COLUMNS = [
        "cveID",
        "cvss_base_score",
        "knownRansomwareCampaignUse",
        "risk_score",
        "risk_level"
    ]

    def explain(self, data):

        missing = [
            column for column in self.REQUIRED_COLUMNS
            if column not in data.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        result = data.copy()

        explanations = []
        contributing_signals = []

        for _, row in result.iterrows():

            reasons = []
            signals = []

            cvss = float(row["cvss_base_score"])
            association = str(
                row["knownRansomwareCampaignUse"]
            ).strip().lower()

            # Technical severity explanation
            if cvss >= 9.0:
                reasons.append(
                    f"Very high technical severity (CVSS {cvss:.1f})."
                )
                signals.append("VERY_HIGH_CVSS")

            elif cvss >= 7.0:
                reasons.append(
                    f"High technical severity (CVSS {cvss:.1f})."
                )
                signals.append("HIGH_CVSS")

            elif cvss >= 4.0:
                reasons.append(
                    f"Medium technical severity (CVSS {cvss:.1f})."
                )
                signals.append("MEDIUM_CVSS")

            else:
                reasons.append(
                    f"Low technical severity (CVSS {cvss:.1f})."
                )
                signals.append("LOW_CVSS")

            # Ransomware association explanation
            if association == "known":
                reasons.append(
                    "Known association with ransomware campaigns "
                    "in the available CISA KEV data."
                )
                signals.append("KNOWN_RANSOMWARE_ASSOCIATION")

            elif association == "unknown":
                reasons.append(
                    "Ransomware campaign association is unknown. "
                    "This is not evidence of absence."
                )
                signals.append("UNKNOWN_RANSOMWARE_ASSOCIATION")

            # Final risk classification
            reasons.append(
                f"Final heuristic risk classification: "
                f"{row['risk_level']} "
                f"(score: {float(row['risk_score']):.2f}/100)."
            )

            explanations.append(" ".join(reasons))
            contributing_signals.append(signals)

        result["risk_explanation"] = explanations
        result["risk_contributing_signals"] = contributing_signals

        result["risk_score_interpretation"] = (
            "Heuristic prioritization score, not a calibrated "
            "probability of exploitation or attack."
        )

        return result
