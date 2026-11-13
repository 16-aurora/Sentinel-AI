# Sentinel AI
# PU Class Prior Sensitivity Analysis

## 1. Objective

Evaluate hypothetical positive class-prior scenarios for the
Positive-Unlabeled ransomware dataset.

## 2. Observed dataset

- Total observations: 1768
- Observed positives: 361
- Unlabeled observations: 1407
- Observed positive proportion: 20.42%

The observed positive proportion is not necessarily the true
positive class prior.

## 3. Hypothetical scenarios

| scenario | assumed_class_prior | assumed_total_positives | observed_positives | estimated_hidden_positives | estimated_labeling_propensity |
| --- | --- | --- | --- | --- | --- |
| P1 | 25.00% | 442 | 361 | 81 | 81.67% |
| P2 | 30.00% | 530 | 361 | 169 | 68.11% |
| P3 | 40.00% | 707 | 361 | 346 | 51.06% |
| P4 | 50.00% | 884 | 361 | 523 | 40.84% |
| P5 | 60.00% | 1061 | 361 | 700 | 34.02% |
| P6 | 70.00% | 1238 | 361 | 877 | 29.16% |

## 4. Interpretation

The scenarios assume no false positive labels and use a
SCAR-based calculation of labeling propensity.

The estimated labeling propensity is:

Observed positives / Assumed total positives.

The number of hidden positives is hypothetical and is not
directly observed.

All six scenarios are mathematically compatible with the
available dataset.

## 5. Methodological limitations

- SCAR has not been established.
- SAR selection bias remains plausible.
- No scenario is confirmed as the true class prior.
- These calculations do not estimate model performance.
- The scenarios must be treated as sensitivity assumptions.

## 6. Decision

Retain all six scenarios for subsequent experimental
sensitivity analysis.

Do not select a single class prior without additional
methodological justification.
