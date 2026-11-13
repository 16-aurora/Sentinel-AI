# Sentinel AI
# Machine Learning Objectives — Cybersecurity

## 1. Purpose

Define the initial analytical and machine learning objectives
for the cybersecurity domain of Sentinel AI.

No model training is performed at this stage.

Each objective must have a clearly defined target, suitable
input features, evaluation strategy and documented limitations.

## 2. Objective A — Ransomware Intelligence

### Research question

Which observable vulnerability characteristics are associated
with CISA's known ransomware campaign-use labels?

### Target

- Variable: ransomware_known
- Positive observations: 361
- Unlabeled observations: 1,407

### Learning approach

Positive-Unlabeled Learning (PU Learning).

Unknown observations must not be treated as confirmed negatives.

### Candidate input groups

- CVSS severity and technical characteristics.
- Attack feasibility.
- Temporal characteristics.
- Vendor and product information.
- CWE categories, subject to suitable encoding.

### Exclusions and safeguards

- Never include ransomware_known as an input feature.
- Never include knownRansomwareCampaignUse as an input feature.
- Review temporal and source-related leakage.
- Do not interpret model output as a calibrated probability
  without appropriate calibration and validation.

### Initial status

RESEARCH DESIGN — PENDING IMPLEMENTATION.

## 3. Objective B — Vulnerability Profiling

### Research question

Can vulnerabilities be grouped according to their technical
severity, impact and attack characteristics?

### Analytical variables

- CVSS base score and severity.
- Attack vector.
- Attack complexity.
- Privileges required.
- User interaction.
- Confidentiality impact.
- Integrity impact.
- Availability impact.
- Attack feasibility index.

### Learning approach

Exploratory analysis and unsupervised learning.

Potential methods:

- K-Means.
- Hierarchical clustering.
- DBSCAN.
- Principal Component Analysis (PCA), if appropriate.

### Safeguards

- Avoid mixing redundant representations without justification.
- Compare component-based and aggregate feature sets.
- Evaluate cluster stability and interpretability.
- Do not describe clusters as confirmed attack probabilities.

### Initial status

RESEARCH DESIGN — PENDING IMPLEMENTATION.

## 4. Objective C — Remediation Intelligence

### Research question

What patterns exist in the remediation recommendations
published by CISA?

### Candidate variables

- action_apply_updates
- action_apply_mitigations
- action_discontinue_product
- action_eol_eos
- action_security_assessment

### Learning approach

Exploratory analysis, descriptive statistics and potentially
unsupervised grouping of remediation profiles.

### Safeguards

These variables describe textual recommendations.
They do not confirm that remediation was performed.

The dataset does not provide verified patch completion
or organizational remediation outcomes.

### Initial status

EXPLORATORY DESIGN — PENDING IMPLEMENTATION.

## 5. Cross-objective safeguards

1. Define separate datasets and feature sets for each objective.
2. Exclude identifiers and target variables from predictors.
3. Prevent target leakage and temporal leakage.
4. Fit preprocessing transformations on training data only.
5. Preserve structural missingness in CVSS 4.0 variables.
6. Establish baseline methods before complex models.
7. Document validation methodology and limitations.
8. Do not infer causal relationships from observational patterns.
9. Avoid presenting heuristic indices as calibrated probabilities.

## 6. Current project boundaries

The current cybersecurity dataset consists of CISA KEV
vulnerabilities enriched with NVD information.

It is not a representative sample of all vulnerabilities.

Consequently, these objectives focus on vulnerability
characterization and patterns within the available dataset.

Predicting whether an arbitrary vulnerability will enter
the CISA KEV catalog would require an appropriate population
of vulnerabilities outside the KEV catalog.

## 7. Implementation status

| Objective | Status |
|---|---|
| A — Ransomware Intelligence | Design pending implementation |
| B — Vulnerability Profiling | Design pending implementation |
| C — Remediation Intelligence | Design pending implementation |
| Model-specific feature selection | Pending |
| Baseline models | Pending |
| Evaluation protocols | Pending |
| Model training | Not started |

