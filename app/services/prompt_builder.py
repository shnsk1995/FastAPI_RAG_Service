"""Prompt construction with Anthropic prompt caching.

Layout (longest -> shortest static prefix maximises cache reuse):

    system: [
        { type: "text", text: <static system instructions>,
          cache_control: { type: "ephemeral" } },                # block 1
        { type: "text", text: <retrieved documents serialised>,
          cache_control: { type: "ephemeral" } },                # block 2
    ]
    messages: [
        ...prior_turns_from_conversation_store,
        { role: "user", content: <current question> },           # dynamic
    ]

Rules:
- Anthropic cache hits require the FIRST N tokens of the prompt to be
  byte-identical. Put static, large content first.
- Cache breakpoints: a max of 4 `cache_control` markers per request.
- Document block format should be deterministic — sort chunks by doc_id then
  chunk_id, render with stable separators so the same retrieval yields the
  same bytes.
- Tools (if any) go inside system before the documents block so they remain
  cacheable.

Output guardrails depend on stable citation markers — instruct the model to
cite as [doc:<document_id>#<chunk_id>] so we can verify hallucinations.
"""

# SYSTEM_INSTRUCTIONS = """You are a helpful assistant grounded in the
# provided documents. Cite every factual claim as [doc:<id>#<chunk>]. If the
# answer is not present in the documents, say you don't know. ..."""
#
# class PromptBuilder:
#     def __init__(self, settings): ...
#
#     def build(
#         self,
#         documents: list[RetrievedChunk],
#         history: list[ChatMessage],
#         question: str,
#     ) -> AnthropicMessagesRequest:
#         """Return a dict ready to pass to anthropic.messages.create.
#         - serialise_documents(documents) -> stable text block
#         - apply cache_control to system + documents blocks
#         - append history + current question to `messages`
#         """
#         ...
#
#     @staticmethod
#     def serialise_documents(docs: list[RetrievedChunk]) -> str:
#         """Deterministic rendering, e.g.:
#             <doc id="abc" chunk="0" title="...">
#             <text>...</text>
#             </doc>
#         """
#         ...
