"""Cross-cutting FastAPI dependency providers.

Wire shared, container-cached clients into routes/services. Keeping clients
module-level lets Lambda warm starts reuse open connections (HTTP/TLS, DDB,
Redis).
"""

# Examples to provide via Depends():
#
# get_settings()              -> Settings (cached)
# get_anthropic_client()      -> anthropic.AsyncAnthropic (singleton)
# get_embedding_client()      -> EmbeddingClient
# get_vector_store()          -> VectorStore repository
# get_metadata_store()        -> MetadataStore repository (DynamoDB)
# get_cache_store()           -> SemanticCacheStore (Redis)
# get_conversation_store()    -> ConversationStore (DynamoDB)
# get_s3_client()             -> boto3 S3 client (cached)
# get_webhook_client()        -> WebhookClient (HMAC-signing httpx wrapper)
# get_current_user(token)     -> AuthenticatedUser (decoded JWT claims)
# require_scopes(*scopes)     -> dependency factory for RBAC scope checks
# get_request_context()       -> RequestContext (request_id, tenant_id, user_id)
