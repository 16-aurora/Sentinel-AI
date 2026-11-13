"""Multidomain intelligence endpoints."""

from fastapi import APIRouter, HTTPException, Query

from core.config import PROJECT_ROOT, VALID_DOMAINS
from schemas.responses import DomainsResponse
from services.intelligence_service import IntelligenceService


router = APIRouter(tags=["Domains"])

intelligence_service = IntelligenceService(PROJECT_ROOT)


@router.get("/domains", response_model=DomainsResponse)
def get_domains():
    """Return the status and intelligence of all domains."""
    return intelligence_service.get_domains()


@router.get("/domains/{domain}")
def get_domain(domain: str):
    """Return intelligence for a specific domain."""
    if domain not in VALID_DOMAINS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown domain: {domain}"
        )

    try:
        return intelligence_service.get_domain(domain)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Domain data not available: {domain}"
        )
@router.get("/domains/{domain}/records")
def get_domain_records(
    domain: str,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """Return paginated source records for a specific domain."""
    if domain not in VALID_DOMAINS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown domain: {domain}"
        )

    try:
        return intelligence_service.get_domain_records(
            domain, limit, offset
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail=f"Source data unavailable for domain: {domain}"
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Domain data not available: {domain}"
        )
