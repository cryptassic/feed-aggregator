from fastapi import Request, Response
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware

class SecureServerHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        return await secure_server_headers(request, call_next)


async def secure_server_headers(request: Request, call_next: Callable) -> Response:
    response = await call_next(request)
    
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response