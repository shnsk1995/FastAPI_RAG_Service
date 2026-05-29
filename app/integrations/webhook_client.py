"""Outbound webhook dispatcher.

Used by the ingestion service when it needs to notify a downstream consumer
(e.g. the ingestion processor Lambda) that a document is ready to be
processed. Inbound webhook signature verification lives in core.security.
"""

# class WebhookClient:
#     def __init__(self, http_client, signing_secret: str, settings): ...
#
#     async def post(
#         self,
#         url: str,
#         payload: dict[str, Any],
#         event_id: str,
#         timeout_seconds: float = 5.0,
#     ) -> None:
#         """1. Canonicalise payload as JSON (sorted keys).
#         2. Sign: hmac.new(secret, body, sha256).hexdigest()
#         3. Headers:
#              X-Event-Id:        event_id (idempotency on the receiver)
#              X-Signature-256:   sha256=<hex>
#              X-Timestamp:       unix seconds (reject if drift > 5 min)
#              Content-Type:      application/json
#         4. POST with retries (3x, exp backoff) on 5xx / connection errors.
#            Non-retriable: 4xx (log + raise).
#         5. Emit metric webhook_delivery{status}.
#         """
#         ...
