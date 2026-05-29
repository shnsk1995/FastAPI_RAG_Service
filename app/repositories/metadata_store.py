"""Document metadata store (DynamoDB).

Primary table layout (`documents`):
    PK: tenant_id
    SK: document_id
    Attrs: filename, title, content_type, size_bytes, etag, state, acl_groups,
           chunk_count, created_at, indexed_at, error, version (for OCC).

GSIs:
    GSI1: state-created_at-index  (list pending / failed across tenants for ops)
    GSI2: created_at-index keyed by user_id for "my uploads"

Reads at request time should be eventually-consistent; state transitions
should use ConditionExpression to prevent races between webhook retries.
"""

# class DocumentMetadata(BaseModel):
#     tenant_id: str
#     document_id: str
#     filename: str
#     title: str | None
#     content_type: str
#     size_bytes: int
#     etag: str | None
#     state: DocumentState
#     acl_groups: list[str]
#     tags: list[str]
#     chunk_count: int | None
#     uploaded_by: str             # user_id
#     created_at: datetime
#     indexed_at: datetime | None
#     error: str | None
#     version: int                 # optimistic-concurrency token
#
# class MetadataStore(Protocol):
#     async def put(self, meta: DocumentMetadata) -> None: ...
#     async def get(self, tenant_id: str, document_id: str) -> DocumentMetadata | None: ...
#     async def update_state(
#         self, tenant_id, document_id, new_state: DocumentState,
#         expected_version: int, **fields,
#     ) -> DocumentMetadata: ...                      # ConditionExpression
#     async def list_by_tenant(
#         self, tenant_id, cursor: str | None, limit: int,
#         state: DocumentState | None = None,
#     ) -> Page[DocumentMetadata]: ...
#     async def delete(self, tenant_id, document_id) -> None: ...   # tombstone
#     async def ping(self) -> bool: ...
