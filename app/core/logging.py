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
