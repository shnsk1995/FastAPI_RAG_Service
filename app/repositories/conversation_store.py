"""Conversation history store (DynamoDB).

Table layout (`conversations`):
    PK: conversation_id
    SK: ts#<ulid>                     # one item per message
    Attrs: role, content, citations, usage, model, user_id, tenant_id

Sort key prefix lets us page through history in time order. Add a TTL
attribute for automatic purging based on retention policy.
"""

# class ConversationStore(Protocol):
#     async def create(self, user: AuthenticatedUser) -> str: ...   # returns conversation_id
#
#     async def append(
#         self, conversation_id: str, message: ChatMessage,
#         citations: list[Citation] | None = None,
#         usage: TokenUsage | None = None,
#     ) -> None: ...
#
#     async def get_recent(
#         self, conversation_id: str, max_messages: int = 20,
#     ) -> list[ChatMessage]: ...
#
#     async def delete(self, conversation_id: str, user: AuthenticatedUser) -> None: ...
#
#     async def assert_owner(self, conversation_id: str, user: AuthenticatedUser) -> None:
#         """Raise AuthorizationError unless user owns this conversation."""
#         ...

from datetime import datetime, timezone
from typing import Literal

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import BotoCoreError, ClientError

from app.config import settings
from app.exceptions import ConversationStoreError


MessageRole = Literal["user","assistant"]


class ConversationStore:
    def __init__(self):
        if not settings.DDB_CONVERSATIONS_TABLE:
            raise ConversationStoreError("DDB_CONVERSATIONS_TABLE is missing")

        session = boto3.Session(
            profile_name=settings.AWS_PROFILE,
            region_name=settings.AWS_REGION
        )

        dynamodb = session.resource("dynamodb")

        self.table = dynamodb.Table(settings.DDB_CONVERSATIONS_TABLE)


    def save_message(self, conversation_id: str, role: MessageRole, content: str) -> None:
        
        try:

            created_at = datetime.now(timezone.utc).isoformat()

            self.table.put_item(
                Item={
                    "conversation_id" : conversation_id,
                    "created_at" : created_at,
                    "role" : role,
                    "content" : content
                }
            )

        except (BotoCoreError, ClientError) as exc:
            raise ConversationStoreError(
                "Failed to save conversation message"
            ) from exc


    
    def get_messages(self, conversation_id: str, limit: int = 20) -> list[dict]:
        
        try:

            response = self.table.query(
                KeyConditionExpression=Key("conversation_id").eq(conversation_id),
                ScanIndexForward=False,
                Limit=limit,
            )


            items = response.get("Items",[])

            return list(reversed(items))

        except (BotoCoreError, ClientError) as exc:
            raise ConversationStoreError(
                "Failed to fetch conversation history"
            ) from exc