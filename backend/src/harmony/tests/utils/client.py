from httpx import AsyncClient, Response
from typing import List, Optional
from harmony.app.schemas import *

class AppClient:
    """
    Wraps raw HTTP calls. 
    If endpoints change paths, modify this class, not the tests.
    """
    def __init__(self, client: AsyncClient, api_prefix: str = "/api/v1"):
        self.client = client
        self.prefix = api_prefix

    async def create_user(self, username: str, email: str, password: str = None) -> str:
        payload = {"username": username, "email": email}
        if password:
            payload["password"] = password
            
        res = await self.client.post(f"{self.prefix}/users/", json=payload)
        res.raise_for_status()
        return res.json()["user_id"]
    
    async def delete_user(self, user_id: str):
        res = await self.client.delete(f"{self.prefix}/users/{user_id}")
        res.raise_for_status()

    async def create_chat(self, user_id: str, user_ids: List[str]) -> str:
        payload = {"user_id_list": user_ids}
        res = await self.client.post(f"{self.prefix}/chats/", params={"user_id": user_id}, json=payload)
        res.raise_for_status()
        return res.json()["chat_id"]

    async def send_message(self, chat_id: str, user_id: str, content: str) -> SendMessageResponse:
        # FUTURE AUTH NOTE: When you switch to tokens, remove `user_id` from payload 
        # and ensure the client sends the Authorization header.
        payload = {"content": content}
        res = await self.client.post(f"{self.prefix}/chats/{chat_id}", params={"user_id": user_id}, json=payload)
        res.raise_for_status()
        return SendMessageResponse(**res.json())

    async def get_chat_history(self, chat_id: str, as_user_id: str) -> GetChatHistoryResponse:
        # FUTURE AUTH NOTE: When you switch to tokens, remove params={"user_id": ...}
        res = await self.client.get(
            f"{self.prefix}/chats/{chat_id}", 
            params={"user_id": as_user_id}
        )
        res.raise_for_status()
        return GetChatHistoryResponse(**res.json())

    async def get_user_chats(self, user_id: str) -> List[str]:
        res = await self.client.get(f"{self.prefix}/users/{user_id}/chats")
        res.raise_for_status()
        return res.json()["chat_id_list"]
    
    async def delete_chat(self, chat_id: str, user_id: str):
        # Using query param as per your controller signature
        res = await self.client.delete(f"{self.prefix}/chats/{chat_id}", params={"user_id": user_id})
        res.raise_for_status()


class SimulationActor:
    """
    Represents a specific user in the test environment.
    Makes tests read like stories: `alice.send_message(...)`
    """
    def __init__(self, user_id: str, username: str, client: AppClient):
        self.user_id = user_id
        self.username = username
        self.client = client

    async def create_chat_with(self, other_actors: List['SimulationActor']) -> str:
        ids = [a.user_id for a in other_actors]
        chat_id = await self.client.create_chat(self.user_id, ids)
        return chat_id

    async def send_message(self, chat_id: str, content: str):
        return await self.client.send_message(chat_id, self.user_id, content)

    async def get_history(self, chat_id: str):
        resp = await self.client.get_chat_history(chat_id, self.user_id)
        return resp.messages

    async def get_my_chats(self):
        return await self.client.get_user_chats(self.user_id)
    
    async def delete_chat(self, chat_id: str):
        await self.client.delete_chat(chat_id, self.user_id)

    async def delete_self(self):
        await self.client.delete_user(self.user_id)