# Sentinel AI — CISA KEV Exploratory Data Analysis Report

**Project:** Sentinel AI — Multidomain Risk Intelligence & Early Warning System  
**Dataset:** CISA Known Exploited Vulnerabilities (KEV) Catalog  
**Catalog version:** 2026.11.04  
**Analysis date:** November 6, 2026  
**Records analyzed:** 1,768

---

## 1. Executive Summary

This report presents the exploratory data analysis (EDA) performed on the CISA Known Exploited Vulnerabilities (KEV) catalog.

The objective was to understand the distribution, characteristics, temporal patterns and remediation context of known exploited vulnerabilities.

The analysis identified relevant patterns involving affected vendors, products, ransomware campaign usage, vulnerability classifications and remediation deadlines.

The findings will help guide future feature engineering, machine learning experimentation and risk intelligence development.

## 2. Dataset Overview

The dataset contains:

- 1,768 vulnerability records.
- 17 columns.
- 291 distinct vendors.
- 713 distinct products.
- 1,421 distinct vulnerability names.

The original dataset was obtained from the official CISA KEV catalog.

Official source: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

## 3. Key Findings

### 3.1 Vendor Distribution

Microsoft was the most frequently represented vendor, with 390 vulnerabilities.

Other highly represented vendors included:

- Cisco: 102
- Apple: 96
- Adobe: 83
- Google: 76

These figures represent catalog records, not the overall security quality of each vendor.

### 3.2 Ransomware Campaign Usage

The dataset contains:

- Known: 361 vulnerabilities (20.4%).
- Unknown: 1,407 vulnerabilities (79.6%).

Unknown indicates that CISA does not confirm known ransomware campaign usage. It does not establish that ransomware exploitation has never occurred.

### 3.3 Vendor Ransomware Distribution

Microsoft had the largest absolute number of vulnerabilities marked as Known, with 117 records.

When comparing proportions among vendors with at least five records, the highest observed rates included:

- QNAP: 81.8% (9 of 11).
- RARLAB: 80.0% (4 of 5).
- Mitel: 71.4% (5 of 7).
- SonicWall: 68.4% (13 of 19).
- Atlassian: 57.1% (8 of 14).

These are descriptive proportions within the KEV dataset, not probabilities of attack or measures of vendor-wide security.

### 3.4 Temporal Distribution

Vulnerabilities added by year:

| Year | Records |
|---|---:|
| 2021 | 311 |
| 2022 | 555 |
| 2023 | 187 |
| 2024 | 186 |
| 2025 | 245 |
| 2026 | 284 |

2022 was the year with the highest number of additions.

The 2026 dataset is incomplete because the analysis was performed on November 6, 2026.

### 3.5 Monthly Distribution

The monthly analysis identified September 2026 as the highest month among the last twelve months analyzed, with 43 additions.

November 2026 contained only two records at the time of analysis and must be treated as an incomplete month.

### 3.6 Affected Products

Windows was the most frequently represented product, with 173 records.

Other prominent products included:

- Multiple Products: 87.
- Chromium V8: 41.
- Internet Explorer: 36.
- Kernel: 35.
- Flash Player: 33.

### 3.7 Common Weakness Enumeration (CWE)

The most frequent CWE identifiers included:

| CWE | Occurrences |
|---|---:|
| CWE-20 | 119 |
| CWE-78 | 113 |
| CWE-787 | 106 |
| CWE-416 | 95 |
| CWE-119 | 88 |
| CWE-22 | 82 |
| CWE-94 | 72 |
| CWE-502 | 71 |
| CWE-287 | 49 |
| CWE-306 | 43 |

These counts represent CWE occurrences. A vulnerability may be associated with more than one weakness.

### 3.8 Remediation Recommendations

The most common CISA recommendation was to apply vendor updates, appearing in 893 records.

Other frequent recommendations involved applying vendor mitigations or discontinuing products when appropriate mitigations were unavailable.

### 3.9 Remediation Deadlines

As of November 6, 2026:

- 1,762 records had deadlines earlier than the reference date.
- 6 records had deadlines on or after the reference date.

An overdue catalog deadline does not establish whether an organization has failed to patch a vulnerability. The dataset does not provide organization-level remediation status.

### 3.10 Textual Analysis

An initial keyword analysis of vulnerability descriptions identified frequent terms including:

- remote
- code
- attacker
- execution
- arbitrary
- unauthenticated
- privileges
- memory
- injection

These terms suggest recurring technical themes and provide an initial foundation for future NLP experiments.

The keyword analysis is exploratory and does not constitute a validated vulnerability classification model.

## 4. Data Quality Assessment

The final exploratory audit reported:

| Check | Result |
|---|---:|
| Total records | 1,768 |
| Total columns | 17 |
| Missing values | 0 |
| Duplicate CVE identifiers | 0 |
| Invalid `dateAdded` values | 0 |
| Invalid `dueDate` values | 0 |

The `has_forensic_triage` feature was corrected and validated against the original categorical field:

- No: 1,671 records.
- Yes: 97 records.

The feature was encoded as:

- 0 = No.
- 1 = Yes.

## 5. Limitations

The following limitations must be considered:

1. CISA KEV is a curated catalog and does not represent every known vulnerability.
2. Vendor and product counts do not measure overall vendor security.
3. Unknown ransomware status must not be interpreted as confirmed absence of ransomware usage.
4. The dataset does not establish whether individual organizations have applied patches.
5. Vendor proportions can be unstable when based on small samples.
6. Annual and monthly comparisons must account for incomplete periods.
7. Keyword frequencies do not establish semantic relationships or predictive capability.
8. The analysis is based on one cybersecurity source and does not yet incorporate climate or economic information.

## 6. Conclusions

The exploratory analysis identified meaningful patterns in the CISA KEV catalog and confirmed that the dataset provides useful information for further cybersecurity research.

The findings highlight the importance of distinguishing absolute vulnerability counts from proportions, preserving uncertainty in ransomware classifications and considering remediation deadlines in their correct context.

The processed dataset and engineered features provide an initial foundation for the next development stages of Sentinel AI.

## 7. Next Steps

The next project activities will include:

1. Consolidating and validating processed datasets.
2. Expanding feature engineering.
3. Integrating additional cybersecurity, climate and economic data sources.
4. Designing explainable risk indicators.
5. Exploring machine learning and NLP approaches.
6. Developing a multidomain risk correlation engine.

---

**Sentinel AI — Multidomain Risk Intelligence & Early Warning System**