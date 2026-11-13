"""Centralized logging configuration for Sentinel AI."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(project_root: Path) -> logging.Logger:
    """Configure application and file logging."""

    project_root = Path(project_root)

    logs_dir = project_root / "reports" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "sentinel_api.log"

    logger = logging.getLogger("sentinel_ai")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        )

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
