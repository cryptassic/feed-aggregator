import os
import traceback
from typing import Any, Dict, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException

# Get debug mode from environment variable, default to False
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"


def _create_error_response(
    status_code: int,
    error_msg: str = "",
    debug_info: Optional[Dict[str, Any]] = None
) -> PlainTextResponse | JSONResponse:
    """
    Create appropriate response based on DEBUG_MODE.
    
    Args:
        status_code: HTTP status code
        error_msg: Error message for debug mode
        debug_info: Additional debug information
    """
    if not DEBUG_MODE:
        return PlainTextResponse("", status_code=status_code)
    
    content = {
        "error": error_msg,
        "status_code": status_code,
    }
    
    if debug_info:
        content["debug_info"] = debug_info
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )


async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 Not Found errors."""
    return _create_error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        error_msg="Resource not found",
        debug_info={"path": str(request.url)} if DEBUG_MODE else None
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    debug_info = None
    if DEBUG_MODE:
        debug_info = {
            "exception_type": exc.__class__.__name__,
            "exception_msg": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url),
            "method": request.method,
            "headers": dict(request.headers),
            "client_host": request.client.host if request.client else None,
        }
    
    return _create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_msg="Internal server error",
        debug_info=debug_info
    )


async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded errors."""
    debug_info = None
    if DEBUG_MODE:
        debug_info = {
            "client_ip": request.client.host if request.client else None,
            "rate_limit_details": str(exc),
        }
    
    return _create_error_response(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        error_msg="Too many requests",
        debug_info=debug_info
    )


def configure_exception_handlers(app):
    """Configure all exception handlers for the application."""
    app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)