# CVSS 4.0 Feature Audit

## Dataset

- Source: NVD
- CVSS version: 4.0
- Records analyzed: 115
- CVSS 4.0-specific metrics: 28

## Core feature assessment

Seven core metrics have complete coverage and observed variation:

- cvss4_attack_requirements
- cvss4_vuln_confidentiality_impact
- cvss4_vuln_integrity_impact
- cvss4_vuln_availability_impact
- cvss4_sub_confidentiality_impact
- cvss4_sub_integrity_impact
- cvss4_sub_availability_impact

All seven are retained as candidate features.

## Experimental metrics

The following metrics contain some values other than NOT_DEFINED,
but have limited coverage:

- cvss4_automatable: 21 records (18.26%)
- cvss4_provider_urgency: 19 records (16.52%)
- cvss4_exploit_maturity: 15 records (13.04%)
- cvss4_value_density: 15 records (13.04%)
- cvss4_recovery: 13 records (11.30%)
- cvss4_vulnerability_response_effort: 12 records (10.43%)
- cvss4_safety: 1 record (0.87%)

They are retained for further investigation, not yet selected
for the primary feature set.

## Undefined metrics

Fourteen metrics contain only NOT_DEFINED values in the
115-record sample. They are excluded provisionally from the
candidate feature set because they have no observed variation.

NOT_DEFINED is an explicit CVSS value and is not equivalent
to a missing value.

## Association analysis

Strong associations were observed among subsequent-system
impact metrics:

- Subsequent integrity vs availability: Cramer's V = 0.858
- Subsequent confidentiality vs integrity: Cramer's V = 0.855
- Subsequent confidentiality vs availability: Cramer's V = 0.836

Associations were also observed among vulnerable-system impacts:

- Integrity vs availability: Cramer's V = 0.638
- Confidentiality vs availability: Cramer's V = 0.540
- Confidentiality vs integrity: Cramer's V = 0.456

These results indicate potential redundancy, but do not justify
automatic feature removal. All seven core metrics remain
provisionally retained.

## Methodological limitations

- Sample size is limited to 115 CVSS 4.0 records.
- Selected CVSS 4.0 assessments are Secondary assessments.
- Some categorical combinations may have low expected counts.
- CVSS base score is calculated from CVSS metrics. Comparisons
  against the base score are descriptive, not independent
  predictive validation.
- Association does not imply causation.
- Feature selection and encoding require validation on
  training data only.

## Current decision

Retain seven core metrics as candidate features.
Keep seven partially populated metrics experimental.
Exclude fourteen constant NOT_DEFINED metrics provisionally.
Reassess redundancy during model development.
