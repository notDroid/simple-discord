from fastapi import Depends, Request
from simple_discord.app.repositories import ChatRepository
from simple_discord.app.services import ChatService

def get_dynamo_client(request: Request):
    return request.app.state.dynamodb

def get_chat_repository(dynamodb = Depends(get_dynamo_client)) -> ChatRepository:
    return ChatRepository(dynamodb)

def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_repository)) -> ChatService:
    return ChatService(chat_repository)