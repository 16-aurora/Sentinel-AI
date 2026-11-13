# Positive-Unlabeled Learning Methodology

## 1. Problem Definition

The CISA KEV dataset contains:
- 361 records labeled Known.
- 1,407 records labeled Unknown.

Unknown does not mean confirmed negative. It means that
known ransomware campaign use has not been confirmed.

Therefore, conventional binary classification may introduce
incorrect assumptions about the negative class.

## 2. Positive-Unlabeled Learning

Positive-Unlabeled (PU) learning uses:
- Positive labeled examples.
- Unlabeled examples that may contain both positive
  and negative instances.

This setting is more appropriate for the current
CISA ransomware label structure.

## 3. Labeling Mechanism Assumptions

### SCAR
Selected Completely At Random assumes that positive
instances are labeled independently of their features.

### SAR
Selected At Random allows the probability of receiving
a positive label to depend on observable characteristics.

Neither assumption has been established for this dataset.

## 4. Preliminary Dataset Evidence

The observed proportion of Known records varies over time:

- 2021: 27.01%
- 2022: 23.78%
- 2023: 22.99%
- 2024: 23.66%
- 2025: 12.65%
- 2026: 9.51%

Known records also have a higher average catalog age
than Unknown records.

These observations suggest potential temporal
labeling bias. They do not prove a SAR mechanism.

## 5. Methodological Risks

- Unknown records must not automatically be treated
  as confirmed negatives.
- The positive class prior is currently unknown.
- The labeling mechanism must be investigated.
- Temporal effects may distort model evaluation.
- Conventional accuracy, precision and recall cannot
  be interpreted as true classification performance
  without appropriate evaluation labels or assumptions.

## 6. Proposed Research Direction

1. Investigate the CISA labeling mechanism.
2. Assess whether SCAR is plausible.
3. Investigate possible SAR behavior.
4. Research positive class prior estimation.
5. Compare appropriate PU learning approaches.
6. Define a defensible evaluation strategy.
7. Only then implement and evaluate a PU model.

## 7. References

Bekker, J. and Davis, J. (2020).
Learning from positive and unlabeled data: a survey.
Machine Learning, 109, 719-760.
https://doi.org/10.1007/s10994-020-05877-5

Jain, S. et al. (2020).
Class Prior Estimation with Biased Positives and
Unlabeled Examples.
AAAI Conference on Artificial Intelligence.
https://doi.org/10.1609/aaai.v34i04.5848

## 8. Current Conclusion

PU learning is a promising research direction for
Sentinel AI. However, no PU algorithm has yet been
selected or validated for this dataset.

## Vendor-Level Labeling Heterogeneity Analysis

### Objective

Investigate whether the observed ransomware positive-label rate varies across vendors, providing preliminary evidence about potential deviations from the SCAR assumption.

### Methodology

Vendor-level positive-label rates were calculated using CISA KEV records. Only vendors with at least 10 records were included in the initial descriptive analysis.

Wilson 95% confidence intervals were calculated to quantify uncertainty in the observed proportions.

A Pearson chi-square test of independence was then conducted using a contingency table of confirmed positive and unlabeled records across vendors.

Because 14 of the 54 expected cell counts were below 5, a sensitivity analysis was performed using only vendors with at least 25 records.

### Results

**Initial analysis (27 vendors):**
- Chi-square statistic: 190.4566
- Degrees of freedom: 26
- P-value: 5.83 × 10⁻²⁷
- Expected cells below 5: 14 of 54

**Filtered sensitivity analysis (13 vendors):**
- Minimum vendor sample size: 25
- Chi-square statistic: 107.872
- Degrees of freedom: 12
- P-value: 1.58 × 10⁻¹⁷
- Minimum expected cell count: 5.17
- Expected cells below 5: 0

### Interpretation

The filtered analysis provides strong statistical evidence that observed positive-label proportions are not homogeneous across the selected vendors.

This finding motivates further investigation of the labeling mechanism and potential SAR (Selected At Random) behavior.

However, vendor-level heterogeneity does not independently establish that SCAR is violated. Differences in vulnerability composition, exposure, reporting, and evidence availability may also contribute to the observed variation.

The analysis concerns observed CISA labels, not the true prevalence of ransomware-related vulnerabilities.

### Limitations

- Vendor sample sizes remain unequal.
- The analysis is restricted to vendors with at least 25 records in the sensitivity test.
- Multiple comparisons and potential confounding factors have not yet been investigated.
- Statistical association does not establish the causal mechanism behind labeling.

### Conclusion

Vendor-level heterogeneity is a significant methodological concern for conventional supervised learning.

The results support investigating feature-dependent labeling mechanisms before selecting and evaluating a PU learning approach.

## Year-Adjusted Vendor Association: Cochran-Mantel-Haenszel Analysis

### Objective

Investigate whether the observed association between Microsoft vulnerabilities and confirmed ransomware labels persists after controlling for the year in which vulnerabilities were added to the CISA KEV catalog.

### Methodology

A Cochran-Mantel-Haenszel (CMH) test was performed using six yearly strata (2021–2026).

Within each year, records were divided into two groups:
- Microsoft vulnerabilities.
- Vulnerabilities associated with all other vendors.

The outcome consisted of confirmed positive labels (`Known`) versus unlabeled records (`Unknown`).

### Results

- Years analyzed: 2021–2026.
- Stratified odds ratio: 1.843.
- CMH statistic: 20.703.
- P-value: 5.36 × 10⁻⁶.

### Interpretation

The observed association between Microsoft records and confirmed ransomware labels remains statistically significant after stratification by year.

The pooled odds ratio indicates approximately 1.84 times higher odds of observing a `Known` label for Microsoft vulnerabilities compared with vulnerabilities from other vendors, conditional on the yearly strata.

This result suggests that temporal differences alone do not explain the observed vendor association.

### Limitations

- The comparison groups Microsoft against all other vendors combined.
- Residual confounding may remain within each year.
- The analysis concerns observed labels, not true ransomware prevalence.
- The result does not independently establish a SAR labeling mechanism or disprove SCAR.

### Conclusion

Vendor-level and temporal heterogeneity should be considered when designing the PU learning methodology. Further investigation is required to characterize the labeling mechanism and assess the robustness of these associations.

## Vulnerability Age and Temporal Label Analysis

### Age category and observed label rates

The observed ransomware label rates differed across vulnerability age categories:

| Age category | Records | Confirmed positives | Observed label rate |
|---|---:|---:|---:|
| Recent | 106 | 1 | 0.94% |
| Intermediate | 207 | 28 | 13.53% |
| Old | 1,455 | 332 | 22.82% |

A chi-square test found an association between age category and observed
label status (chi-square = 35.9474, df = 2, p = 1.56e-08).
Cramer's V was 0.1426, indicating a modest association.

These results describe observed catalog labels, not the actual probability
of ransomware exploitation. They do not establish a causal relationship
between vulnerability age and ransomware activity.

### Age category by year of addition

The cross-tabulation revealed a strong structural relationship between
the year of addition and the age category:

- 2021–2024: all records were classified as Old.
- 2025: 29 Intermediate and 216 Old records.
- 2026: 178 Intermediate and 106 Recent records.

This distribution indicates that age category and year of addition
cannot be interpreted as independent explanatory variables in this dataset.

### Modeling implications

- Keep vulnerability age features experimental for now.
- Do not interpret age-related label differences as causal effects.
- Investigate temporal effects and potential label-selection mechanisms
  before using age as a predictive feature.
- Treat the CISA Unknown label as unlabeled, not as a confirmed negative.
- Avoid conclusions about actual ransomware prevalence based only on
  observed KEV label proportions.

The analysis is cross-sectional and reflects the catalog snapshot used
in this study. Further temporal validation is required.


## Vendor-Level Temporal Analysis: Cochran-Mantel-Haenszel Test

### Methodology

Cochran-Mantel-Haenszel (CMH) tests were performed to compare the
observed odds of receiving a Known ransomware label for five vendors
against all other vendors, stratifying by year of addition (2021–2026).

Benjamini-Hochberg correction was applied across the five comparisons.

### Results

| Vendor | Pooled odds ratio | CMH statistic | Adjusted p-value |
|---|---:|---:|---:|
| Microsoft | 1.8430 | 20.7030 | 0.00000894 |
| Cisco | 0.2739 | 12.6403 | 0.00047189 |
| Apple | 0.0000 | 29.2199 | 0.00000032 |
| Google | 0.0000 | 22.9301 | 0.00000420 |
| Adobe | 0.5034 | 4.2844 | 0.03846391 |

All five comparisons were statistically significant at the 0.05
threshold after Benjamini-Hochberg correction.

### Interpretation and limitations

- Microsoft showed higher observed odds of a Known label than other vendors.
- Cisco and Adobe showed lower observed odds.
- Apple and Google had no observed positive labels in the analyzed
  vendor-year strata, resulting in pooled odds ratios of zero.
- Complete separation and sparse-data issues require particular caution
  when interpreting Apple and Google results.
- Statistical significance does not establish a causal relationship
  or prove a SAR labeling mechanism.
- The analysis compares observed CISA catalog labels, not actual
  ransomware exploitation rates.
- Stratification controls for year but does not eliminate other
  possible confounding factors.
- Benjamini-Hochberg correction addresses multiple testing but does not
  resolve sparse-data or model-assumption problems.

### Methodological conclusion

The results provide further evidence of heterogeneity in observed
ransomware labeling across vendors after stratification by year.
However, they do not identify the underlying label-selection mechanism.

The findings support continued investigation of potential selection
bias and reinforce the decision to treat Unknown records as unlabeled,
not confirmed negatives.
