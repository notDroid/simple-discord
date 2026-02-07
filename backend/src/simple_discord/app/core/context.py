from contextvars import ContextVar
from typing import List, Optional, Protocol

class DynamoDBWriter(Protocol):
    async def put_item(self, TableName: str, Item: dict, ConditionExpression: str = None, **kwargs) -> None:
        ...

    async def delete_item(self, TableName: str, Key: dict) -> None:
        ...

    async def batch_put(self, TableName: str, Items: List[dict]) -> None:
        ...

    async def delete_batch(self, TableName: str, Keys: List[dict]) -> None:
        ...
    
active_writer_var: ContextVar[Optional['DynamoDBWriter']] = ContextVar("active_writer", default=None)