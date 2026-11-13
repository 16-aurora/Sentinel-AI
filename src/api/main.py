"""Sentinel AI REST API entry point."""

import logging
import time

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from core.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    PROJECT_ROOT,
)
from core.logging_config import configure_logging
from schemas.responses import ErrorResponse

from routes.health import router as health_router
from routes.domains import router as domains_router


logger = configure_logging(PROJECT_ROOT)


def create_app() -> FastAPI:
    """Build and configure the Sentinel AI application."""

    application = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION
    )

    @application.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=f"HTTP_{exc.status_code}",
                message=str(exc.detail)
            ).model_dump(),
            headers=exc.headers
        )

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError
    ):
        issues = [
            {
                "location": list(error.get("loc", [])),
                "message": error.get("msg", "Invalid value"),
                "type": error.get("type", "validation_error")
            }
            for error in exc.errors()
        ]

        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error="VALIDATION_ERROR",
                message="The request contains invalid data.",
                details={"issues": issues}
            ).model_dump()
        )

    @application.exception_handler(Exception)
    async def internal_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="INTERNAL_SERVER_ERROR",
                message="An unexpected internal error occurred."
            ).model_dump()
        )

    @application.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            logger.info(
                "%s %s | status=%s | duration_ms=%.2f",
                request.method,
                request.url.path,
                response.status_code,
                duration_ms
            )

            return response

        except Exception:
            logger.exception(
                "Unhandled error processing %s %s",
                request.method,
                request.url.path
            )
            raise

    @application.get("/", include_in_schema=False)
    def root():
        return FileResponse(PROJECT_ROOT / "dashboard" / "index.html")

    application.mount(
        "/static",
        StaticFiles(directory=PROJECT_ROOT / "dashboard"),
        name="static"
    )

    application.include_router(health_router)
    application.include_router(domains_router)

    logger.info("Sentinel AI API application created.")

    return application


app = create_app()
