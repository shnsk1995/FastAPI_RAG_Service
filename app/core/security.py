"""Authentication primitives.

API Gateway can be configured with a Cognito or Lambda authorizer that already
validates the JWT and forwards claims as request context. For defense-in-depth,
re-verify the token here too — never trust upstream alone.

Verification steps:
1. Pull JWKS from JWKS_URL (cache in-memory for the container; refresh on
   `kid` miss).
2. Verify signature, `iss`, `aud`, `exp`, `nbf`, `token_use=access`.
3. Map claims -> AuthenticatedUser (sub, email, tenant_id, roles, scopes).
"""

# Dataclasses / models:
#
# class AuthenticatedUser(BaseModel):
#     user_id: str            # 'sub'
#     tenant_id: str          # custom claim 'custom:tenant_id'
#     email: str | None
#     roles: list[str]        # ["admin", "analyst", ...]
#     scopes: list[str]       # ["chat:read", "ingest:write", ...]
#     groups: list[str]       # for document ACL filtering
#
# Public surface:
#
# class JWTValidator:
#     def __init__(self, jwks_url, issuer, audience): ...
#     async def verify(self, token: str) -> AuthenticatedUser: ...
#
# # FastAPI dependency. Reads Authorization header; raises AuthenticationError.
# async def get_current_user(
#     authorization: str = Header(...),
#     validator: JWTValidator = Depends(get_jwt_validator),
# ) -> AuthenticatedUser: ...
#
# # Service-to-service: HMAC signature verification for webhooks (separate
# # from user JWT). See webhook_client for the signing side.
# def verify_webhook_signature(body: bytes, signature: str, secret: str) -> bool:
#     # HMAC-SHA256, constant-time compare.
#     ...
