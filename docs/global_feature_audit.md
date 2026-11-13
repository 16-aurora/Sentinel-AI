# Sentinel AI — Global Feature Engineering Audit

## 1. Dataset overview

- Dataset: cybersecurity_features_v1 with additional engineered features
- Records: 1,768
- Unique CVEs: 1,768
- Columns audited: 100
- Missing cells: 57,970

The dataset combines CISA KEV records, NVD enrichment,
CVSS metrics and engineered cybersecurity risk features.

## 2. Global column quality

- Constant columns: 3
- Variable columns: 97
- Exact duplicate column pairs: 91
- Duplicate pairs outside constant CVSS 4.0 metrics: 0

The constant columns are:

- `nvd_found`
- `nvd_status`
- `ransomware_label_available`

They are retained for data provenance and quality control,
but excluded from the initial predictive feature candidates.

## 3. CVSS 4.0 audit

There are 115 CVSS 4.0 records and 1,653 records without
CVSS 4.0 assessments.

Fourteen CVSS 4.0 metrics were constant across the observed
CVSS 4.0 records, with the value NOT_DEFINED.

These fourteen columns generated exactly 91 pairwise
duplicate combinations:

14 * 13 / 2 = 91.

Validation confirmed:

- Expected pairs: 91
- Actual pairs: 91
- Pairs among constant columns: 91
- Other exact duplicate pairs: 0

The seven encoded core CVSS 4.0 features are retained as
candidate model features. Original categorical fields are
preserved for interpretation and traceability.

Missing CVSS 4.0 values are structural: only 115 records
have CVSS 4.0 assessments. They must not be imputed as zero.

## 4. Severity and technical impact

CVSS base score and normalized severity are equivalent
representations. Only one should be used in an individual
model experiment.

The technical impact index is derived from confidentiality,
integrity and availability impact components.

The index has a ceiling effect: 1,382 records (78.17%)
have the maximum value of 1.0.

Both the aggregate index and individual components are
preserved for comparative model experiments.

Attack feasibility is treated as a separate heuristic
dimension, not as an attack probability.

## 5. Temporal features

The initial temporal candidate features are:

- `vulnerability_age_days`
- `days_overdue`
- `original_remediation_window`

`days_until_due` and `deadline_overdue` are excluded
provisionally from the initial candidate set due to
redundancy with days overdue.

The reference date used for these engineered features
was 2026-11-09.

A remediation deadline does not prove whether a vulnerability
has actually been patched.

## 6. Remediation features

Initial remediation candidates:

- `action_apply_updates`
- `action_apply_mitigations`
- `action_discontinue_product`
- `action_eol_eos`
- `action_security_assessment`

The combined security assessment indicator is the logical
union of exposure assessment and forensic investigation.

`action_cisa_directive` is a subset of `action_apply_mitigations`
in this dataset and is excluded from the initial independent
candidate set.

`action_disconnect_product` is a subset of `action_eol_eos`
and is excluded from the initial candidate set.

`active_remediation_indicators` exactly equals the sum of
the eight original remediation binary indicators across
all 1,768 records. It is preserved as an alternative
aggregate feature, not combined automatically with all
individual indicators.

Textual remediation indicators represent mentions in
recommendations, not verified completed actions.

## 7. Ransomware label limitations

`ransomware_known` represents known ransomware campaign use.

Unknown records are unlabeled, not confirmed negatives.
The dataset is therefore treated as a positive-unlabeled
learning context rather than ordinary binary classification.

`ransomware_label_available` is constant and is not a
predictive feature.

## 8. General feature selection principles

- Preserve original source fields for traceability.
- Exclude constant features from model inputs.
- Avoid exact duplicate and highly redundant predictors.
- Compare aggregate and component representations experimentally.
- Do not impute structurally unavailable CVSS 4.0 values as zero.
- Fit transformations and encoders on training data only.
- Avoid target leakage and use time-aware validation where appropriate.
- Treat heuristic indices as engineered indicators, not calibrated probabilities.

## 9. Current status

The global inventory and duplicate-column audit are complete.

Feature selection remains provisional until model-specific
experiments establish which representations provide useful
predictive information.
