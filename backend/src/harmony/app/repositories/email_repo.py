from harmony.app.core import settings
from harmony.app.db import to_dynamo_json, from_dynamo_json
from .base_repo import BaseRepository

class EmailSetRepository(BaseRepository):
    table_name = settings.EMAIL_SET_TABLE_NAME
    
    def __init__(self, client):
        super().__init__(client)

    async def add_email(self, email: str):
        await self.writer.put_item(
            TableName=self.table_name,
            Item=to_dynamo_json({"email": email}),
            ConditionExpression='attribute_not_exists(email)',
        )