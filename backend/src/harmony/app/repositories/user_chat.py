from harmony.app.core import settings
from harmony.app.db import to_dynamo_json, from_dynamo_json
from harmony.app.schemas import UserChatItem
from .base_repo import BaseRepository

class UserChatRepository(BaseRepository):
    table_name = settings.USER_CHAT_TABLE_NAME
    
    def __init__(self, client):
        super().__init__(client)

    async def create_chat(self, chat_id: str, user_id_list: list[str]):
        items = [
            to_dynamo_json({
                "user_id": user_id,
                "chat_id": chat_id
            })
            for user_id in user_id_list
        ]
        await self.writer.put_batch(TableName=self.table_name, Items=items)

    async def verify_user_chat(self, chat_id: str, user_id: str):
        response = await self.client.get_item(
            TableName=self.table_name,
            Key=to_dynamo_json({
                "user_id": user_id,
                "chat_id": chat_id
            })
        )
        return "Item" in response

    async def get_user_chats(self, user_id: str) -> list[str]:
        response = await self.client.query(
            TableName=self.table_name,
            KeyConditionExpression="user_id = :uid",
            ExpressionAttributeValues=to_dynamo_json({
                ":uid": user_id
            })
        )
        chat_id_list = [
            from_dynamo_json(item)["chat_id"]
            for item in response.get("Items", [])
        ]
        return chat_id_list

    async def delete_chat(self, chat_id: str):
        response = await self.client.query(
            TableName=self.table_name,
            IndexName="ChatIdIndex",
            KeyConditionExpression="chat_id = :cid",
            ExpressionAttributeValues=to_dynamo_json({
                ":cid": chat_id
            }),
            ProjectionExpression="user_id"
        )
        
        keys = [
            to_dynamo_json({
                "user_id": from_dynamo_json(item)["user_id"],
                "chat_id": chat_id
            })
            for item in response.get("Items", [])
        ]
        await self.writer.delete_batch(TableName=self.table_name, Keys=keys)