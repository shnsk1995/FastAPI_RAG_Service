"""Chat request/response schemas."""

# class ChatRole(StrEnum):
#     USER = "user"
#     ASSISTANT = "assistant"
#     SYSTEM = "system"
#
# class ChatMessage(BaseModel):
#     role: ChatRole
#     content: str = Field(min_length=1, max_length=8000)
#
# class ChatCompletionRequest(BaseModel):
#     conversation_id: str | None = None       # if None, server creates one
#     messages: list[ChatMessage] = Field(min_length=1, max_length=50)
#     # Optional knobs (server clamps to safe ranges):
#     temperature: float | None = Field(default=None, ge=0.0, le=1.0)
#     max_tokens: int | None = Field(default=None, ge=1, le=4096)
#     # Retrieval controls:
#     top_k: int = Field(default=8, ge=1, le=50)
#     filters: dict[str, Any] | None = None    # user-supplied metadata filter
#                                              # (intersected with RBAC filter)
#     stream: bool = False
#
# class Citation(BaseModel):
#     document_id: str
#     chunk_id: str
#     score: float
#     title: str | None
#     snippet: str | None                       # short, redacted preview
#     uri: str | None                           # presigned GET if allowed
#
# class TokenUsage(BaseModel):
#     input_tokens: int
#     output_tokens: int
#     cache_read_input_tokens: int = 0          # prompt cache hit count
#     cache_creation_input_tokens: int = 0      # prompt cache write count
#
# class CacheStatus(StrEnum):
#     SEMANTIC_HIT = "semantic_hit"
#     SEMANTIC_MISS = "semantic_miss"
#     SEMANTIC_DISABLED = "semantic_disabled"
#
# class ChatCompletionResponse(BaseModel):
#     conversation_id: str
#     message: ChatMessage                      # assistant message
#     citations: list[Citation]
#     usage: TokenUsage
#     cache_status: CacheStatus
#     model: str
#     latency_ms: int

from pydantic import BaseModel, Field


class ChatCompletionRequest(BaseModel):
    conversation_id: str | None = None       # if None, server creates one
    message: str #list[ChatMessage] = Field(min_length=1, max_length=50)
     # Optional knobs (server clamps to safe ranges):
    #temperature: float | None = Field(default=None, ge=0.0, le=1.0)
    #max_tokens: int | None = Field(default=None, ge=1, le=4096)
     # Retrieval controls:
    #top_k: int = Field(default=8, ge=1, le=50)
    #filters: dict[str, Any] | None = None    # user-supplied metadata filter
                                              # (intersected with RBAC filter)
    #stream: bool = False



class ChatCompletionResponse(BaseModel):
    conversation_id: str
    message: str #ChatMessage                      # assistant message
    #citations: list[Citation]
    #usage: TokenUsage
    #cache_status: CacheStatus
    #model: str
    #latency_ms: int