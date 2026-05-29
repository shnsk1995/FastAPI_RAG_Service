"""S3 client wrapper.

Built on boto3 / aioboto3. Cache the client at module level so warm Lambda
invocations reuse the HTTP/TLS connection pool. Always use SSE-KMS for
ingestion bucket and tag objects with tenant_id for cost allocation + ABAC.
"""

# class S3Client:
#     def __init__(self, bucket: str, kms_key_id: str | None, region: str): ...
#
#     def generate_presigned_put_url(
#         self,
#         key: str,
#         content_type: str,
#         max_bytes: int,
#         expires_in: int,
#         metadata: dict[str, str] | None = None,
#     ) -> str:
#         """Presigned PUT with the following conditions:
#         - Content-Type must equal `content_type`.
#         - Content-Length-Range: 1..max_bytes.
#         - x-amz-server-side-encryption: aws:kms, SSEKMSKeyId.
#         - Optional x-amz-tagging: tenant_id=<>, document_id=<>.
#         User-provided metadata is prefixed `x-amz-meta-` and goes into a
#         per-object metadata blob the worker reads back.
#         """
#         ...
#
#     def generate_presigned_get_url(
#         self, key: str, expires_in: int,
#     ) -> str: ...
#
#     async def get_streaming_body(self, key: str) -> AsyncIterator[bytes]:
#         """Yield chunks for streaming parse (large PDFs)."""
#         ...
#
#     async def delete(self, key: str) -> None: ...
#     async def head(self, key: str) -> dict[str, Any]: ...
