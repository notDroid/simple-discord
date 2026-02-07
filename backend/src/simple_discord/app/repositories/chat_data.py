from simple_discord.app.core import settings
from simple_discord.app.db import to_dynamo_json, from_dynamo_json
from simple_discord.app.schemas import ChatDataItem
from .base_repo import BaseRepository

class ChatDataRepository(BaseRepository):
    table_name = settings.CHAT_DATA_TABLE_NAME
    
    def __init__(self, client):
        super().__init__(client)

    async def create_chat(self, item: ChatDataItem):
        dynamo_item = to_dynamo_json(item.model_dump())

        await self.writer.put_item(
            TableName=self.table_name,
            Item=dynamo_item,
            ConditionExpression='attribute_not_exists(chat_id)',
        )

    async def get_chat_by_id(self, chat_id: str) -> ChatDataItem | None:
        response = await self.client.get_item(
            TableName=self.table_name,
            Key=to_dynamo_json({"chat_id": chat_id})
        )
        item = response.get("Item")
        if not item:
            return None
        chat_data = from_dynamo_json(item)
        return ChatDataItem.model_validate(chat_data)
    
    async def chat_exists(self, chat_id: str) -> bool:
        response = await self.client.get_item(
            TableName=self.table_name,
            Key=to_dynamo_json({"chat_id": chat_id}),
            ProjectionExpression="chat_id"
        )
        return "Item" in response
    
    async def delete_chat(self, chat_id: str):

        await self.writer.delete_item(
            TableName=self.table_name,
            Key=to_dynamo_json({"chat_id": chat_id})
        )