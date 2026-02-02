from simple_discord.app.repositories import UserChatRepository, UserDataRepository
from simple_discord.app.schemas import UserDataItem, UserMetaData

from ulid import ULID
from datetime import datetime, timezone

class UserService:
    
    def __init__(
            self,
            user_chat_repository: UserChatRepository, 
            user_data_repository: UserDataRepository
    ):
        self.user_chat_repository = user_chat_repository
        self.user_data_repository = user_data_repository

    async def verify_user_in_chat(self, user_id: str, chat_id: str) -> bool:
        return await self.user_chat_repository.verify_user_chat(chat_id=chat_id, user_id=user_id)
    
    async def get_user_by_id(self, user_id: str) -> UserDataItem | None:
        return await self.user_data_repository.get_user_by_id(user_id)
    
    async def user_exists(self, user_id: str) -> bool:
        user_data =  await self.user_data_repository.get_user_by_id(user_id)
        return user_data is not None
    
    async def create_user(self, user_metadata: UserMetaData):
        ulid_val = ULID()
        user_id = str(ulid_val)
        timestamp = datetime.fromtimestamp(ulid_val.timestamp, timezone.utc).isoformat()

        user_data_item = UserDataItem(
            user_id=user_id,
            created_at=timestamp,
            metadata=user_metadata
        )
        await self.user_data_repository.create_user(user_data_item)
        return user_id