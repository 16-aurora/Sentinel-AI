# Sentinel AI - Risk Engine V2

## 1. Overview

The Risk Engine is the cybersecurity risk assessment component
of Sentinel AI.

It processes vulnerability records and produces:
- Heuristic risk scores.
- Risk classifications.
- Prioritized vulnerability rankings.
- Risk alerts.
- Human-readable risk explanations.

## 2. Architecture

The engine contains four components:

### Risk Scorer
File: src/risk_engine/risk_scorer.py

Calculates a heuristic risk score using:
- CVSS technical severity: weight 0.65.
- Known ransomware campaign association: weight 0.25.

Unknown ransomware association is treated as missing evidence,
not as a negative label.

Available component weights are renormalized.

The temporal component is not currently used.

### Risk Prioritizer
File: src/risk_engine/risk_prioritizer.py

Ranks vulnerabilities by descending risk score.
Ties are resolved using ascending CVE identifier.

### Risk Alert Engine
File: src/risk_engine/risk_alerts.py

Generates four alert categories:
- CRITICAL_RISK
- RANSOMWARE_ASSOCIATION
- CRITICAL_RANSOMWARE
- NONE

Alerts are prioritization signals, not proof of active attacks.

### Risk Explainer
File: src/risk_engine/risk_explainer.py

Produces human-readable explanations and identifies
contributing technical and ransomware-association signals.

## 3. Pipeline

File: src/risk_engine/risk_pipeline.py

The integrated pipeline executes:

1. Risk scoring.
2. Alert generation.
3. Risk explanation.
4. Vulnerability prioritization.

## 4. Current Dataset

Source: cybersecurity_features_v1.csv

- Vulnerability records: 1,768.
- Unique CVE identifiers: 1,768.
- Integrated assessment records: 1,768.
- Output columns: 81.

## 5. V2 Risk Distribution

- CRITICAL: 1,132 (64.03%).
- HIGH: 538 (30.43%).
- MEDIUM: 94 (5.32%).
- LOW: 4 (0.23%).

## 6. Alert Distribution

- CRITICAL_RISK: 816.
- CRITICAL_RANSOMWARE: 316.
- RANSOMWARE_ASSOCIATION: 45.
- NONE: 591.

## 7. Testing

Automated tests are located in:

tests/test_risk_engine.py

Latest recorded execution:
- 4 tests passed.
- 0 failures.
- Execution time: 1.13 seconds.

Run tests with:

python -m pytest tests/test_risk_engine.py -v

## 8. Limitations

- Risk scores are heuristic scores, not calibrated probabilities.
- Risk weights and classification thresholds require further validation.
- Unknown ransomware association does not mean absence of ransomware.
- Historical CISA remediation due dates do not establish current patch status.
- Alerts do not prove active exploitation or attacks.
- The current pipeline does not consume PU Bagging predictions.

## 9. Output

Integrated assessment:

data/processed/sentinel_risk_assessment_v2.csv

The output includes risk scores, classifications, alert information,
explanations and prioritization.
