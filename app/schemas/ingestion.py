"""Ingestion request/response schemas."""

# class DocumentState(StrEnum):
#     PENDING = "pending"           # presigned URL issued, awaiting upload
#     UPLOADED = "uploaded"         # S3 ObjectCreated received
#     PROCESSING = "processing"     # parsing/chunking/embedding in progress
#     INDEXED = "indexed"           # vectors live in vector store
#     FAILED = "failed"
#     DELETED = "deleted"           # tombstone
#
# class PresignedUploadRequest(BaseModel):
#     filename: str = Field(min_length=1, max_length=255)
#     content_type: str             # must be in settings.ALLOWED_MIME_TYPES
#     size_bytes: int = Field(gt=0)
#     # Optional doc-level metadata the user wants attached to all chunks:
#     title: str | None = None
#     tags: list[str] = Field(default_factory=list, max_length=20)
#     # Optional ACL override (must be subset of user's groups):
#     acl_groups: list[str] | None = None
#
# class PresignedUploadResponse(BaseModel):
#     document_id: str              # ULID
#     upload_url: str               # PUT here
#     s3_key: str
#     fields: dict[str, str] | None # if using POST-style presigned post
#     expires_at: datetime
#     max_bytes: int                # echoed for client to enforce
#
# # Payload that the S3-event router sends to our /webhook endpoint:
# class IngestionWebhookPayload(BaseModel):
#     event_id: str                 # for idempotency
#     bucket: str
#     key: str
#     etag: str
#     size_bytes: int
#     content_type: str
#     document_id: str              # parsed from S3 key prefix
#     tenant_id: str
#     uploaded_at: datetime
#
# class DocumentMetadataResponse(BaseModel):
#     document_id: str
#     filename: str
#     title: str | None
#     state: DocumentState
#     tags: list[str]
#     size_bytes: int
#     chunk_count: int | None
#     created_at: datetime
#     indexed_at: datetime | None
#     error: str | None             # populated when state == FAILED
