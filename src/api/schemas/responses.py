"""Pydantic response models for Sentinel AI."""

from typing import Any
from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    application: str
    description: str
    api_version: str
    documentation: str
    health_endpoint: str


class HealthResponse(BaseModel):
    system: str
    status: str
    domains_available: int = Field(ge=0)
    domains_total: int = Field(ge=0)


class DomainsResponse(BaseModel):
    system_status: str
    domains_available: int = Field(ge=0)
    domains_total: int = Field(ge=0)
    domains: dict[str, Any]


class DomainResponse(BaseModel):
    domain: dict[str, Any]


class ErrorResponse(BaseModel):
    """Standard API error response."""

    success: bool = False
    error: str
    message: str
    details: dict[str, Any] | None = None
