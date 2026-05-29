"""Shared Pydantic models: error envelope, pagination, identifiers."""

# class ErrorDetail(BaseModel):
#     code: str
#     message: str
#     field: str | None = None
#
# class ErrorResponse(BaseModel):
#     error: ErrorDetail
#     request_id: str
#
# class PageParams(BaseModel):
#     cursor: str | None = None
#     limit: int = Field(default=20, ge=1, le=100)
#
# class Page(GenericModel, Generic[T]):
#     items: list[T]
#     next_cursor: str | None
#
# DocumentId = NewType("DocumentId", str)      # ULID-formatted strings
# ConversationId = NewType("ConversationId", str)
