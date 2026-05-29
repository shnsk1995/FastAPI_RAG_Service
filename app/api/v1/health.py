"""Liveness & readiness probes.

- /healthz  — liveness, always returns 200 if the process is up. Used by
              Lambda extensions / external monitors.
- /readyz   — readiness, returns 200 only when downstream deps are reachable
              (vector store ping, DDB describe-table, Redis PING, Secrets
              Manager). Used to gate traffic during cold start.
"""

# router = APIRouter()
#
# @router.get("/healthz")
# async def liveness(): return {"status": "ok"}
#
# @router.get("/readyz")
# async def readiness(
#     vs = Depends(get_vector_store),
#     md = Depends(get_metadata_store),
#     cs = Depends(get_cache_store),
# ):
#     # Run lightweight pings in parallel with asyncio.gather.
#     # Return {status, checks: {...}}; 503 if any required check fails.
#     ...

from fastapi import APIRouter

from app.config import settings

router = APIRouter(
    prefix='/health',
    tags=["Health"]
)

@router.get("")
def health_check():
    return {
        "status" : "healthy",
        "service" : settings.APP_NAME,
        "environment" : settings.APP_ENV
    }