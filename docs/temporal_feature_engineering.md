# Sentinel AI — Temporal Feature Engineering

## Reference date

All temporal features in this analysis use the fixed reference date
2026-11-09 to ensure reproducibility.

## Features created

- vulnerability_age_days: Days since the vulnerability was added to CISA KEV.
- days_until_due: Days remaining until the CISA remediation deadline.
- remediation_urgency: Administrative deadline urgency category.
- deadline_overdue: Binary indicator that the administrative deadline has passed.
- days_overdue: Number of days elapsed since the administrative deadline.
- overdue_age_category: Categorization of administrative deadline delay.
- original_remediation_window: Days between dateAdded and dueDate.

## Remediation window validation

The original remediation window was validated against the difference
between dateAdded and dueDate.

All 1,763 overdue records matched exactly.

The remediation window contains 17 distinct values.
Its mean is approximately 41.27 days and its median is 21 days.

## Redundancy analysis

Spearman correlation between vulnerability_age_days and days_overdue:
0.9488.

The difference between these variables equals the original remediation
window for all 1,763 overdue records.

Therefore, age_delay_difference is not retained as an independent
predictive feature.

## Relationship with technical severity

Spearman correlation between original_remediation_window and CVSS:
- All records: -0.0800 (p = 0.000759).
- Four main windows: -0.0634 (p = 0.008985).

These associations are statistically significant but very weak.

## Methodological limitations

- CISA remediation deadlines are administrative deadlines.
- An overdue deadline does not prove that a vulnerability remains unpatched.
- Vulnerability age and days overdue share a common temporal reference.
- The remediation window should not be interpreted as a direct risk score.
- Correlation does not establish causality.
- The fixed reference date must be reconsidered for future production use.