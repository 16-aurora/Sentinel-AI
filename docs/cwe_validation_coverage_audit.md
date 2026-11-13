# Sentinel AI
# CWE Validation Coverage Audit

## 1. Purpose

Evaluate the coverage of the CWE multi-label encoder
when transforming validation observations.

The encoder vocabulary is fitted exclusively on training data.

## 2. Dataset and encoder

| Metric | Result |
|---|---:|
| Training observations | 1414 |
| Validation observations | 354 |
| CWE classes learned in training | 180 |
| Validation CWE occurrences | 339 |
| Unknown CWE occurrences | 22 |
| Validation rows containing unknown CWE | 22 |

## 3. Coverage

Known-category coverage:

**93.51%**

Unknown occurrence rate:

**6.49%**

Rows affected:

**6.21%**

Coverage is calculated over individual CWE occurrences.
It does not represent the percentage of complete observations
whose entire CWE set is known.

## 4. Unknown CWE categories

- CWE-191: 2
- CWE-25: 2
- CWE-707: 2
- CWE-259: 2
- CWE-706: 1
- CWE-254: 1
- CWE-647: 1
- CWE-645: 1
- CWE-497: 1
- CWE-197: 1
- CWE-39: 1
- CWE-91: 1
- CWE-913: 1
- CWE-601: 1
- CWE-357: 1
- CWE-782: 1
- CWE-1321: 1
- CWE-424: 1

Total unknown categories: 18

## 5. Encoding decision

The encoder vocabulary is learned exclusively from training data.

CWE categories that appear only in validation are not added
to the fitted vocabulary.

Known CWE labels in a multi-label observation are retained,
even when another label in the same observation is unknown.

Unknown labels are ignored during transformation and counted
in this audit.

## 6. Limitations

- Validation observations may contain CWE categories absent
  from training.
- Unknown categories are not represented in the encoded matrix.
- This may reduce information available for those observations.
- The coverage estimate depends on the current train/validation
  split and random seed.
- A different split may produce different coverage.

## 7. Validation status

- CWE parsing corrected: PASS
- Training-only vocabulary: PASS
- Malformed CWE labels: NONE DETECTED
- Validation coverage measured: PASS
- Unknown categories documented: PASS

## 8. Next steps

Evaluate the complete preprocessing pipeline, document its
configuration and establish reproducible transformation
artifacts before model experimentation.

No model performance conclusions are drawn from this audit.
