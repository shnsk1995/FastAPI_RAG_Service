"""Vector store abstraction (Protocol).

Concrete implementations are swapped in via settings.VECTOR_STORE_PROVIDER.
Keep the interface narrow so we can move providers without touching service
code.
"""

# class VectorStore(Protocol):
#     async def upsert(self, records: list[VectorRecord]) -> None: ...
#
#     async def query(
#         self,
#         embedding: list[float],
#         top_k: int,
#         filter: dict[str, Any] | None,
#         include_text: bool = True,
#     ) -> list[RetrievedChunk]: ...
#
#     async def hybrid_query(
#         self,
#         embedding: list[float],
#         text_query: str,            # for BM25 / lexical side
#         top_k: int,
#         filter: dict[str, Any] | None,
#         alpha: float = 0.5,
#     ) -> list[RetrievedChunk]: ...
#
#     async def delete(self, ids: list[str]) -> None: ...
#     async def delete_by_filter(self, filter: dict[str, Any]) -> int: ...
#     async def ping(self) -> bool: ...
#
#
# Concrete classes to add later (in this same file or sibling files):
#
# class OpenSearchVectorStore(VectorStore):     # Amazon OpenSearch Serverless
#     # Use the AWS SigV4-signed HTTP client. kNN + BM25 in one index.
#     ...
#
# class PineconeVectorStore(VectorStore):
#     # Use pinecone async client; namespace per tenant for hard isolation.
#     ...
#
# class PGVectorStore(VectorStore):
#     # asyncpg + pgvector; HNSW or IVFFlat index; RBAC via row-level security.
#     ...
