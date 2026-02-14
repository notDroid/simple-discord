from harmony.app.schemas import *
from .dependencies import get_user_service

from fastapi import Depends, APIRouter

router = APIRouter()

'''
API endpoints for user operations.

POST /
  Body:    { ... } (CreateUserRequest)
  Returns: { "user_id": "<str>" }

GET /{user_id}/chats
  Returns: { "chat_id_list": ["<str>", ...] }

DELETE /{user_id}
  Status:  204 No Content
'''

@router.post("/", response_model=CreateUserResponse)
async def create_user(
    meta_data: CreateUserRequest,
    user_service = Depends(get_user_service)
):
    user_id = await user_service.create_user(meta_data)
    return {"user_id": user_id}

@router.get("/{user_id}/chats", response_model=GetUserChatsResponse)
async def get_user_chats(
    user_id: str,
    user_service = Depends(get_user_service)
):
    chats = await user_service.get_user_chats(user_id=user_id)
    return GetUserChatsResponse(chat_id_list=chats)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    user_service = Depends(get_user_service)
):
    await user_service.delete_user(user_id=user_id)