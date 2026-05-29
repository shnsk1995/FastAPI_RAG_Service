"""Chunking strategy.

Recommended default: semantic / recursive character splitting with overlap,
sized to the embedding model's effective context (e.g. 512–1024 tokens with
50–100 token overlap). Always keep chunk boundaries at paragraph / sentence
edges — never mid-token.

Special handling:
- Tables: keep each table as one chunk (don't split rows).
- Code blocks: don't split (or split on logical units).
- Long headings: prepend the heading text to each chunk under that heading
  so the embedding has section context.
"""

# class Chunk(BaseModel):
#     chunk_id: str           # f"{document_id}#{ordinal:05d}"
#     text: str
#     token_count: int
#     metadata: dict[str, Any]   # page, section, kind, parent_doc_id, ...
#
# class Chunker:
#     def __init__(self, settings): ...
#
#     def chunk(
#         self,
#         blocks: list[TextBlock],
#         doc_metadata: DocumentMetadata,
#     ) -> list[Chunk]:
#         """1. Group blocks under their nearest preceding heading.
#         2. For each group, run recursive splitter with target_tokens +
#            overlap_tokens from settings.
#         3. Prepend heading to each emitted chunk.
#         4. Carry through page numbers + section paths into chunk.metadata.
#         5. Filter out empty / near-duplicate chunks (cosine on embeddings or
#            simhash on text) to keep the corpus clean.
#         """
#         ...
