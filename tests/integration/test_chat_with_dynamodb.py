import pytest

from app.api.deps import get_llm_client
from app.repositories.conversation_store import ConversationStore


class FakeLLMClient:
    async def generate_response(self, messages):
        return "Fake integration test answer"

    
def override_get_llm_client():
    return FakeLLMClient()

@pytest.mark.integration
def test_chat_saves_messages_to_dynamodb(app, client):
    app.dependency_overrides[get_llm_client]=override_get_llm_client

    chat_response = client.post(
        "/api/v1/chat",
        json={
            "message" : "Hello from integration test"
        },
    )

    assert chat_response.status_code == 200

    chat_data = chat_response.json()

    assert chat_data["message"] == "Fake integration test answer"
    assert chat_data["conversation_id"]

    conversation_id = chat_data["conversation_id"]

    
    try:

        history_response = client.get(
            f"/api/v1/chat/{conversation_id}/messages"
        )

        assert history_response.status_code == 200

        history_data = history_response.json()

        assert history_data["conversation_id"] == conversation_id
        assert len(history_data["chat_history"]) == 2

        assert history_data["chat_history"][0]["role"] == "user"
        assert history_data["chat_history"][0]["content"] == "Hello from integration test"

        assert history_data["chat_history"][1]["role"] == "assistant"
        assert history_data["chat_history"][1]["content"] == "Fake integration test answer"
    
    finally:
        store = ConversationStore()
        store.delete_conversation(conversation_id)

