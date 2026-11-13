"""
Sentinel AI - Risk Engine Automated Tests
"""

import pandas as pd

from src.risk_engine.risk_scorer import RiskScorer
from src.risk_engine.risk_prioritizer import RiskPrioritizer
from src.risk_engine.risk_alerts import RiskAlertEngine
from src.risk_engine.risk_explainer import RiskExplainer


def sample_data():
    return pd.DataFrame({
        "cveID": [
            "CVE-TEST-001",
            "CVE-TEST-002",
            "CVE-TEST-003",
            "CVE-TEST-004"
        ],
        "cvss_base_score": [10.0, 8.1, 6.0, 3.0],
        "knownRansomwareCampaignUse": [
            "Known",
            "Unknown",
            "Known",
            "Unknown"
        ]
    })


def test_risk_scorer():
    result = RiskScorer().calculate(sample_data())

    assert len(result) == 4
    assert result["risk_score"].notna().all()
    assert result["risk_level"].notna().all()


def test_risk_prioritizer():
    data = sample_data()
    data = RiskScorer().calculate(data)

    result = RiskPrioritizer().prioritize(data)

    assert result["risk_priority"].tolist() == [1, 2, 3, 4]
    assert result["risk_score"].is_monotonic_decreasing


def test_risk_alert_engine():
    data = sample_data()
    data = RiskScorer().calculate(data)

    result = RiskAlertEngine().generate_alerts(data)

    assert len(result) == 4
    assert result["alert_type"].notna().all()


def test_risk_explainer():
    data = sample_data()
    data = RiskScorer().calculate(data)

    result = RiskExplainer().explain(data)

    assert len(result) == 4
    assert result["risk_explanation"].notna().all()
