"""
Sentinel AI - Anomaly Detector V1

Loads a trained Isolation Forest model and detects
statistically unusual vulnerability patterns.
"""

from pathlib import Path

import joblib
import pandas as pd


class AnomalyDetector:

    REQUIRED_COLUMNS = [
        "cveID",
        "cvss_base_score",
        "attack_vector",
        "attack_complexity",
        "privileges_required",
        "user_interaction",
        "confidentiality_impact",
        "integrity_impact",
        "availability_impact"
    ]

    def __init__(self, model_path=None):

        if model_path is None:
            model_path = (
                Path(__file__).resolve().parents[2]
                / "models"
                / "isolation_forest"
                / "isolation_forest_v1.joblib"
            )

        bundle = joblib.load(model_path)

        self.model = bundle["model"]
        self.preprocessor = bundle["preprocessor"]
        self.feature_names = bundle["feature_names"]

    def detect(self, data):

        missing = [
            col for col in self.REQUIRED_COLUMNS
            if col not in data.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        if data["cveID"].isna().any():
            raise ValueError("Missing CVE identifiers")

        if data["cveID"].duplicated().any():
            raise ValueError("Duplicate CVE identifiers")

        features = data[self.REQUIRED_COLUMNS[1:]].copy()

        if features.isna().any().any():
            raise ValueError("Missing feature values")

        if not pd.api.types.is_numeric_dtype(
            features["cvss_base_score"]
        ):
            raise ValueError("CVSS must be numeric")

        if not features["cvss_base_score"].between(0, 10).all():
            raise ValueError("CVSS values must be between 0 and 10")

        transformed = self.preprocessor.transform(features)

        transformed = pd.DataFrame(
            transformed,
            columns=self.feature_names,
            index=data.index
        )

        predictions = self.model.predict(transformed)
        scores = self.model.decision_function(transformed)

        result = pd.DataFrame({
            "cveID": data["cveID"].values,
            "anomaly_prediction": predictions,
            "anomaly_score": scores,
            "is_anomaly": predictions == -1
        })

        result["anomaly_investigation_flag"] = (
            result["is_anomaly"].map({
                True: "REVIEW_STATISTICAL_ANOMALY",
                False: "NO_ANOMALY_FLAG"
            })
        )

        return result
