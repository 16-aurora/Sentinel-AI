
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.ml.anomaly_detector import AnomalyDetector


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def detector():
    return AnomalyDetector()


@pytest.fixture
def source_data():
    path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "cybersecurity_features_v1.csv"
    )
    return pd.read_csv(path)


def test_detector_processes_all_records(detector, source_data):
    results = detector.detect(source_data)

    assert len(results) == len(source_data)
    assert results["cveID"].is_unique
    assert results["anomaly_score"].notna().all()


def test_detector_reproduces_saved_results(detector, source_data):
    results = detector.detect(source_data)

    previous_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "isolation_forest_results_v1.csv"
    )
    previous = pd.read_csv(previous_path)

    comparison = results.merge(
        previous[["cveID", "anomaly_prediction", "anomaly_score"]],
        on="cveID",
        suffixes=("_new", "_saved"),
        validate="one_to_one"
    )

    assert np.array_equal(
        comparison["anomaly_prediction_new"],
        comparison["anomaly_prediction_saved"]
    )

    assert np.allclose(
        comparison["anomaly_score_new"],
        comparison["anomaly_score_saved"],
        rtol=1e-9,
        atol=1e-9
    )


def test_detector_rejects_missing_columns(detector, source_data):
    incomplete = source_data.drop(columns=["cvss_base_score"])

    with pytest.raises(ValueError):
        detector.detect(incomplete)


def test_detector_rejects_duplicate_cve_ids(detector, source_data):
    duplicated = pd.concat(
        [source_data.iloc[:2], source_data.iloc[:1]],
        ignore_index=True
    )

    with pytest.raises(ValueError):
        detector.detect(duplicated)
