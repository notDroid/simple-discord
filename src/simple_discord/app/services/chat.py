from ulid import ULID
from datetime import datetime, timezone

from simple_discord.app.schemas import *
from simple_discord.app.repositories import ChatRepository


class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    async def send_message(self, chat_id: str, user_id: str, content: str):
        ulid_val = ULID()
        ulid_str = str(ulid_val)
        timestamp = datetime.fromtimestamp(ulid_val.timestamp, timezone.utc).isoformat()

        msg = ChatMessage(
            chat_id=chat_id,
            ulid=ulid_str,
            timestamp=timestamp,
            user_id=user_id,
            content=content
        )

        await self.chat_repository.create_message(msg)

        return timestamp

    async def get_chat_history(self, chat_id: str):
        messages = await self.chat_repository.get_chat_history(chat_id)
        return GetChatHistoryResponse(messages=messages)