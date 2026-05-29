"""Low-level cache store (Redis / ElastiCache).

Used by SemanticCache. Two indexes to maintain inside Redis:
- Hash:    sc:<namespace>:<id>      -> {response_json, embedding_bytes, created_at}
- Vector:  RediSearch HNSW index on namespace, field=embedding, dim=N

Set TTL on every key. Use SCAN, never KEYS, to walk namespaces.
"""

# class CacheStore(Protocol):
#     async def upsert(
#         self, namespace: str, id: str, embedding: list[float],
#         payload: dict, ttl_seconds: int,
#     ) -> None: ...
#
#     async def search(
#         self, namespace: str, embedding: list[float], top_k: int = 1,
#     ) -> list[tuple[str, float, dict]]: ...
#         # returns (id, similarity, payload)
#
#     async def invalidate_namespace(self, namespace_prefix: str) -> int: ...
#     async def ping(self) -> bool: ...
