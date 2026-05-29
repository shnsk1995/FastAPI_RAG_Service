"""FastAPI application factory.

Boots the ASGI app, registers middleware, exception handlers, and routers.
Module-level singletons (clients, settings) live here so Lambda containers
reuse them across warm invocations.
"""

# Imports to add when implementing:
# - FastAPI, CORS / GZip middleware
# - app.config.get_settings
# - app.core.logging.configure_logging
# - app.core.middleware.RequestContextMiddleware (request_id, user_id, latency)
# - app.api.v1.router (aggregated v1 router)
# - app.exceptions.register_exception_handlers

from fastapi import FastAPI
from app.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.chat import router as chat_router
from app.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    """Build and return the FastAPI instance.

    Steps:
    1. Load settings via get_settings() (cached pydantic-settings).
    2. Configure structured JSON logging (CloudWatch friendly).
    3. Instantiate FastAPI(title, version, docs_url=None if prod).
    4. Add middleware in order: RequestContext -> Auth -> RateLimit -> CORS -> GZip.
    5. Register exception handlers (validation, auth, guardrail, llm, infra).
    6. Mount routers: /api/v1 (chat + ingestion + health).
    7. Pre-warm heavy clients (Anthropic, vector store, embedding model, S3)
       in startup hook so cold-start latency is paid once per container.
    8. Return the app.
    """
    app = FastAPI(
        title = settings.APP_NAME,
        version="0.1.0",
        description="Backend service for chat and document ingestion",
    )

    app.include_router(health_router)
    app.include_router(chat_router)

    register_exception_handlers(app)

    return app


# Module-level instance so Mangum / uvicorn can import `app.main:app`.
app = create_app()


@app.get("/")
def root():
    return {
        "message" : "Chat and Ingestion Service is running",
        "environment" : settings.APP_ENV
    }