# Sentinel AI
# Master Feature Selection Audit

## 1. Purpose

This document records the global feature selection audit for
the cybersecurity dataset used in Sentinel AI.

The purpose is to establish a transparent and reproducible
classification of the available variables before machine
learning model development.

The audit distinguishes between:

- Initial model candidates.
- Alternative representations.
- Variables excluded from predictive use.
- Target variables.

This classification is preliminary and does not constitute
final approval of features for every model.

## 2. Dataset overview

| Metric | Result |
|---|---:|
| Dataset observations | 1768 |
| Original dataset columns | 100 |
| Classified variables | 100 |
| Unclassified variables | 0 |
| Duplicate classifications | 0 |

The feature selection matrix contains five fields:

- feature
- group
- origin
- decision
- reason

## 3. Global classification results

| Decision | Number of variables |
|---|---:|
| KEEP | 8 |
| ALTERNATIVE | 70 |
| EXCLUDE | 20 |
| TARGET | 2 |

### Interpretation

**KEEP**

Initial candidates for subsequent model-specific evaluation.
These variables are not automatically approved for every model.

**ALTERNATIVE**

Potentially useful variables that represent alternative
encodings, aggregates, source fields or experimental features.
They should be evaluated in separate model configurations
where appropriate.

**EXCLUDE**

Variables excluded from initial predictive feature sets because
they are identifiers, constant fields, provenance metadata,
redundant representations or otherwise unsuitable predictors.

**TARGET**

Variables representing the prediction target. They must not
be used as input predictors.

## 4. Feature groups

The matrix organizes variables into the following groups:

- **ATTACK_FEASIBILITY**: 5 variables
- **CATEGORICAL**: 4 variables
- **CVSS4**: 7 variables
- **CVSS4_CONSTANT**: 14 variables
- **CVSS4_CORE**: 7 variables
- **CVSS4_EXPERIMENTAL**: 7 variables
- **CVSS_METADATA**: 1 variables
- **CVSS_ORIGINAL**: 10 variables
- **CVSS_PROVENANCE**: 2 variables
- **DATA_QUALITY**: 2 variables
- **IDENTIFIER**: 1 variables
- **NVD_METADATA**: 1 variables
- **REMEDIATION**: 10 variables
- **REMEDIATION_SOURCE**: 1 variables
- **SEVERITY**: 3 variables
- **TARGET**: 1 variables
- **TARGET_METADATA**: 2 variables
- **TARGET_SOURCE**: 1 variables
- **TECHNICAL_IMPACT**: 4 variables
- **TEMPORAL**: 9 variables
- **TEMPORAL_SOURCE**: 4 variables
- **TEXT_NLP**: 4 variables

## 5. Key methodological decisions

### 5.1 Ransomware labels and positive-unlabeled learning

The CISA field `knownRansomwareCampaignUse` is the original
source of the ransomware label.

The derived variable `ransomware_known` represents the same
target in encoded form.

The dataset contains:

- Known ransomware campaign use: 361 observations.
- Unknown ransomware campaign use: 1,407 observations.

Unknown observations must not be interpreted as confirmed
negative examples.

Any model using this target must respect the positive-unlabeled
nature of the labels. The original source label and its encoded
representation must never be included as predictors.

### 5.2 CVSS severity representations

The dataset contains the original CVSS base score,
normalized severity and categorical severity.

The normalized score is mathematically equivalent to the
base score divided by ten.

These representations should not automatically be included
together. Model experiments should compare suitable alternatives.

### 5.3 Attack feasibility

Attack feasibility components and their aggregate index are
heuristic representations.

The index uses an equal-weight arithmetic mean of the
selected components.

It is not an empirically calibrated probability of exploitation.

Component-based and aggregate-based model configurations
should be evaluated separately.

### 5.4 Technical impact

Confidentiality, integrity and availability impact scores
are represented individually and through an aggregate index.

The aggregate index should not automatically be combined
with all three individual components.

CVSS base scores are themselves derived from CVSS metrics.
Using the score together with its underlying impact metrics
may introduce redundancy or double counting.

### 5.5 Temporal variables

The initial temporal candidates are:

- `vulnerability_age_days`
- `days_overdue`
- `original_remediation_window`

Alternative temporal representations are retained in the
matrix for potential comparison.

The reference date used in the current feature engineering
was 2026-11-09.

Administrative remediation deadlines do not establish
whether a vulnerability has actually been patched.

### 5.6 Remediation variables

The initial remediation candidates are:

- `action_apply_updates`
- `action_apply_mitigations`
- `action_discontinue_product`
- `action_eol_eos`
- `action_security_assessment`

These variables are derived from the wording of CISA
remediation instructions.

They describe textual recommendations, not verified
remediation activity or patch status.

Several original indicators overlap or are subsets of
other indicators. Alternative representations are retained
for later model comparison.

### 5.7 CVSS 4.0 coverage

The integrated dataset contains 115 CVSS 4.0 observations
out of 1,768 total observations.

The seven encoded core metrics are retained as alternatives.

Their missing values in records without CVSS 4.0 assessments
are structural missingness, not zero impact.

Fourteen additional CVSS 4.0 metrics showed no observed
variation in the available records and were excluded
provisionally.

Seven experimental metrics have limited coverage and require
additional missingness analysis before model use.

All selected CVSS 4.0 assessments in this dataset were
identified as Secondary assessments. This provenance must
be considered when interpreting results.

## 6. Data quality and leakage safeguards

The following safeguards are required during model development:

1. Exclude identifiers and target variables from predictors.
2. Never treat unknown ransomware labels as confirmed negatives.
3. Fit encoders and frequency mappings using training data only.
4. Fit normalization and imputation inside training pipelines.
5. Preserve structural missingness in CVSS 4.0 features.
6. Use temporal validation where appropriate.
7. Avoid using future information when predicting historical outcomes.
8. Keep provenance and assessment metadata available for audit.
9. Evaluate alternative feature representations separately.
10. Document every model-specific feature set.

## 7. Important dataset limitations

- The dataset contains CISA Known Exploited Vulnerabilities,
  not a representative population of all vulnerabilities.
- The ransomware labels are positive-unlabeled.
- CVSS 4.0 coverage is limited to 115 observations.
- Remediation indicators are extracted from recommendation text.
- Administrative deadlines do not prove patch completion.
- Some engineered variables are correlated or mathematically related.
- Heuristic indices are not calibrated probabilities.

These limitations restrict the conclusions that can be drawn
from predictive experiments.

## 8. Next steps

Before training models:

1. Define each prediction objective separately.
2. Establish a valid target and observation population.
3. Select model-specific feature sets.
4. Audit leakage for each prediction objective.
5. Establish baseline models.
6. Define temporal or other appropriate validation strategies.
7. Compare alternative feature configurations.
8. Document performance, errors and limitations.

No composite multidomain risk score is approved by this audit.

## 9. Audit status

| Validation | Status |
|---|---|
| All dataset columns classified | PASS |
| Unique feature classifications | PASS |
| Duplicate classifications | PASS — none found |
| Unclassified columns | PASS — none found |
| Feature decisions documented | PASS |
| Model-specific selection | PENDING |
| Leakage audit per prediction objective | PENDING |

---

Audit generated: 2026-11-09

Project: Sentinel AI
Dataset: cybersecurity_features_v1.csv
Feature matrix: master_feature_selection_matrix.csv
