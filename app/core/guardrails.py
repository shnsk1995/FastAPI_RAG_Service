"""Input/output guardrails.

Two stages:
- Input guardrails run BEFORE retrieval and LLM call. Cheap, fail fast.
- Output guardrails run AFTER the LLM responds, before returning to client.

Checks to implement (each returns GuardrailResult with allow / block / redact):
- PII detection (emails, phones, SSNs, credit cards) — Amazon Comprehend
  DetectPiiEntities, Presidio, or regex fallback.
- Prompt injection / jailbreak detection — model-based classifier or
  Bedrock Guardrails ContentFilter.
- Toxicity / hate / sexual / violence — Bedrock Guardrails or Perspective API.
- Off-topic detection — embedding similarity vs. allowed topic centroids.
- Secrets leakage in output — regex for API keys, JWTs.
- Hallucination citation check — every cited doc_id must exist in retrieved
  context; reject otherwise.
"""

# Data model:
#
# class GuardrailCategory(StrEnum):
#     PII = "pii"
#     INJECTION = "injection"
#     TOXICITY = "toxicity"
#     OFF_TOPIC = "off_topic"
#     SECRETS = "secrets"
#     UNCITED = "uncited"
#
# class GuardrailResult(BaseModel):
#     allowed: bool
#     redacted_text: str | None
#     violations: list[GuardrailCategory]
#     scores: dict[str, float]


# Public surface:
#
# class Guardrails:
#     def __init__(self, provider_client, policy_id, settings): ...
#
#     async def check_input(self, text: str, user: AuthenticatedUser) -> GuardrailResult:
#         # 1. PII scan -> redact (don't block) for non-sensitive scopes.
#         # 2. Prompt injection scan -> block if score > threshold.
#         # 3. Toxicity / policy -> block.
#         # Log every violation with category + score + hashed input.
#         ...
#
#     async def check_output(
#         self,
#         response_text: str,
#         retrieved_doc_ids: list[str],
#     ) -> GuardrailResult:
#         # 1. Re-run PII / toxicity / secrets on model output.
#         # 2. Verify any [doc:<id>] citations are in retrieved_doc_ids.
#         # 3. Optionally rewrite citations as URLs.
#         ...
