"""Shared pytest configuration for Sentinel AI."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODULE_PATHS = [
    PROJECT_ROOT,
    PROJECT_ROOT / "src" / "risk_engine",
    PROJECT_ROOT / "src" / "orchestration",
    PROJECT_ROOT / "src" / "api",
]

for module_path in MODULE_PATHS:
    path = str(module_path)

    if module_path.exists() and path not in sys.path:
        sys.path.insert(0, path)
