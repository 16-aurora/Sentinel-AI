# Sentinel AI
# Ransomware Intelligence — Feature Readiness Audit

## 1. Purpose

Evaluate the initial suitability of the 16 candidate features
for the ransomware intelligence experiment.

## 2. Audit results

- Total candidate features: 16
- CANDIDATE: 11
- ALTERNATIVE: 3
- REVIEW: 2

### Risk distribution

- LOW: 2
- MEDIUM: 13
- HIGH: 1

## 3. Important decisions

### Severity

`severity_normalized` is the initial continuous severity
candidate. `technical_severity` is retained as an alternative.

### Attack feasibility

The four individual heuristic components are candidates.
`attack_feasibility_index` is an alternative aggregate.

The index is heuristic and must not be interpreted as an
empirically calibrated exploitation probability.

### Technical impact

The three individual impact components are candidates.
`technical_impact_index` is an alternative aggregate.

Avoid combining the aggregate and all its components without
a specific experimental justification.

### Temporal features

`vulnerability_age_days` is marked REVIEW due to its dependence
on a fixed reference date and potential temporal leakage.

`original_remediation_window` is also marked REVIEW until
point-in-time availability is established.

Neither variable is approved for the initial experiment.

### Categorical features

Vendor, product and CWE variables require suitable encoding.
Encoding must be fitted on training data only.

## 4. Target safeguards

The target is positive-unlabeled:

- Known: 361
- Unknown: 1,407

Unknown observations are not confirmed negatives.

The target and its original source field must never be included
as predictor variables.

## 5. Limitations

This audit establishes preliminary feature readiness only.
It does not establish causal relevance, predictive performance
or final model suitability.

The current dataset contains CISA KEV vulnerabilities only.
It does not represent the complete population of vulnerabilities.

## 6. Validation

All 16 initial candidate features have been reviewed.
No candidate was omitted from the readiness audit.

Model-specific selection and leakage checks remain pending.
