"""Auth-related Pydantic models.

These mirror the JWT claims we accept after Cognito / API GW authorizer
validation. Kept separate from `core.security.AuthenticatedUser` so that
HTTP layer and domain layer don't accidentally couple.
"""

# class TokenClaims(BaseModel):
#     sub: str
#     iss: str
#     aud: str | list[str]
#     exp: int
#     iat: int
#     scope: str | None = None        # space-separated
#     token_use: str | None = None    # "access" or "id"
#     groups: list[str] = Field(default_factory=list)
#     tenant_id: str | None = Field(default=None, alias="custom:tenant_id")
#
#     class Config:
#         populate_by_name = True
#         extra = "ignore"
#
# class AuthenticatedUserSchema(BaseModel):
#     user_id: str
#     tenant_id: str
#     email: str | None
#     roles: list[str]
#     scopes: list[str]
#     groups: list[str]
