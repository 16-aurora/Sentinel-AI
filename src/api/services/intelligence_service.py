"""Central service for Sentinel AI multidomain intelligence."""
import csv

from pathlib import Path
import sys
import time
from threading import RLock

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ORCHESTRATOR_DIR = PROJECT_ROOT / "src" / "orchestration"

if str(ORCHESTRATOR_DIR) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATOR_DIR))

from multidomain_orchestrator import (
    DOMAIN_CONFIG,
    MultidomainOrchestrator,
)


class IntelligenceService:
    """Provides cached access to multidomain intelligence."""

    CACHE_TTL_SECONDS = 60

    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)
        self.orchestrator = MultidomainOrchestrator(
            self.project_root
        )

        self._cache = None
        self._cache_timestamp = 0.0
        self._cache_signature = None
        self._cache_lock = RLock()

    def _get_data_signature(self):
        """Return a signature based on source file metadata."""

        signature = []

        for domain, config in DOMAIN_CONFIG.items():
            path = self.project_root / config["file"]

            try:
                stat = path.stat()
                signature.append(
                    (domain, stat.st_mtime_ns, stat.st_size)
                )
            except OSError:
                signature.append((domain, None, None))

        return tuple(signature)

    def get_system_report(self) -> dict:
        """Return a valid cached report or generate a fresh one."""

        with self._cache_lock:
            current_time = time.monotonic()
            current_signature = self._get_data_signature()

            cache_is_valid = (
                self._cache is not None
                and self._cache_signature == current_signature
                and current_time - self._cache_timestamp
                < self.CACHE_TTL_SECONDS
            )

            if cache_is_valid:
                return self._cache

            report = self.orchestrator.run()

            self._cache = report
            self._cache_timestamp = time.monotonic()
            self._cache_signature = self._get_data_signature()

            return report

    def get_health(self) -> dict:
        report = self.get_system_report()

        return {
            "system": "Sentinel AI",
            "status": report["system_status"],
            "domains_available": report["domains_available"],
            "domains_total": report["domains_total"],
        }

    def get_domains(self) -> dict:
        report = self.get_system_report()

        return {
            "system_status": report["system_status"],
            "domains_available": report["domains_available"],
            "domains_total": report["domains_total"],
            "domains": report["domains"],
        }

    def get_domain(self, domain: str) -> dict:
        report = self.get_system_report()

        if domain not in report["domains"]:
            raise KeyError(domain)

        return report["domains"][domain]
    def get_domain_records(self, domain: str, limit: int = 50, offset: int = 0) -> dict:
        """Return paginated source records for a validated domain."""
        if domain not in DOMAIN_CONFIG:
            raise KeyError(domain)

        if limit < 1 or limit > 500 or offset < 0:
            raise ValueError("Invalid pagination parameters")

        config = DOMAIN_CONFIG[domain]
        source_path = self.project_root / config["file"]

        if not source_path.is_file():
            raise FileNotFoundError(
                f"Source data unavailable for domain: {domain}"
            )

        with source_path.open(
            "r", encoding="utf-8-sig", newline=""
        ) as source:
            reader = csv.DictReader(source)
            records = list(reader)

        return {
            "domain": domain,
            "total": len(records),
            "limit": limit,
            "offset": offset,
            "records": records[offset:offset + limit],
        }
