# Sentinel AI - Multidomain Orchestrator V2

## 1. Overview

The Multidomain Orchestrator coordinates three independent
intelligence domains:

- Cybersecurity intelligence
- Climate exposure intelligence
- Economic risk intelligence

Its responsibility is to verify dataset availability, validate
basic data integrity, calculate domain-level summaries and
produce a unified system status report.

It does not merge incomparable risk scores into a global score.

## 2. Architecture

The orchestrator uses three independent domain inputs.

| Domain | Dataset unit | Records |
|---|---|---:|
| Cybersecurity | CVE / vulnerability | 1,768 |
| Climate | Country-year | 297 |
| Economy | Country-year | 297 |

Total records inspected: 2,362.

Cybersecurity records represent individual vulnerabilities.
Climate and economic records represent country-year observations.
These units are intentionally preserved.

## 3. Input datasets

### Cybersecurity

`data/processed/sentinel_integrated_intelligence_v2.csv`

Required fields:

- `cveID`
- `risk_score`
- `risk_level`
- `risk_score_interpretation`

### Climate

`data/processed/climate/eu27_climate_exposure_index_v1.csv`

Required fields:

- `country_code`
- `year`
- `climate_exposure_index`
- `climate_exposure_category`

### Economy

`data/processed/economy/eu27_economic_risk_assessment_v1.csv`

Required fields:

- `country_code`
- `year`
- `economic_risk_score`
- `economic_risk_category`

## 4. Validation rules

The orchestrator checks:

1. Dataset file existence.
2. Required schema fields.
3. Expected record count.
4. Non-empty record identifiers.
5. Unique record keys.
6. Non-empty risk categories.
7. Numeric risk scores.
8. Finite score values.
9. Score range between 0 and 100.

Record keys:

- Cybersecurity: `cveID`
- Climate: `country_code + year`
- Economy: `country_code + year`

## 5. System statuses

| Status | Meaning |
|---|---|
| OPERATIONAL | All three domains are available |
| PARTIAL | At least one domain is unavailable or invalid |

Domain-level statuses include:

- AVAILABLE
- UNAVAILABLE
- SCHEMA_ERROR
- REVIEW
- DATA_ERROR
- READ_ERROR

## 6. Risk score interpretation

The three domains use different scoring methodologies.

### Cybersecurity

The `risk_score` is a heuristic prioritization score.
It is not a calibrated probability of exploitation or attack.

### Climate

The `climate_exposure_index` is a relative, heuristic index
based on climate exposure indicators.

It is not a probability of a natural disaster.

### Economy

The `economic_risk_score` is a heuristic score based on
economic adverse signals and configured weights.

It is not a calibrated probability of an economic crisis.

The three scores must not be interpreted as directly equivalent
or averaged into a global risk score.

## 7. Outputs

The orchestrator generates:

`reports/multidomain/sentinel_multidomain_status_v1.json`

Initial orchestration report.

`reports/multidomain/sentinel_multidomain_status_v2.json`

Report generated after data integrity validation.

The report includes:

- System status
- Number of available domains
- Domain-level status
- Record counts
- Score field and category field
- Minimum, maximum and mean score
- Category distributions
- Validation errors, if present

## 8. Automated testing

Permanent test suite:

`tests/test_multidomain_orchestrator.py`

Validated scenarios:

1. All domains available.
2. Missing domain.
3. Invalid schema.
4. Unexpected record count.
5. Duplicate record key.
6. Invalid score.

Latest execution:

- Tests: 6
- Failures: 0
- Errors: 0

Result: ALL TESTS PASSED.

## 9. Current limitations

- The orchestrator reads local CSV files.
- Expected record counts are configured explicitly.
- It does not yet provide an HTTP API.
- It does not automatically refresh source datasets.
- It does not perform real-time monitoring.
- It does not combine cybersecurity CVEs with country-year
  records because no validated geographic relationship has
  been established.
- A successful integrity audit does not prove that the
  underlying risk methodology is predictive or calibrated.

## 10. Future development

Potential next steps:

- Expose orchestration through a REST API.
- Add structured application logging.
- Add configurable data freshness checks.
- Add source provenance and dataset version tracking.
- Integrate a monitoring dashboard.
- Add end-to-end API and integration tests.

## 11. Project component

Module:

`src/orchestration/multidomain_orchestrator.py`

Test suite:

`tests/test_multidomain_orchestrator.py`

Documentation:

`docs/multidomain_orchestrator_documentation.md`
