# Sentinel AI
# Complete Preprocessing Pipeline Audit

## 1. Objective

Validate the technical consistency and numerical integrity
of the initial ransomware preprocessing pipeline.

## 2. Dataset dimensions

| Dataset | Observations | Original features |
|---|---:|---:|
| Training | 1414 | 11 |
| Validation | 354 | 11 |

## 3. Transformation results

| Dataset | Observations | Transformed features |
|---|---:|---:|
| Training | 1414 | 486 |
| Validation | 354 | 486 |

## 4. Validation checks

| Check | Result |
|---|---|
| Same transformed dimensions | PASS |
| Feature names match dimensions | PASS |
| Unique feature names | PASS |
| Training values finite | PASS |
| Validation values finite | PASS |
| Training and validation indices disjoint | PASS |

## 5. Preprocessing architecture

- Numerical variables: median imputation and StandardScaler.
- Categorical variables: OneHotEncoder.
- CWE variables: custom multi-label transformer.
- CWE vocabulary fitted exclusively on training observations.

## 6. CWE validation coverage

The separate CWE validation audit reported:

- 180 CWE categories learned in training.
- 93.51% known-category coverage.
- 18 unknown CWE categories.
- 22 unknown CWE occurrences.
- 6.21% of validation observations affected.

Unknown validation categories were not added to the
training vocabulary.

## 7. Limitations

This audit verifies technical preprocessing consistency.
It does not establish predictive performance.

The target remains Positive-Unlabeled:
observations marked Unknown are not confirmed negatives.

The current split is not a temporal validation strategy.

## 8. Status

COMPLETE — Initial preprocessing pipeline technically validated.

No predictive model has been trained or evaluated at this stage.
