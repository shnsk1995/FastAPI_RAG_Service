"""Structured logging configuration.

Use structlog so every log line is one JSON object on stdout. Lambda forwards
stdout to CloudWatch automatically. Include request_id, user_id, tenant_id,
route, latency_ms, and any domain fields. Never log raw prompts, API keys, or
full document contents — log hashes and lengths instead.
"""

# Public surface:
#
# def configure_logging(level: str, env: str) -> None:
#     """Idempotent; call from create_app() once per cold start.
#     - In local: human-readable rendering.
#     - In Lambda: JSON renderer, ISO timestamps, UTC.
#     - Bind contextvars: aws_request_id, function_name, function_version.
#     """
#
# def get_logger(name: str) -> structlog.BoundLogger: ...
#
# # Helpers used by middleware:
# def bind_request_context(request_id, user_id, tenant_id, route): ...
# def clear_request_context(): ...


# Logging policy:
# - INFO: request start/end, cache hit/miss, retrieval doc_ids (not text),
#         LLM model + token counts.
# - WARN: guardrail violations, retries, partial degradations.
# - ERROR: 5xx, upstream failures, with exc_info.
# - Never log: bearer tokens, full chat content, document text bodies,
#             embedding vectors. Hash sensitive identifiers if needed.

import logging
import sys
from typing import Any

import structlog

from app.config import settings

def configure_logging() -> None:
    """

    Configure application logging.

    Local environment:
        Human-readable console logs.

    Non-local environments:
        JSON logs suitable for CloudWatch, Lambda, ECS, and log search.

    """

    log_level_name = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
        force=True,
    )

    shared_processors: list[Any] = [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.APP_ENV =="local":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    
    structlog.configure(
        processors=[
            *shared_processors,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    """Return a structured logger with common service fields."""

    return structlog.get_logger(name).bind(
        service=settings.APP_NAME,
        environment=settings.APP_ENV,
    )