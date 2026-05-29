"""Chat endpoints.

Routes:
    POST   /api/v1/chat/completions            — non-streaming
    POST   /api/v1/chat/completions/stream     — SSE streaming
    GET    /api/v1/chat/conversations/{id}     — fetch history
    DELETE /api/v1/chat/conversations/{id}     — delete history (GDPR)

All routes require JWT auth + Scope.CHAT_READ.
"""

# router = APIRouter()
#
# @router.post(
#     "/completions",
#     response_model=ChatCompletionResponse,
#     dependencies=[Depends(require_scopes(Scope.CHAT_READ))],
# )
# async def chat_completion(
#     body: ChatCompletionRequest,
#     user: AuthenticatedUser = Depends(get_current_user),
#     service: ChatService = Depends(get_chat_service),
# ) -> ChatCompletionResponse:
#     """Single-turn or multi-turn chat with RAG.
#
#     Pipeline (delegated to ChatService.complete):
#       1. Input guardrails           (core.guardrails.check_input)
#       2. Semantic cache lookup      (services.semantic_cache.get)
#       3. Retrieval w/ RBAC filter   (services.retriever.search)
#       4. Prompt build w/ caching    (services.prompt_builder)
#       5. LLM call                   (services.llm_client.complete)
#       6. Output guardrails          (core.guardrails.check_output)
#       7. Cache store + conversation persist
#       8. Return response with citations, usage, cache_status
#     """
#     ...
#
# @router.post("/completions/stream", dependencies=[...])
# async def chat_completion_stream(...):
#     """Stream tokens as SSE.
#     - Use anthropic streaming + StreamingResponse(media_type="text/event-stream").
#     - Output guardrails run in chunks (sliding window) OR on the buffered
#       final text before emitting `event: done`.
#     - Heartbeats every 15s (API Gateway 29s idle timeout).
#     - Send `event: citations` before `event: done` with the source list.
#     """
#     ...
#
# @router.get("/conversations/{conversation_id}", ...)
# async def get_conversation(conversation_id: str, ...): ...
#
# @router.delete("/conversations/{conversation_id}", ...)
# async def delete_conversation(conversation_id: str, ...): ...

from fastapi import APIRouter, Depends
from app.schemas.chat import ChatCompletionRequest, ChatCompletionResponse
from app.services.chat_service import ChatService
from app.api.deps import get_chat_service


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)



@router.post("", response_model=ChatCompletionResponse)
async def chat(request: ChatCompletionRequest, chat_service: ChatService = Depends(get_chat_service)):
    return await chat_service.generate_response(request)