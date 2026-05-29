"""Semantic cache.

Different from Anthropic prompt caching:
- Prompt caching = byte-level prefix cache INSIDE Anthropic's infra; saves
  input tokens on the next call with the same prefix.
- Semantic cache = our own response cache keyed by question embedding, so we
  skip the LLM entirely when a near-duplicate question was asked recently.

Backing store: Redis (ElastiCache) with RediSearch HNSW index for ANN, OR a
small Redis hash + brute-force cosine if QPS is low.

Key design:
    namespace = f"sc:{tenant_id}:{filter_hash}"
    member    = embedding vector + metadata (response, citations, usage,
                model, created_at)

Lookups must respect tenancy and filters — never serve a hit across tenants
or across different retrieval filters.
"""

# class CacheHit(BaseModel):
#     response: ChatCompletionResponse
#     similarity: float
#     cached_at: datetime
#
# class SemanticCache:
#     def __init__(
#         self,
#         cache_store: CacheStore,        # repositories.cache_store
#         embedder: Embedder,
#         settings: Settings,
#     ): ...
#
#     def build_key(self, tenant_id: str, filters: dict | None) -> str:
#         """Stable namespace string; filter dict is canonical-JSON hashed."""
#         ...
#
#     async def get(
#         self, namespace: str, question: str
#     ) -> CacheHit | None:
#         """1. embed(question)
#            2. ANN search within namespace, top-1
#            3. if similarity >= threshold AND not stale -> return
#         """
#         ...
#
#     async def set(
#         self, namespace: str, question: str, response: ChatCompletionResponse
#     ) -> None:
#         """1. embed(question)
#            2. upsert into namespace with TTL
#            3. evict if namespace exceeds size cap (LRU).
#         """
#         ...
#
#     async def invalidate_tenant(self, tenant_id: str) -> None:
#         """Called when a document is added/removed for the tenant so stale
#         cached answers don't outlive their source documents."""
#         ...
