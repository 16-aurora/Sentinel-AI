# Sentinel AI
# Positive-Unlabeled Learning — Experimental Protocol

## 1. Research objective

Investigate whether vulnerability characteristics can help
distinguish CISA KEV records associated with known ransomware
campaign use from the remaining unlabeled observations.

The scope is restricted to the CISA KEV dataset.

This experiment does not aim to estimate ransomware risk across
the entire CVE population.

## 2. Available labels

- Positive observations: 361
- Unlabeled observations: 1,407
- Total observations: 1,768

The CISA label "Unknown" is not interpreted as a confirmed negative.

## 3. Learning paradigm

The problem is formulated as Positive-Unlabeled (PU) learning.

Two label-selection assumptions will be considered:

### SCAR — Selected Completely At Random

Assumes that positive observations have the same probability
of being labeled, independently of their characteristics.

This assumption is useful as a theoretical baseline but has
not been established for this dataset.

### SAR — Selected At Random

Allows the probability of receiving a positive label to depend
on observed characteristics.

This is a relevant alternative because reporting and detection
may differ across vendors, products and vulnerability types.

Neither assumption is confirmed at this stage.

## 4. Candidate experimental approach

PU Bagging will be investigated as an initial experimental
approach.

The proposed procedure will repeatedly sample observations
from the unlabeled pool as provisional negatives and combine
the resulting models.

These provisional negatives are not confirmed negative cases.

## 5. Class-prior sensitivity

The observed positive proportion is:

361 / 1768 = 20.42%

This is not an estimate of the true positive class prior.

Experiments will consider hypothetical class-prior scenarios
and assess how conclusions change under different assumptions.

## 6. Evaluation principles

- Do not treat unlabeled observations as confirmed negatives.
- Do not interpret ordinary binary classification accuracy
  as true predictive accuracy.
- Distinguish observed-label enrichment from actual precision.
- Evaluate ranking stability across experimental repetitions.
- Compare sensitivity across class-prior scenarios.
- Document selection bias and dataset limitations.
- Avoid interpreting model scores as calibrated probabilities.

## 7. Data and leakage safeguards

- Fit preprocessing transformations on training data only.
- Do not use ransomware labels as predictors.
- Preserve the distinction between positive and unlabeled cases.
- Investigate temporal and vendor-related selection effects.
- Avoid using information unavailable at the intended prediction time.

## 8. Current status

Experimental protocol drafted.

No PU model has been trained.

No predictive performance has been established.

The next stage is to define the experimental design,
baseline and evaluation procedure before model fitting.
