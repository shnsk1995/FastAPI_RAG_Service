"""Ingestion endpoints (event-driven RAG corpus management).

Flow:
    1. Client → POST /upload-url            (this service)
    2. Client → PUT presigned URL → S3       (direct, no API GW transit)
    3. S3 ObjectCreated event → EventBridge / Lambda → downstream processor
       → calls POST /webhook on this service to confirm + trigger indexing.
    4. /webhook handler verifies HMAC, then ingestion_service.process(...).

Routes:
    POST   /api/v1/ingestion/upload-url       — issue presigned URL
    POST   /api/v1/ingestion/webhook          — receive S3 upload notification
    GET    /api/v1/ingestion/documents        — list user's docs + status
    GET    /api/v1/ingestion/documents/{id}   — fetch doc metadata + status
    DELETE /api/v1/ingestion/documents/{id}   — remove doc + vectors (GDPR)
"""

# router = APIRouter()
#
# @router.post(
#     "/upload-url",
#     response_model=PresignedUploadResponse,
#     dependencies=[Depends(require_scopes(Scope.INGEST_UPLOAD))],
# )
# async def create_upload_url(
#     body: PresignedUploadRequest,
#     user: AuthenticatedUser = Depends(get_current_user),
#     service: IngestionService = Depends(get_ingestion_service),
# ) -> PresignedUploadResponse:
#     """Validate filename / mime / size; create a DocumentMetadata row in
#     state=PENDING with ACL derived from the user's groups/tenant; return
#     presigned PUT URL with content-length-range + content-type conditions.
#
#     The S3 key embeds tenant_id and document_id:
#         s3://<bucket>/uploads/<tenant_id>/<document_id>/<safe_filename>
#     """
#     ...
#
# @router.post(
#     "/webhook",
#     dependencies=[Depends(require_scopes(Scope.INGEST_PROCESS))],
# )
# async def ingestion_webhook(
#     request: Request,
#     service: IngestionService = Depends(get_ingestion_service),
# ):
#     """Receive upload-complete notification from the S3 event router.
#
#     1. Read raw body bytes; verify HMAC sig header (X-Signature-256).
#     2. Parse payload: bucket, key, etag, size, document_id, tenant_id.
#     3. Idempotency: if metadata.state in {INDEXED, PROCESSING}, return 200.
#     4. Update state -> PROCESSING.
#     5. Enqueue the job (return 202) OR run synchronously if invoked inside
#        the worker Lambda. Long work goes to SQS to avoid API GW 29s limit.
#     """
#     ...
#
# @router.get("/documents", ...)
# async def list_documents(...): ...           # paginated, ACL-filtered
#
# @router.get("/documents/{document_id}", ...)
# async def get_document(...): ...
#
# @router.delete("/documents/{document_id}", ...)
# async def delete_document(...):
#     """Tombstone metadata, delete vectors with this doc_id, delete S3 object."""
#     ...
