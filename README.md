# Sentinel AI — Multidomain Risk Intelligence

Sentinel AI is a Python-based multidomain risk intelligence and early-warning platform designed to collect, process and analyze public information across cybersecurity, climate and economy.

## Objectives

- Collect data from public and reliable sources.
- Clean, validate and transform datasets.
- Extract analytical features.
- Detect anomalies and emerging risk signals.
- Apply Machine Learning and NLP techniques.
- Build domain-specific risk assessment engines.
- Integrate multidomain intelligence.
- Provide structured intelligence through a REST API.

## Risk Domains

### Cybersecurity
- CISA KEV and NVD vulnerability intelligence.
- Vulnerability feature engineering.
- Positive-Unlabeled learning experiments.
- Isolation Forest anomaly detection.
- Explainable cybersecurity risk assessment.

### Climate
- European climate data processing.
- Country-year exposure assessment.
- Climate Exposure Index.

### Economy
- European economic indicator processing.
- Country-year economic risk assessment.
- Economic Risk Engine and risk classification.

## Multidomain Architecture

The orchestration layer integrates cybersecurity, climate and economic intelligence while preserving their original analytical units. It does not calculate an unsupported global average across incompatible observations.

## Backend REST API

Built with FastAPI, Uvicorn and Pydantic.

- GET /
- GET /health
- GET /domains
- GET /domains/{domain}
- GET /docs
- GET /openapi.json

Additional capabilities:
- Centralized response schemas and error handling.
- Request logging and log rotation.
- Process-local caching with a 60-second TTL.
- Domain availability and data validation.

## Technology Stack

- Python 3.12
- NumPy, SciPy and Pandas
- scikit-learn and Joblib
- Matplotlib
- FastAPI, Uvicorn and Pydantic
- Pytest, HTTPX and HTTPX2
- NLP tools

## Local API Startup

Run `run_sentinel_api.bat` from the project environment.

Local address: `http://127.0.0.1:8000`

Interactive documentation: `http://127.0.0.1:8000/docs`

## Testing

The latest recorded complete regression suite passed 29 tests.

## Documentation

Technical documentation is available in the `docs/` directory, including API, multidomain orchestration, economic risk and Machine Learning documentation.

## Project Status

The multidomain intelligence core and local REST API are implemented and tested. The API is intended for local development. Authentication, HTTPS and production deployment hardening remain outside the current scope.

## Disclaimer

Sentinel AI is an analytical and early-warning prototype. Its outputs support investigation and decision-making and do not replace expert assessment or official risk evaluations.
