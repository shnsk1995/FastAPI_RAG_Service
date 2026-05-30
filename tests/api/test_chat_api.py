from fastapi.testclient import TestClient

from app.api.deps import get_chat_service
from app.main import create_app
from app.schemas.chat import ChatCompletionResponse

class FakeChatService:
    async def generate_response(self, request):

        return ChatCompletionResponse(
            conversation_id=request.conversation_id or "test-conversation-id",
            message=f"Fake answer for: {request.message}",
        )


def override_get_chat_service():
    return FakeChatService()


def test_chat_completion_success():
    app = create_app()
    app.dependency_overrides[get_chat_service] = override_get_chat_service

    client = TestClient(app)

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

    app.dependency_overrides.clear()