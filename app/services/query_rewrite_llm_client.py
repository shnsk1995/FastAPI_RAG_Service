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
import json
from anthropic import AsyncAnthropic
from app.config import settings
from app.exceptions import LLMServiceError
from app.core.logging import get_logger
from app.schemas.chat import QueryRewriteResponse
from app.integrations.tools import REWRITE_QUERY_TOOL

logger = get_logger(__name__)

class QueryRewriteLLMClient:

  def __init__(self):
    if not settings.ANTHROPIC_API_KEY:
      raise ValueError("ANTHROPIC_API_KEY is missing")

    self.client = AsyncAnthropic(
      api_key=settings.ANTHROPIC_API_KEY,
    )

  async def rewrite_user_query(self, messages: list[dict[str, str]]) -> str:

    try:

      logger.info(
        "query_rewrite_started",
        model=settings.ANTHROPIC_SONNET_MODEL,
        message_count=len(messages),
        max_tokens=settings.ANTHROPIC_MAX_TOKENS,
        temperature=settings.ANTHROPIC_TEMPERATURE
      )




      response = await self.client.messages.create(
        model=settings.ANTHROPIC_SONNET_MODEL,
        max_tokens=settings.ANTHROPIC_MAX_TOKENS,
        #temperature=settings.ANTHROPIC_TEMPERATURE,
        system=settings.QUERY_REWRITE_SYSTEM_PROMPT,
        messages=messages,
        tools=[REWRITE_QUERY_TOOL],
        tool_choice={
          "type" : "tool",
          "name" : "rewrite_query"
        }
      )

      rewritten_query = None

      for block in response.content:
        if block.type == "tool_use" and block.name == "rewrite_query":
          rewritten_query = block.input["rewritten_query"]
          break
      
      if rewritten_query is None:
        raise LLMServiceError("Empty response from query rewrite LLM provider.")
        

      result = QueryRewriteResponse.model_validate(
        block.input
      )

      answer = result.rewritten_query

      logger.info(
        "query_rewrite_completed",
        model=settings.ANTHROPIC_SONNET_MODEL,
        answer_length=len(answer),
        input_tokens=response.usage.input_tokens if response.usage else None,
        output_tokens=response.usage.output_tokens if response.usage else None,
      )

      return answer

      

    except LLMServiceError:

      logger.warning(
        "query_rewrite_llm_request_failed",
        model=settings.ANTHROPIC_SONNET_MODEL,
      )

      raise

    except Exception as exc:
      raise LLMServiceError(
        f"Failed to generate response from query rewrite LLM provider: {str(exc)}"
      ) from exc

