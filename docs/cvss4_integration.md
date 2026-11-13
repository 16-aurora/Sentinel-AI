# CVSS 4.0 Feature Integration

## Objective

Integrate seven encoded CVSS 4.0 features into the complete
cybersecurity dataset using cveID as the unique identifier.

## Input datasets

- data/processed/cybersecurity_integrated_v2.csv
- data/processed/cvss4_encoded_features.csv

## Integration method

- Join key: cveID
- Join type: left join
- Validation: one-to-one
- Original dataset records: 1,768
- CVSS 4.0 records: 115

## Added features

1. cvss4_attack_requirements_encoded
2. cvss4_vuln_confidentiality_impact_encoded
3. cvss4_vuln_integrity_impact_encoded
4. cvss4_vuln_availability_impact_encoded
5. cvss4_sub_confidentiality_impact_encoded
6. cvss4_sub_integrity_impact_encoded
7. cvss4_sub_availability_impact_encoded

## Validation results

- Final records: 1,768
- Unique CVEs: 1,768
- Matched CVSS 4.0 records: 115
- Unmatched original records: 1,653
- Duplicate CVEs: 0
- Feature value comparisons: 805
- Mismatches: 0

The 1,653 records without CVSS 4.0 metrics retain missing
values in the seven new columns. These values were not imputed.

## Data type consideration

Integer encoded features become float64 after integration
because missing values must be represented in the resulting
columns. This does not indicate a change in the matched
numerical values.

## Output

data/processed/cybersecurity_features_v1.csv

- Records: 1,768
- Columns: 68
- Unique CVEs: 1,768

## Limitations

- CVSS 4.0 coverage is limited to 115 records.
- The encoded variables are candidate model features.
- Their predictive usefulness has not yet been established.
- Feature transformations must be handled carefully during
  model training to prevent data leakage.
