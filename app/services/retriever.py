"""Retrieval-augmented search.

Steps performed here (order matters for production quality):
    1. Optional query rewrite using conversation history (LLM-assisted) or
       HyDE-style expansion.
    2. Embed the (rewritten) query — embedder.embed_query.
    3. Vector store search with ACL filter (rbac.acl_filter_for(user))
       intersected with user-supplied filters.
    4. Optional hybrid search: BM25 lexical search in OpenSearch, fused with
       dense via Reciprocal Rank Fusion.
    5. Optional reranking with a cross-encoder (Cohere Rerank / bge-reranker)
       — typically retrieve top_k*5, rerank, keep top_k.
    6. Post-filter: drop chunks the user cannot access (defense-in-depth via
       rbac.can_access_document).
    7. Diversity / MMR to avoid near-duplicate chunks dominating context.
"""

# class Retriever:
#     def __init__(
#         self,
#         vector_store: VectorStore,
#         embedder: Embedder,
#         reranker: Reranker | None,
#         settings: Settings,
#     ): ...
#
#     async def search(
#         self,
#         query: str,
#         user: AuthenticatedUser,
#         top_k: int = 8,
#         filters: dict | None = None,
#         conversation_history: list[ChatMessage] | None = None,
#     ) -> list[RetrievedChunk]:
#         ...
#
# class RetrievedChunk(BaseModel):
#     document_id: str
#     chunk_id: str
#     text: str
#     score: float
#     metadata: dict[str, Any]      # title, page, section, uri, acl, ...
