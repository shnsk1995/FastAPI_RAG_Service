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
