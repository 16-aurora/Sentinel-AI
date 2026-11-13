# Sentinel AI — Backend REST API Documentation

## 1. Overview

Sentinel AI exposes a REST API built with FastAPI. It provides access to
multidomain risk intelligence across three domains:

- Cybersecurity
- Climate
- Economy

The API acts as an access layer over the existing intelligence
orchestration system. It does not replace the domain-specific risk engines.

## 2. Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- Standard-library CSV processing
- Pytest
- HTTPX for API testing

## 3. Architecture

The backend follows a modular structure:

- `src/api/main.py`: application factory, middleware and exception handlers.
- `src/api/core/config.py`: central API configuration.
- `src/api/core/logging_config.py`: logging configuration.
- `src/api/routes/health.py`: health endpoint.
- `src/api/routes/domains.py`: multidomain endpoints.
- `src/api/services/intelligence_service.py`: access to intelligence data
  and in-memory caching.
- `src/api/schemas/responses.py`: Pydantic response schemas.
- `src/orchestration/multidomain_orchestrator.py`: domain validation
  and orchestration.

## 4. Available Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API root information |
| GET | `/health` | System health and domain availability |
| GET | `/domains` | Multidomain intelligence summary |
| GET | `/domains/{domain}` | Details for a specific domain |
| GET | `/openapi.json` | OpenAPI specification |
| GET | `/docs` | Interactive Swagger documentation |

Supported domain identifiers:

- `cybersecurity`
- `climate`
- `economy`

Unknown domain identifiers return HTTP 404.

## 5. Health and Operational Status

The health endpoint reports:

- System name.
- Overall operational status.
- Number of available domains.
- Total configured domains.

The system reports `OPERATIONAL` when all configured domains pass
orchestration validation. Otherwise, it reports a partial status.

This status describes data and orchestration availability. It is not
a complete infrastructure or production-readiness health assessment.

## 6. Data Validation and Domain Units

The orchestration layer validates:

- Source file availability.
- Required columns.
- Expected record counts.
- Unique and non-empty record keys.
- Non-empty risk categories.
- Numeric, finite risk scores within the configured 0–100 range.

The domains use different analytical units:

- Cybersecurity: individual CVE vulnerabilities.
- Climate: country-year observations.
- Economy: country-year observations.

These units are not directly interchangeable. The API preserves
domain-specific scores and does not calculate an unsupported global
average across the three domains.

## 7. Caching

The intelligence service implements process-local in-memory caching.

Current configuration:

- Cache time-to-live: 60 seconds.
- Source-file metadata: modification timestamp and file size.
- Cache invalidation: source metadata changes or TTL expiration.
- Concurrency protection: `RLock`.

The cache reduces repeated CSV loading and orchestration work.

The cache is local to each application process. Multiple server workers
would maintain independent caches.

File metadata-based invalidation is not a cryptographic integrity check.
Changes that preserve both file size and modification timestamp may not
be detected immediately.

## 8. Logging

The backend uses Python's standard logging framework.

Log output:

- Console.
- `reports/logs/sentinel_api.log`.

The file handler uses rotation:

- Maximum file size: 5 MB.
- Backup files: 3.
- UTF-8 encoding.

Request logging records HTTP method, path, response status and duration.
Unexpected exceptions are recorded for diagnostics.

Request bodies and secrets should not be written to logs.

## 9. Error Handling

The API uses a consistent JSON error structure:

- `success`: false.
- `error`: machine-readable error identifier.
- `message`: human-readable explanation.
- `details`: optional additional information.

Handled error categories include:

- HTTP errors, such as 404.
- Request validation errors, such as 422.
- Unexpected internal errors, returned as 500.

Internal exception details and tracebacks are not exposed in the
HTTP 500 response.

## 10. Local Installation and Startup

Requirements:

- Python environment configured.
- Project dependencies installed.
- Project data files available in their expected directories.

From the project root, execute:

`run_sentinel_api.bat`

The startup script activates `.venv` and launches Uvicorn.

Default local address:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

The startup script uses automatic reload for development.

To stop the server, press `CTRL+C`.

## 11. Testing

The project includes API integration tests and orchestration tests.

The API test suite checks:

- Root endpoint.
- Health endpoint.
- Domain listing.
- Individual domain endpoints.
- Unknown domain handling.
- Request validation errors.
- Unexpected internal errors.

The orchestration test suite checks domain availability,
schema validation, record counts, duplicate keys and invalid scores.

Real-server HTTP tests are also used to verify independent Uvicorn startup
and endpoint responses.

## 12. Security and Deployment Limitations

The current configuration is intended for local development.

- The server binds to `127.0.0.1`.
- Authentication is not implemented.
- CORS is not configured.
- HTTPS and TLS termination are not configured.
- Debug and development reload settings must be reviewed before deployment.

Before exposing the API to external users, implement and validate
appropriate authentication, authorization, CORS restrictions, HTTPS,
secret management, deployment configuration and operational monitoring.

This project should not be considered production-secure solely because
its local endpoint tests pass.

## 13. Current Scope

The backend provides a local REST interface to existing cybersecurity,
climate and economic intelligence outputs.

It does not claim to provide:

- A public production service.
- User accounts or role-based access.
- Persistent database storage.
- Distributed caching.
- Automated background ingestion through the API.
- A unified score across incompatible domain units.

## 14. Disclaimer

Sentinel AI is an analytical and early-warning prototype.
Its outputs are intended to support investigation and decision-making,
not replace expert assessment or official risk evaluations.
