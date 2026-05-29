"""Thin Anthropic wrapper.

Responsibilities:
- Hold the single anthropic.AsyncAnthropic instance (constructed once per
  Lambda container, key loaded from Secrets Manager at cold start).
- Centralise retries + circuit breaker (tenacity): retry on 429/5xx with
  exponential backoff + jitter; surface UpstreamLLMError after exhaustion.
- Translate Anthropic responses into our domain types.
- Record token usage including prompt-cache hit/miss fields.
"""

# class LLMClient:
#     def __init__(self, anthropic_client, settings): ...
#
#     async def complete(self, request: AnthropicMessagesRequest) -> LLMResponse:
#         """Single shot. Returns text + usage + stop_reason.
#         - Pass system blocks with cache_control through verbatim.
#         - Read response.usage.cache_read_input_tokens for observability.
#         """
#         ...
#
#     async def stream(self, request: AnthropicMessagesRequest) -> AsyncIterator[LLMStreamEvent]:
#         """Yield text deltas + final usage.
#         - Use client.messages.stream context manager.
#         - Re-raise transient errors as UpstreamLLMError after retries.
#         """
#         ...
#
# class LLMResponse(BaseModel):
#     text: str
#     usage: TokenUsage
#     stop_reason: str
#     model: str
from anthropic import AsyncAnthropic
from app.config import settings
from app.exceptions import LLMServiceError



class LLMClient:

  def __init__(self):
    if not settings.ANTHROPIC_API_KEY:
      raise ValueError("ANTHROPIC_API_KEY is missing")

    self.client = AsyncAnthropic(
      api_key=settings.ANTHROPIC_API_KEY,
    )

  async def generate_response(self, messages: list[dict[str, str]]) -> str:

    try:
      response = await self.client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=settings.ANTHROPIC_MAX_TOKENS,
        #temperature=settings.ANTHROPIC_TEMPERATURE,
        system=settings.ANTHROPIC_SYSTEM_PROMPT,
        messages=messages,
      )

      if not response.content:
        return "I could not generate a response."

      first_block = response.content[0]

      if first_block.type == "text":
        return first_block.text

      raise LLMServiceError("Unsupported response type from LLM provider")

    except LLMServiceError:
      raise

    except Exception as exc:
      raise LLMServiceError(
        f"Failed to generate response from LLM provider: {str(exc)}"
      ) from exc

