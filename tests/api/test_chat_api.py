from fastapi.testclient import TestClient

from app.api.deps import get_chat_service
from app.schemas.chat import ChatCompletionResponse
from app.schemas.chat import ChatHistoryResponse, ChatMessage

class FakeChatService:
    async def generate_response(self, request):

        return ChatCompletionResponse(
            conversation_id=request.conversation_id or "test-conversation-id",
            message=f"Fake answer for: {request.message}",
        )

    async def get_chat_history(self, conversation_id: str):
        return ChatHistoryResponse(
            conversation_id=conversation_id,
            chat_history=[
                ChatMessage(
                    role="user",
                    content="Hello",
                    created_at="2026-05-30T10:00:00Z",
                ),
                ChatMessage(
                    role="assistant",
                    content="Hi, how can I help?",
                    created_at="2026-05-30T10:00:01Z",
                ),
            ],
        )

    


def override_get_chat_service():
    return FakeChatService()


def test_chat_completion_success(app, client):
    app.dependency_overrides[get_chat_service] = override_get_chat_service


    response = client.post(
        "/api/v1/chat",
        json={
            "message" : "Explain RAG",
        },
    )


    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Fake answer for: Explain RAG"
    assert data["conversation_id"] == "test-conversation-id"

def test_chat_completion_requires_message(client):
    response = client.post(
        "/api/v1/chat",
        json={
            "conversation_id" : "test-conversation-1"
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["message"] == "Invalid request payload"

    assert len(data["details"]) > 0
    assert data["details"][0]["field"] == "body.message"
    assert data["details"][0]["type"] == "missing"

def test_get_conversation_history_success(app, client):
    app.dependency_overrides[get_chat_service] = override_get_chat_service

    response = client.get(
        "/api/v1/chat/test-conversation-1/messages"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["conversation_id"] == "test-conversation-1"
    assert len(data["chat_history"]) == 2

    assert data["chat_history"][0]["role"] == "user"
    assert data["chat_history"][0]["content"] == "Hello"

    assert data["chat_history"][1]["role"] == "assistant"
    assert data["chat_history"][1]["content"] == "Hi, how can I help?"