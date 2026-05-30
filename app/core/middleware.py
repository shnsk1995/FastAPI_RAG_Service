"""ASGI middleware for the FastAPI app.

Order in create_app() (outermost first):
    RequestContextMiddleware  -> sets request_id, binds structlog context
    AuthMiddleware            -> validates JWT for protected paths
    RateLimitMiddleware       -> token-bucket per (user_id, route)
    CORSMiddleware            -> standard fastapi.middleware.cors
    GZipMiddleware            -> compress responses
"""

# class RequestContextMiddleware(BaseHTTPMiddleware):
#     """Generates / propagates X-Request-Id, records latency, binds logger.
#     - Read incoming X-Request-Id (from API Gateway) or generate uuid4.
#     - Stash in contextvars + response header.
#     - Time the request; emit metric `request_duration_ms{route,status}`.
#     """
#     ...
#
# class AuthMiddleware(BaseHTTPMiddleware):
#     """Optional alternative to per-route Depends(get_current_user).
#     Skips public paths (health, /openapi.json in non-prod, /docs).
#     Attaches AuthenticatedUser to request.state.user.
#     """
#     ...
#
# class RateLimitMiddleware(BaseHTTPMiddleware):
#     """Token-bucket in Redis keyed by (user_id, route).
#     Returns 429 with Retry-After when exhausted.
#     Bypass for ingest:process scope (service-to-service).
#     """
#     ...


import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger, bind_request_context, clear_request_context

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid4()))
        start_time = time.perf_counter()

        bind_request_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        try:

            logger.info("http_request_started")

            response = await call_next(request)

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            response.headers["x-request-id"] = request_id

            logger.info(
                "http_request_completed",
                status_code=response.status_code,
                latency_ms = latency_ms,
            )

            return response
        
        except Exception:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            logger.exception(
                "http_request_failed",
                latency_ms=latency_ms,
            )

            raise
        
        finally:
            clear_request_context()