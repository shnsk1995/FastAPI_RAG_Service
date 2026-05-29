"""Ingestion orchestration.

Two entry points:

1. create_upload_url() — synchronous, called from the upload-url endpoint.
2. process_upload()    — asynchronous-friendly, called from the webhook
                         endpoint (or from a separate worker Lambda
                         triggered directly by an S3 ObjectCreated event).

`process_upload` is idempotent: re-delivery of the same S3 event must not
double-index. Use the (document_id, etag) pair as the idempotency key.

Failure handling: on any step failure, set DocumentState.FAILED with a
human-readable reason; the S3 object stays so a retry job can re-trigger
processing. Vectors written before the failure must be rolled back
(delete by document_id) to avoid partial corpora.
"""

# class IngestionService:
#     def __init__(
#         self,
#         s3: S3Client,
#         metadata: MetadataStore,
#         webhook: WebhookClient,
#         parser: DocumentParser,
#         chunker: Chunker,
#         embedder: Embedder,
#         indexer: Indexer,
#         settings: Settings,
#     ): ...
#
#     async def create_upload_url(
#         self, req: PresignedUploadRequest, user: AuthenticatedUser,
#     ) -> PresignedUploadResponse:
#         """Steps:
#         1. Validate content_type ∈ ALLOWED_MIME_TYPES, size ≤ MAX_UPLOAD.
#         2. Compute document_id (ULID).
#         3. Resolve effective ACL = intersect(req.acl_groups or user.groups,
#                                              user.groups). Tenant always added.
#         4. metadata.put(DocumentMetadata(state=PENDING, acl=..., ...)).
#         5. s3.generate_presigned_url(
#              key=f"uploads/{tenant_id}/{document_id}/{safe_filename}",
#              method="PUT",
#              conditions=[content-length-range, content-type, sse, kms],
#              expires_in=settings.S3_PRESIGNED_URL_TTL_SECONDS,
#            )
#         6. Return URL + document_id + expiry.
#         """
#         ...
#
#     async def process_upload(self, payload: IngestionWebhookPayload) -> None:
#         """Steps:
#         1. metadata.get(payload.document_id); ensure tenant matches key.
#         2. Idempotency: if state ∈ {INDEXED, PROCESSING with same etag} -> return.
#         3. metadata.update_state(PROCESSING).
#         4. Stream object from S3 (s3.get_streaming_body).
#         5. text_blocks = parser.parse(stream, content_type).
#         6. chunks = chunker.chunk(text_blocks, doc_metadata).
#         7. embeddings = await embedder.embed_documents([c.text for c in chunks])
#            # batched, with retries.
#         8. indexer.upsert([
#              VectorRecord(id=f"{doc_id}#{chunk_id}", values=emb,
#                metadata={doc_id, chunk_id, tenant_id, acl, title, page, ...})
#              for chunk, emb in zip(chunks, embeddings)
#            ])
#         9. metadata.update(state=INDEXED, chunk_count=len(chunks),
#                            indexed_at=now).
#        10. semantic_cache.invalidate_tenant(tenant_id)  # via webhook or SNS
#        11. Emit `document.indexed` event (EventBridge) for downstream
#            consumers (UI refresh, audit log).
#
#        On any exception: rollback (delete vectors by document_id),
#        metadata.update(state=FAILED, error=...), re-raise so SQS / DLQ
#        captures the failure for retry analysis.
#         """
#         ...
#
#     async def delete_document(self, document_id: str, user: AuthenticatedUser) -> None:
#         """ACL check -> delete vectors -> tombstone metadata -> delete S3
#         object -> emit `document.deleted` event.
#         """
#         ...
