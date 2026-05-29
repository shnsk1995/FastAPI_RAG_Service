"""Embedding generation.

Used by both ingestion (embed_documents) and retrieval (embed_query). Some
embedding APIs distinguish a "document" vs "query" task type — honour that.

Provider options:
- Voyage AI (voyage-3) — recommended for Anthropic stacks.
- Bedrock Cohere Embed v3 / Titan Embeddings.
- OpenAI text-embedding-3-large.

Implement batching, retries with backoff, and concurrency control (a
semaphore) so a single ingestion job doesn't blow the rate limit.
"""

# class Embedder:
#     def __init__(self, http_client, settings): ...
#
#     async def embed_documents(self, texts: list[str]) -> list[list[float]]:
#         """Batched. Splits into batches of settings.EMBED_BATCH_SIZE.
#         Returns embeddings in the same order as input."""
#         ...
#
#     async def embed_query(self, text: str) -> list[float]:
#         """Single query embedding. Uses query task type if supported."""
#         ...
#
#     @property
#     def dimension(self) -> int: ...
