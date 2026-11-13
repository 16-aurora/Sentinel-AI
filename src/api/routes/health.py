"""Health and availability endpoints."""

from fastapi import APIRouter

from core.config import PROJECT_ROOT
from schemas.responses import HealthResponse
from services.intelligence_service import IntelligenceService


router = APIRouter(tags=["Health"])

intelligence_service = IntelligenceService(PROJECT_ROOT)


@router.get("/health", response_model=HealthResponse)
def health():
    """Return the current multidomain system health."""
    return intelligence_service.get_health()
