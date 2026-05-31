"""Domain exceptions and FastAPI exception handlers.

Goals:
- Map every internal exception to a consistent JSON error envelope
  { "error": { "code": "...", "message": "...", "request_id": "..." } }.
- Never leak stack traces or internal identifiers to clients.
- Emit structured logs + metrics for every error.
"""

# Define exception classes (raise these from services / routers):
#
# class AppError(Exception):                      # base
#     status_code: int = 500
#     code: str = "internal_error"
#
# class AuthenticationError(AppError): 401 / "unauthenticated"
# class AuthorizationError(AppError):  403 / "forbidden"
# class ValidationAppError(AppError):  422 / "invalid_request"
# class GuardrailViolation(AppError):  400 / "guardrail_blocked"
#     # carries `category` (pii | injection | toxicity | policy)
# class RateLimitExceeded(AppError):   429 / "rate_limited"
# class UpstreamLLMError(AppError):    502 / "llm_unavailable"
# class VectorStoreError(AppError):    503 / "retrieval_failed"
# class IngestionError(AppError):      500 / "ingestion_failed"
# class NotFoundError(AppError):       404 / "not_found"
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.logging import get_logger
from fastapi.exceptions import RequestValidationError

logger = get_logger(__name__)

class LLMServiceError(Exception):
  """Raised when the LLM provider fails."""

  def __init__(self, message: str = "LLM service failed"):
    self.message = message
    super().__init__(self.message)




class InputGuardrailError(Exception):
  """Raised when input guardrail processing fails."""

  def __init__(self, message : str = "Input guardrail processing failed"):
    self.message = message
    super().__init__(self.message)




class ConversationStoreError(Exception):

  def __init__(self, message: str = "Conversation store failed"):
    self.message =message
    super().__init__(self.message)




def register_exception_handlers(app: FastAPI) -> None:
    """Attach handlers for AppError, RequestValidationError, HTTPException, Exception.

    Each handler should:
    - Build the standard error envelope.
    - Pull request_id from contextvars (set by RequestContextMiddleware).
    - Log with structlog including user_id, tenant_id, route, exc_info for 5xx.
    - Emit a CloudWatch metric (errors_total{code=...}).
    """
    @app.exception_handler(LLMServiceError)
    async def llm_service_error_handler(request: Request, exc: LLMServiceError):


      logger.error(
        "llm_service_error",
        path=request.url.path,
        method=request.method,
        message=exc.message,
      )

      return JSONResponse(
        status_code=502,
        content={
          "error" : "llm_service_error",
          "message" : exc.message,
        },
      )
    

    @app.exception_handler(ConversationStoreError)
    async def conversation_store_error_handler(request: Request, exc: ConversationStoreError):



      logger.error(
        "conversation_store_error",
        path=request.url.path,
        method=request.method,
        message=exc.message,
      )

      return JSONResponse(
        status_code=503,
        content={
          "error" : "conversation_store_error",
          "message" : exc.message,
        }
      )


    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request : Request, exc : RequestValidationError):
      logger.warning(
        "request_validation_error",
        path=request.url.path,
        method=request.method,
        error_count=len(exc.errors()),
      )


      return JSONResponse(
        status_code=422,
        content={
          "error" : "validation_error",
          "message" : "Invalid request payload",
          "details" : [
            {
              "field" : ".".join(str(part) for part in error.get("loc", [])),
              "message" : error.get("msg"),
              "type" : error.get("type"),
            }
            for error in exc.errors()
          ],
        },
      )
    



    @app.exception_handler(InputGuardrailError)
    async def input_guardrail_error(request : Request, exc : InputGuardrailError):
      logger.error(
        "input_guardrail_error",
        path=request.url.path,
        method=request.method,
        message=exc.message,
      )

      return JSONResponse(
        status_code=502,
        content={
          "error" : "input_guardrail_error",
          "message" : exc.message
        }
      )


