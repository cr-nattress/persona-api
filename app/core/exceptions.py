"""
Custom exception handlers for API error responses.

Provides centralized error handling with detailed error messages.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from typing import Union
from datetime import datetime
from traceback import format_exc
from app.core.logging import get_logger

logger = get_logger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors.

    Returns detailed error information including validation details.
    """
    error_details = []
    for error in exc.errors():
        field_path = ".".join(str(x) for x in error["loc"][1:])
        error_details.append(f"{field_path}: {error['msg']}")

    error_message = "Request validation failed: " + " | ".join(error_details)

    logger.warning(f"Validation error: {error_message}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": error_message,
            "error_type": "ValidationError",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "timestamp": datetime.utcnow().isoformat(),
            "details": error_details
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTPException with detailed error information.

    Converts HTTPException detail to standardized error response format.
    """
    # Extract status code and detail from HTTPException
    status_code = exc.status_code
    detail = exc.detail

    logger.log(
        "WARNING" if 400 <= status_code < 500 else "ERROR",
        f"HTTP Exception: {status_code}: {detail}"
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error": str(detail) if detail else "An error occurred",
            "error_type": "HTTPException",
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all unhandled exceptions.

    Provides detailed error information while maintaining security.
    """
    error_type = type(exc).__name__
    error_message = str(exc)
    traceback_str = format_exc()

    logger.error(f"Unhandled exception: {error_type}")
    logger.error(f"  - Message: {error_message}")
    logger.error(f"  - Traceback: {traceback_str}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": f"{error_type}: {error_message}" if error_message else error_type,
            "error_type": error_type,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
