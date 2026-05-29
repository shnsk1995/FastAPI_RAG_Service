"""Chat orchestration — the heart of the RAG pipeline.

This class composes the building blocks. Routers should NEVER call retriever /
LLM / cache directly; they call ChatService.complete or .stream and let this
module enforce the pipeline order.
"""

# class ChatService:
#     def __init__(
#         self,
#         retriever: Retriever,
#         prompt_builder: PromptBuilder,
#         llm_client: LLMClient,
#         semantic_cache: SemanticCache,
#         guardrails: Guardrails,
#         conversation_store: ConversationStore,
#         settings: Settings,
#     ): ...
#
#     async def complete(
#         self,
#         request: ChatCompletionRequest,
#         user: AuthenticatedUser,
#         request_id: str,
#     ) -> ChatCompletionResponse:
#         """Non-streaming pipeline:
#
#             1. Resolve / create conversation_id; load short-term history.
#             2. guardrails.check_input(latest_user_message, user)
#                  -> if blocked: raise GuardrailViolation.
#                  -> if redacted: use redacted text downstream.
#             3. cache_key = semantic_cache.build_key(
#                   user.tenant_id, request.filters, redacted_question)
#                hit = await semantic_cache.get(cache_key, embedding=...)
#                if hit and hit.similarity >= threshold:
#                    return hit.response  # mark CacheStatus.SEMANTIC_HIT
#             4. docs = await retriever.search(
#                   query=redacted_question,
#                   user=user,
#                   top_k=request.top_k,
#                   filters=request.filters,
#                   conversation_history=history,    # optional query rewrite
#                )
#             5. prompt = prompt_builder.build(
#                   system_prompt=SYSTEM_PROMPT,
#                   documents=docs,
#                   history=history,
#                   question=redacted_question,
#                )
#                # PromptBuilder marks the system + docs blocks with
#                # cache_control={"type": "ephemeral"} so Anthropic prompt
#                # caching kicks in for repeat queries on the same corpus.
#             6. llm_response = await llm_client.complete(prompt, request)
#             7. guardrails.check_output(llm_response.text, docs_ids)
#                  -> if blocked: raise GuardrailViolation (or redact).
#             8. await semantic_cache.set(cache_key, response, ttl=...)
#             9. await conversation_store.append(conversation_id, ...)
#            10. Return ChatCompletionResponse w/ citations + usage + latency.
#         """
#         ...
#
#     async def stream(
#         self, request, user, request_id,
#     ) -> AsyncIterator[StreamEvent]:
#         """Same pipeline but yields:
#             - event: token   (text deltas)
#             - event: citations
#             - event: done
#         Output guardrails: buffer full text, run check on the final string
#         before the `done` event; or run streaming-safe checks on a sliding
#         window. If a guardrail fires mid-stream, send `event: error` and
#         truncate.
#         """
#         ...
#
#     async def get_conversation(self, conversation_id, user): ...
#     async def delete_conversation(self, conversation_id, user): ...
from uuid import uuid4

from app.config import settings
from app.schemas.chat import ChatCompletionRequest,ChatCompletionResponse , ChatMessage, ChatHistoryResponse
from app.services.llm_client import LLMClient
from app.repositories.conversation_store import ConversationStore
from app.core.logging import get_logger

logger = get_logger(__name__)

class ChatService:

    def __init__(self, llm_client: LLMClient, conversation_store: ConversationStore):
        self.llm_client = llm_client
        self.conversation_store = conversation_store

    async def generate_response(self, request: ChatCompletionRequest) -> ChatCompletionResponse:

        conversation_id = request.conversation_id or str(uuid4())

        logger.info(
            "chat_request_started",
            conversation_id=conversation_id,
            message_length=len(request.message),
            has_existing_conversation=bool(request.conversation_id),
        )

        previous_messages = self.conversation_store.get_messages(
            conversation_id=conversation_id,
            limit=settings.CHAT_HISTORY_LIMIT
        )

        logger.info(
            "chat_history_loaded",
            conversation_id=conversation_id,
            history_message_count=len(previous_messages),
        )

        llm_messages =[
            {
                "role" : message["role"],
                "content" : message["content"]
            }
            for message in previous_messages
            if message.get("role") in {"user", "assistant"}
            and message.get("content")
        ]

        llm_messages.append({
            "role" : "user",
            "content" : request.message
        })

        self.conversation_store.save_message(
            conversation_id=conversation_id,
            role="user",
            content=request.message,
        )

        logger.info(
            "user_message_saved",
            conversation_id=conversation_id,
        )


        answer = await self.llm_client.generate_response(llm_messages)

        logger.info(
            "llm_response_generated",
            conversation_id=conversation_id,
            answer_length=len(answer),
        )

        
        self.conversation_store.save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
        )

        logger.info(
            "assistant_message_saved",
            conversation_id=conversation_id,
        )

        logger.info(
            "chat_request_completed",
            conversation_id=conversation_id,
        )

        return ChatCompletionResponse(
        conversation_id=conversation_id,
        message=answer
        )


    async def get_chat_history(self, conversation_id : str) -> ChatCompletionResponse:

        previous_messages = self.conversation_store.get_messages(
            conversation_id = conversation_id,
            limit = settings.CHAT_HISTORY_LIMIT
        )

        messages = [
                
                
            ChatMessage(
                role = message["role"],
                content = message["content"],
                created_at = message["created_at"],
            )
                
            for message in previous_messages
            if message.get("role") in {"user","assistant"}
            and message.get("content")
        ]

        return ChatHistoryResponse(
            conversation_id = conversation_id,
            chat_hisotry = messages
        )