import pytest

from app.schemas.chat import ChatCompletionRequest
from app.schemas.input_guardrail import InputGuardrailResult
from app.services.chat_service import ChatService

class FakeLLMClient:
    def __init__(self):
        self.received_messages = None

    async def generate_response(self, messages):
        self.received_messages = messages
        return "Fake LLM answer"




class FakeConversationStore:
    def __init__(self):
        self.saved_messages = []

    def get_messages(self, conversation_id: str, limit: int = 20):
        return [
            {
                "role": "user",
                "content": "My name is Hari.",
                "created_at": "2026-05-30T10:00:00Z",
            },
            {
                "role": "assistant",
                "content": "Nice to meet you, Hari.",
                "created_at": "2026-05-30T10:00:01Z",
            },
        ]

    def save_message(self, conversation_id: str, role: str, content: str):
        self.saved_messages.append(
            {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
            }
        )

class FakeInputGuardrailClient:
    def __init__(self):
        self.raw_input = None
    
    async def process_input(self, raw_input : str):
        self.raw_input = raw_input

        return InputGuardrailResult(
            original_input=self.raw_input,
            processed_input=self.raw_input.strip(),
            was_blocked=False,
            block_reason=None,
            guardrail_action='none',
            pii_detected=False,
            prompt_attack_detected=False,
        )




@pytest.mark.asyncio
async def test_chat_service_uses_history_and_saves_messages():
    llm_client = FakeLLMClient()
    conversation_store = FakeConversationStore()
    input_guardrail_client = FakeInputGuardrailClient()

    service = ChatService(
        llm_client=llm_client,
        conversation_store=conversation_store,
        input_guardrail_client=input_guardrail_client,
    )

    request = ChatCompletionRequest(
        message="What is my name?",
        conversation_id="test-conversation-1",
    )

    response = await service.generate_response(request)

    assert response.message == "Fake LLM answer"
    assert response.conversation_id == "test-conversation-1"

    assert llm_client.received_messages == [
        {
            "role": "user",
            "content": "My name is Hari.",
        },
        {
            "role": "assistant",
            "content": "Nice to meet you, Hari.",
        },
        {
            "role": "user",
            "content": "What is my name?",
        },
    ]

    assert conversation_store.saved_messages == [
        {
            "conversation_id": "test-conversation-1",
            "role": "user",
            "content": "What is my name?",
        },
        {
            "conversation_id": "test-conversation-1",
            "role": "assistant",
            "content": "Fake LLM answer",
        },
    ]

    assert input_guardrail_client.raw_input == "What is my name?"