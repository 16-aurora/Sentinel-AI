# Sentinel AI - Economic Risk Engine V1

## 1. Overview

The Economic Risk Engine V1 is a heuristic scoring component
designed to identify potentially adverse economic conditions
across the 27 European Union member states.

The analysis covers 2015-2025 using World Bank indicators.

The engine produces country-year economic exposure scores.
It does not estimate crisis probabilities or predict recessions.

## 2. Data Sources

Source: World Bank API.

Indicators:

| Indicator | World Bank Code |
|---|---|
| GDP growth | NY.GDP.MKTP.KD.ZG |
| Inflation | FP.CPI.TOTL.ZG |
| Unemployment | SL.UEM.TOTL.ZS |
| GDP per capita | NY.GDP.PCAP.KD |

GDP per capita is transformed into year-over-year percentage
growth for anomaly analysis.

The resulting panel contains 27 countries and 11 years.

## 3. Anomaly Detection

Country-specific Z-scores are calculated using the historical
observations available for each indicator.

Thresholds:

- High anomaly: absolute Z-score >= 2.
- Moderate anomaly: absolute Z-score >= 1.5.
- Normal: absolute Z-score < 1.5.

For adverse signals, direction matters:

- GDP growth: unusually low values.
- GDP per capita growth: unusually low values.
- Inflation: unusually high values.
- Unemployment: unusually high values.

These are retrospective statistical signals, not live forecasts.

## 4. Risk Dimensions

The engine combines three dimensions:

| Dimension | Weight |
|---|---:|
| Economic growth deterioration | 40% |
| Inflation pressure | 30% |
| Unemployment pressure | 30% |

GDP growth and GDP per capita growth are highly correlated
in the analyzed sample (Pearson r = 0.9864).

To reduce double counting, the growth dimension uses the
strongest adverse component instead of summing both scores.

## 5. Component Scoring

The adverse threshold is 1.5 standard deviations.

The component score is:

- 0 when the observation does not cross the adverse threshold.
- Otherwise, the absolute adverse Z-score divided by 3,
  multiplied by 100.
- Scores are capped at 100.

For growth, adverse direction is negative.
For inflation and unemployment, adverse direction is positive.

## 6. Aggregation

The final score is the weighted average of available dimensions.

If a dimension is unavailable, the remaining weights are
renormalized proportionally.

The resulting score ranges from 0 to 100.

## 7. Risk Categories

| Score | Category |
|---|---|
| 0-24.99 | Low |
| 25-49.99 | Moderate |
| 50-74.99 | High |
| 75-100 | Critical |

These thresholds are initial heuristic design choices.

## 8. Sensitivity Analysis

Four weight configurations were evaluated:

| Scenario | Growth | Inflation | Unemployment |
|---|---:|---:|---:|
| Baseline | 40% | 30% | 30% |
| Equal weights | 33.3% | 33.3% | 33.3% |
| Growth focus | 50% | 25% | 25% |
| Social-price focus | 20% | 40% | 40% |

The baseline and growth-focused scenarios shared all ten
highest-ranked profiles.

The equal-weight scenario shared four of the baseline top ten.
The social-price-focused scenario shared none.

This indicates sensitivity in the prioritization of profiles.

## 9. Validation

The original 297 country-year scores were reproduced exactly
by the baseline sensitivity scenario.

Eight automated unit tests passed.

Tests cover:

- Non-adverse indicators.
- Extreme growth deterioration.
- Correlated growth indicators.
- Missing dimensions and weight renormalization.
- Missing all indicators.
- Risk category boundaries.
- Invalid directions.
- Invalid weights.

## 10. Important Limitations

1. Z-scores use the full historical period, including the
   observation being evaluated. This introduces look-ahead
   information and prevents interpreting the results as
   real-time early warnings.

2. The 2015-2025 period is relatively short for economic
   structural analysis.

3. The World Bank's latest observations may be revised or
   estimated, especially near the end of the period.

4. The engine uses heuristic weights and thresholds.
   They are not statistically calibrated.

5. GDP growth and GDP per capita growth are highly correlated.

6. Inflation and unemployment are correlated in this sample.
   Correlation does not establish causality.

7. Country observations are not weighted by economic size.
   Scores represent country-level profiles, not an EU-wide
   GDP-weighted risk measure.

8. A high score is an investigation signal, not proof of
   economic crisis.

## 11. Output Artifacts

Main assessment:

- data/processed/economy/eu27_economic_risk_assessment_v1.csv

Reusable implementation:

- src/risk_engine/economic_risk_scorer.py

Automated tests:

- tests/test_economic_risk_engine.py

Sensitivity reports:

- reports/figures/economy/economic_risk_weight_sensitivity_v1.csv
- reports/figures/economy/economic_risk_weight_sensitivity_detail_v1.csv

## 12. Conclusion

Economic Risk Engine V1 provides a reproducible, transparent,
country-year heuristic framework for identifying adverse
economic conditions.

It is designed as one component of Sentinel AI's broader
multidomain risk intelligence architecture.

It should be interpreted as an exploratory decision-support
tool rather than a calibrated predictive model.
