"""Vector index writer.

Thin wrapper around the vector_store repository that:
- Builds VectorRecord objects from (Chunk + embedding + ACL + doc metadata).
- Performs idempotent upserts (id = f"{document_id}#{chunk_id}").
- Supports `delete_by_document(document_id)` for rollback / GDPR.
- Tracks per-doc upsert progress for resumable indexing on partial failure.
"""

# class VectorRecord(BaseModel):
#     id: str
#     values: list[float]
#     metadata: dict[str, Any]    # MUST include: document_id, chunk_id,
#                                 # tenant_id, acl_groups, title, page,
#                                 # section, source_uri.
#
# class Indexer:
#     def __init__(self, vector_store: VectorStore, settings): ...
#
#     async def upsert(self, records: list[VectorRecord]) -> None:
#         """Batched upsert (settings.UPSERT_BATCH_SIZE), with retries."""
#         ...
#
#     async def delete_by_document(self, document_id: str) -> int:
#         """Delete every chunk for a document. Returns count removed."""
#         ...
