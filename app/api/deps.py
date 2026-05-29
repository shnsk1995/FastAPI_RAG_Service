"""Service-layer dependency providers for routers.

Keep router files thin: routers only declare Depends(get_X_service), and
this module wires concrete implementations using settings + repositories.

Each `get_*_service` should:
- Reuse cached repository/client instances (module-level).
- Construct the service lazily on first request, cache thereafter.
"""

# def get_chat_service(
#     settings = Depends(get_settings),
#     llm = Depends(get_anthropic_client),
#     retriever = Depends(get_retriever),
#     cache = Depends(get_cache_store),
#     guardrails = Depends(get_guardrails),
#     convo = Depends(get_conversation_store),
# ) -> ChatService: ...
#
# def get_ingestion_service(
#     settings = Depends(get_settings),
#     s3 = Depends(get_s3_client),
#     metadata = Depends(get_metadata_store),
#     webhook = Depends(get_webhook_client),
#     parser = Depends(get_parser),
#     chunker = Depends(get_chunker),
#     embedder = Depends(get_embedder),
#     indexer = Depends(get_indexer),
# ) -> IngestionService: ...
#
# def get_retriever(...) -> Retriever: ...
# def get_guardrails(...) -> Guardrails: ...
from fastapi import Depends
from app.services.chat_service import ChatService
from app.services.llm_client import LLMClient
from app.repositories.conversation_store import ConversationStore

def get_llm_client()-> LLMClient:
    return LLMClient()

def get_conversation_store()-> ConversationStore:
    return ConversationStore()

def get_chat_service(llm_client: LLMClient = Depends(get_llm_client), conversation_store: ConversationStore = Depends(get_conversation_store)) -> ChatService:
    return ChatService(llm_client=llm_client, conversation_store=conversation_store)