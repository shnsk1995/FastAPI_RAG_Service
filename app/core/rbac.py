"""Role / scope / document-level access control.

Two enforcement layers:
1. Endpoint-level scope check (FastAPI dependency on the route).
2. Document-level ACL filter applied inside the retriever, so a user only
   sees vectors whose `acl` field intersects their `groups` claim.

Both layers must be present — never rely on a single check.
"""

# Constants (scopes used across the app):
#
# class Scope(StrEnum):
#     CHAT_READ      = "chat:read"
#     CHAT_WRITE     = "chat:write"
#     INGEST_UPLOAD  = "ingest:upload"
#     INGEST_PROCESS = "ingest:process"     # for the webhook handler
#     ADMIN          = "admin"
#
# Role -> scopes mapping lives either here (static) or in Cognito groups
# (preferred) and is resolved at JWT-decode time.


# Public surface:
#
# def require_scopes(*required: Scope):
#     """FastAPI dependency factory.
#         @router.post(..., dependencies=[Depends(require_scopes(Scope.CHAT_READ))])
#     Raises AuthorizationError if any required scope is missing.
#     """
#     ...
#
# def acl_filter_for(user: AuthenticatedUser) -> dict:
#     """Build the vector-store metadata filter that restricts retrieval
#     to documents the user is allowed to see.
#
#     Returns provider-specific filter, e.g.:
#         {"bool": {"should": [
#             {"terms": {"acl.groups": user.groups}},
#             {"term":  {"acl.tenant_id": user.tenant_id}},
#         ]}}
#     """
#     ...
#
# def can_access_document(user: AuthenticatedUser, doc_meta: dict) -> bool:
#     """Post-retrieval check (defense-in-depth in case the filter was
#     bypassed)."""
#     ...
