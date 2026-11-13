
# Repeated Vendor-Group Validation

## Objective

Evaluate whether PU Bagging models generalize to previously
unseen vendors using five independent group-based partitions.

## Experimental configuration

- Models: Random Forest and Extra Trees
- PU Bagging iterations: 50
- Trees per iteration: 200
- Random state: 42
- Five vendor-group partitions
- Vendor overlap between training and validation: 0

## Results

| Metric | Random Forest | Extra Trees |
|---|---:|---:|
| Mean score separation | 0.0084 | 0.0049 |
| Mean global ROC-AUC | 0.5406 | 0.5120 |
| Mean global Average Precision | 0.2855 | 0.2866 |
| Mean macro vendor ROC-AUC | 0.6937 | 0.6423 |
| Mean training time (seconds) | 17.5592 | 13.2414 |

## Interpretation

Random Forest achieved higher mean global ROC-AUC,
score separation and macro vendor ROC-AUC.

Extra Trees achieved slightly higher mean global
Average Precision and shorter training time.

Both models showed weak global score separation
and variability across vendor partitions.

The macro vendor ROC-AUC was calculated only for vendors
containing both observed label groups in each validation split.

## Limitations

- CISA ransomware labels are positive-unlabeled labels.
- Unlabeled records are not confirmed negative examples.
- Evaluation metrics measure association with observed labels.
- Five partitions are not five independent datasets.
- Vendor composition differs between partitions.
- Macro metrics cover only eligible vendors.
- Scores are not calibrated probabilities of ransomware risk.

## Conclusion

Random Forest is the more promising candidate in this
repeated vendor-group experiment, but generalization
to unseen vendors remains limited and requires further study.

No definitive model selection is made at this stage.
