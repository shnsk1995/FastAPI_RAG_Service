"""AWS Secrets Manager wrapper.

Pull all third-party API keys (Anthropic, embedding provider, webhook signing
secret) at cold start, cache for the container lifetime. Optional periodic
refresh if rotation matters: re-fetch on auth errors from the upstream API.
"""

# class SecretsManager:
#     def __init__(self, region: str): ...
#
#     async def get_secret(self, secret_id: str, *, version: str = "AWSCURRENT") -> str:
#         """Returns the SecretString. Caches in-memory keyed by secret_id."""
#         ...
#
#     async def get_secret_json(self, secret_id: str) -> dict[str, Any]:
#         """Same as get_secret but json.loads the result. Use for grouped
#         secrets (multiple keys in one secret)."""
#         ...
#
#     def invalidate(self, secret_id: str) -> None:
#         """Drop the cached value so the next call re-fetches. Used when an
#         upstream rejects the key (likely rotated)."""
#         ...
