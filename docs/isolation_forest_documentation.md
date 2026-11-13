# Sentinel AI - Isolation Forest Documentation

## 1. Overview

Isolation Forest is an unsupervised machine learning algorithm
implemented in Sentinel AI to identify statistically unusual
observations in the cybersecurity dataset.

The detector complements the Risk Engine. It identifies unusual
technical profiles but does not determine whether a vulnerability
is dangerous or represents an active security threat.

## 2. Dataset

- Source: Integrated CISA KEV and NVD cybersecurity dataset.
- Observations: 1,768 vulnerabilities.
- Original feature count: 68 columns.
- Selected model inputs: 8 features.

### Selected features

Numeric:
- cvss_base_score

Categorical:
- attack_vector
- attack_complexity
- privileges_required
- user_interaction
- confidentiality_impact
- integrity_impact
- availability_impact

Risk labels, ransomware association and model outputs were excluded
from the Isolation Forest input features.

## 3. Preprocessing

The preprocessing pipeline uses:

- StandardScaler for CVSS base scores.
- OneHotEncoder with handle_unknown="ignore" for categorical features.
- Encoded feature matrix: 24 columns.
- No missing or infinite values in the prepared matrix.

The fitted preprocessing transformer is saved alongside the model
and reused during inference.

The original exploratory model and preprocessor were fitted using
the complete dataset. Consequently, this experiment does not
represent an independent held-out evaluation.

## 4. Isolation Forest V1 Configuration

- Algorithm: IsolationForest
- Number of estimators: 200
- Contamination: 0.05
- Random state: 42
- Parallel processing: n_jobs=-1

### Original experiment results

- Total observations: 1,768
- Anomalies: 89
- Normal observations: 1,679
- Observed anomaly rate: 5.03%

The anomaly score is obtained from decision_function.
Lower scores indicate observations considered more anomalous.

Predictions:
- -1: anomaly
- 1: normal observation

The contamination value is an experimental threshold assumption,
not an estimate of the true prevalence of anomalous vulnerabilities.

## 5. Reproducibility and Automated Testing

The reusable module is:

src/ml/anomaly_detector.py

The detector:
- Loads the saved model and preprocessor.
- Validates incoming vulnerability data.
- Generates anomaly predictions and scores.
- Produces investigation flags.

Functional reproducibility test:
- 1,768 records processed.
- Predictions identical to the original experiment.
- Anomaly scores identical within numerical tolerance.

Automated tests:
- Processes all records.
- Reproduces saved predictions and scores.
- Rejects missing required columns.
- Rejects duplicate CVE identifiers.

Result: 4 automated tests passed.

## 6. Random Seed Stability Experiment

Three models were trained using different random seeds:

| Seed | Anomalies |
|------|-----------|
| 21   | 87        |
| 42   | 89        |
| 123  | 87        |

Pairwise Jaccard similarities:

| Comparison | Jaccard |
|------------|---------|
| 21 vs 42   | 0.7959  |
| 21 vs 123  | 0.7576  |
| 42 vs 123  | 0.8526  |

A total of 72 anomalies were shared by all three models.

These results describe sensitivity to random initialization.
They do not establish predictive accuracy against verified anomalies.

## 7. Categorical Feature Bias Investigation

An exploratory analysis compared anomaly rates across the
seven categorical features.

Some categories showed substantially higher anomaly rates:

- attack_vector = ADJACENT: 2 of 4 (50.00%).
- attack_vector = ADJACENT_NETWORK: 6 of 24 (25.00%).
- attack_complexity = HIGH: 21 of 124 (16.94%).
- availability_impact = LOW: 24 of 29 (82.76%).
- confidentiality_impact = LOW: 37 of 92 (40.22%).
- integrity_impact = LOW: 33 of 89 (37.08%).

These are descriptive associations, not causal effects.

Categories with very small sample sizes can produce unstable
anomaly-rate estimates. Rare categories should not automatically
be interpreted as security threats.

Detailed results:
reports/figures/anomaly_category_bias_report.csv

## 8. Categorical Feature Ablation Experiment

An alternative Isolation Forest configuration was trained using
only cvss_base_score.

Configuration:
- IsolationForest
- 200 estimators
- Contamination: 0.05
- Random state: 42
- StandardScaler on CVSS

Results:

| Metric | Original | CVSS-only |
|--------|----------|-----------|
| Anomalies | 89 | 74 |

Overlap:
- Shared anomalies: 32.
- Original-only anomalies: 57.
- CVSS-only anomalies: 42.
- Jaccard similarity: 0.2443.

This indicates that categorical features substantially change
which observations are identified as anomalies.

It does not demonstrate that either configuration is more accurate.

## 9. Anomaly Group Profiles

| Group | Observations | Mean CVSS | Mean Risk |
|-------|--------------|-----------|-----------|
| Shared | 32 | 4.64 | 49.04 |
| Original-only | 57 | 6.22 | 63.85 |
| CVSS-only | 42 | 8.48 | 85.20 |
| Normal in both | 1,637 | 8.56 | 86.31 |

The two configurations identify different technical profiles.

The Risk Engine and Isolation Forest measure different concepts:
heuristic risk prioritization and statistical unusualness,
respectively.

Detailed results:
reports/figures/anomaly_group_profile_comparison_v1.csv

## 10. Saved Artifacts

Model and preprocessing:
- models/isolation_forest/isolation_forest_v1.joblib
- models/isolation_forest/experiment_metadata.json

Detector:
- src/ml/anomaly_detector.py

Results:
- data/processed/isolation_forest_results_v1.csv
- data/processed/isolation_forest_low_threshold_anomalies_v1.csv
- data/processed/sentinel_integrated_intelligence_v1.csv

Reports:
- reports/figures/anomaly_category_bias_report.csv
- reports/figures/anomaly_group_profile_comparison_v1.csv

Tests:
- tests/test_anomaly_detector.py

## 11. Limitations

1. There is no independently verified anomaly ground truth.
2. The contamination value is a chosen experimental assumption.
3. The initial model was fitted on the complete dataset.
4. Rare categories can influence anomaly detection.
5. An anomaly is not necessarily a dangerous vulnerability.
6. Results are specific to the analyzed CISA KEV dataset.
7. Shared CVSS inputs mean that comparisons with the Risk Engine
   are not independent evidence of predictive performance.
8. The CVSS-only experiment is exploratory and not a validated
   replacement for the original detector.

## 12. Future Improvements

- Evaluate models on carefully separated data.
- Investigate alternative categorical encoding strategies.
- Study feature influence with controlled experiments.
- Evaluate stability across data samples and time periods.
- Seek independently reviewed anomaly labels.
- Monitor changes in input data distributions.
- Document and validate future detector versions.

## 13. Conclusion

Isolation Forest V1 provides a reusable unsupervised anomaly
detection component within Sentinel AI.

The experiments show reproducible results and meaningful
sensitivity to random initialization and feature selection.

The detector is intended to support investigation and
prioritization, not to confirm security incidents or provide
calibrated probabilities of risk.
