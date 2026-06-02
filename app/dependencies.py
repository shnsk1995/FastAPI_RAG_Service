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
from app.services.llm_client import LLMClient
from app.services.query_rewrite_llm_client import QueryRewriteLLMClient
from app.repositories.conversation_store import ConversationStore
from app.integrations.input_guardrail_client import InputGuardrailClient
from functools import lru_cache

@lru_cache(maxsize=1)
def get_llm_client()-> LLMClient:
    return LLMClient()

@lru_cache(maxsize=1)
def get_conversation_store()-> ConversationStore:
    return ConversationStore()

@lru_cache(maxsize=1)
def get_input_guardrail_client()-> InputGuardrailClient:
    return InputGuardrailClient()

@lru_cache(maxsize=1)
def get_query_rewrite_llm_client()-> QueryRewriteLLMClient:
    return QueryRewriteLLMClient()