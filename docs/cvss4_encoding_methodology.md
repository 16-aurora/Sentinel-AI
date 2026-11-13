# CVSS 4.0 Categorical Feature Encoding

## Objective

Transform seven categorical CVSS 4.0 metrics into numerical
features while preserving the original categorical variables.

## Dataset

- Records: 115
- Original categorical features: 7
- Encoded features: 7
- Missing encoded values: 0

## Encoding strategy

### Attack requirements

| Category | Encoded value |
|---|---:|
| NONE | 0 |
| PRESENT | 1 |

### Impact metrics

| Category | Encoded value |
|---|---:|
| NONE | 0 |
| LOW | 1 |
| HIGH | 2 |

The impact mapping represents an ordinal ordering.
It does not establish equal mathematical distances between
categories.

## Encoded features

- cvss4_attack_requirements_encoded
- cvss4_vuln_confidentiality_impact_encoded
- cvss4_vuln_integrity_impact_encoded
- cvss4_vuln_availability_impact_encoded
- cvss4_sub_confidentiality_impact_encoded
- cvss4_sub_integrity_impact_encoded
- cvss4_sub_availability_impact_encoded

## Validation

The encoding passed a reversibility test:

- Original records: 115
- Encoded records: 115
- Features reconstructed successfully: 7 of 7
- Reconstruction mismatches: 0

Original categorical columns were preserved.

## Methodological considerations

- The encoded features are candidate model inputs, not
  automatically validated predictive features.
- Ordinal encoding imposes an ordering on categories.
- One-Hot Encoding should be considered as an alternative
  during model experimentation.
- Transformations must be fitted within the training pipeline
  when applicable to avoid data leakage.
- The sample contains only 115 CVSS 4.0 records.
- All selected CVSS 4.0 assessments in this dataset are
  Secondary assessments.
- Feature usefulness must be evaluated during model validation.

## Output

data/processed/cvss4_encoded_features.csv
