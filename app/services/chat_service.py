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
from dataclasses import dataclass
from typing import Any

from app.config import settings
from app.schemas.chat import ChatCompletionRequest,ChatCompletionResponse , ChatMessage, ChatHistoryResponse
from app.services.llm_client import LLMClient
from app.services.query_rewrite_llm_client import QueryRewriteLLMClient
from app.repositories.conversation_store import ConversationStore
from app.integrations.input_guardrail_client import InputGuardrailClient
from app.core.logging import get_logger

logger = get_logger(__name__)

@dataclass
class ChatContext:
    request : ChatCompletionRequest
    conversation_id : str
    log : Any
    safe_input : str | None = None
    


class ChatService:

    def __init__(self,
    llm_client: LLMClient,
    conversation_store: ConversationStore,
    input_guardrail_client : InputGuardrailClient,
    query_rewrite_llm_client : QueryRewriteLLMClient,
    ):
        self.llm_client = llm_client
        self.conversation_store = conversation_store
        self.input_guardrail_client = input_guardrail_client
        self.query_rewrite_llm_client = query_rewrite_llm_client

    async def generate_response(self, request: ChatCompletionRequest) -> ChatCompletionResponse:

        ctx = self._init_context(request)

        ctx.log.info(
            "chat_request_started",
            message_length=len(request.message),
            has_existing_conversation=bool(request.conversation_id),
        )

        input_guardrail_response = await self._check_input_guardrail(ctx)
        
        if input_guardrail_response.was_blocked:
            ctx.log.warning(
            "chat_request_blocked_by_input_guardrail",
            block_reason=input_guardrail_response.block_reason,
            )

            return ChatCompletionResponse(
                message=input_guardrail_response.block_reason
                or "I cannot process this request.",
                conversation_id=ctx.conversation_id,
            )

        ctx.safe_input = input_guardrail_response.processed_input

        previous_messages = self._get_previous_messages(ctx)
        
        llm_messages = self._build_llm_messages(previous_messages, ctx.safe_input)

        rewritten_user_query = await self._rewrite_user_query(llm_messages)

        ctx.safe_input = rewritten_user_query

        llm_messages[-1]["content"] = rewritten_user_query
        
        self._persist_user_message(ctx)
        answer = await self.llm_client.generate_response(llm_messages)
        self._persist_assistant_message(ctx, answer)

        ctx.log.info(
            "chat_request_completed",
        )

        return ChatCompletionResponse(
        conversation_id=ctx.conversation_id,
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
            chat_history = messages
        )

    
    def _init_context(self, request : ChatCompletionRequest) -> ChatContext:
        conversation_id = request.conversation_id or str(uuid4())
        return ChatContext(
            request = request,
            conversation_id=conversation_id,
            log=logger.bind(conversation_id=conversation_id),
            safe_input = None,
            
        )

    async def _check_input_guardrail(self, ctx : ChatCompletionRequest):
        input_guardrail_response = await self.input_guardrail_client.process_input(ctx.request.message)
        
        ctx.log.info(
            "input_guardrail_processed",
            was_blocked=input_guardrail_response.was_blocked,
            guardrail_action=input_guardrail_response.guardrail_action,
            pii_detected=input_guardrail_response.pii_detected,
            prompt_attack_detected=input_guardrail_response.prompt_attack_detected,
            processed_input_length=len(input_guardrail_response.processed_input),
        )

        return input_guardrail_response

    def _get_previous_messages(self, ctx : ChatContext):
        previous_messages = self.conversation_store.get_messages(
            conversation_id=ctx.conversation_id,
            limit=settings.CHAT_HISTORY_LIMIT
        )

        ctx.log.info(
            "chat_history_loaded",
            history_message_count=len(previous_messages),
        )

        return previous_messages

    def _build_llm_messages(self, previous_messages : list[dict], safe_input : str):
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
            "content" : safe_input
        })

        return llm_messages

    def _persist_user_message(self, ctx : ChatContext):
        self.conversation_store.save_message(
            conversation_id=ctx.conversation_id,
            role="user",
            content=ctx.safe_input,
        )

        ctx.log.info(
            "user_message_saved",
        )

    def _persist_assistant_message(self, ctx : ChatContext, answer: str):
        self.conversation_store.save_message(
            conversation_id=ctx.conversation_id,
            role="assistant",
            content=answer,
        )

        ctx.log.info(
            "assistant_message_saved",
        )

    async def _rewrite_user_query(self, llm_messages : list[dict]):
        rewritten_query = await self.query_rewrite_llm_client.rewrite_user_query(llm_messages)

        return rewritten_query

