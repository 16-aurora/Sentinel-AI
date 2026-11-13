# Sentinel AI — Cybersecurity Feature Design

## 1. Domain objective

Identify, characterize and prioritize cybersecurity risks using vulnerability intelligence from the CISA Known Exploited Vulnerabilities (KEV) catalog.

## 2. Feature dimensions

| Dimension | Variables | Purpose |
|---|---|---|
| Temporal | days_since_added, added_year, added_month, added_quarter | Measure vulnerability age and temporal patterns |
| Remediation urgency | days_until_due, deadline_overdue, days_past_due, deadline_urgency | Prioritize remediation deadlines |
| Exploitation | ransomware_known | Identify vulnerabilities associated with known ransomware campaigns |
| Technical impact | cwes, vulnerabilityName, shortDescription | Characterize vulnerability weaknesses |
| Technology exposure | vendorProject, product | Identify affected vendors and products |
| Remediation guidance | requiredAction, forensicTriage, has_forensic_triage | Analyze recommended mitigation and triage information |

## 3. Data sources

- CISA Known Exploited Vulnerabilities (KEV) catalog.
- Future integration: NVD vulnerability database.

## 4. Important limitations

- KEV inclusion indicates known exploitation, not the probability of a future attack.
- The catalog does not establish whether a specific organization's systems are exposed or patched.
- Vendor ransomware rates describe the observed KEV records, not the overall security of a vendor.
- Remediation deadlines do not confirm whether remediation has been completed.

## 5. Future engineering tasks

- Define model-specific feature sets.
- Evaluate categorical encoding strategies.
- Design time-aware features.
- Prevent target leakage.
- Integrate cybersecurity features with climate and economic indicators.

## 6. Current status

Initial cybersecurity feature design based on the CISA KEV dataset. Further validation and refinement required before model training.