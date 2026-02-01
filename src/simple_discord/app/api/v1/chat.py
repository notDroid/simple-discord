from simple_discord.app.schemas import *
from .dependencies import get_chat_service

from fastapi import Depends
from fastapi import APIRouter

router = APIRouter()

@router.post("/{chat_id}", response_model=SendMessageResponse, status_code=201)
async def send_message(
    chat_id: str,
    msg: SendMessageRequest, 
    chat_service = Depends(get_chat_service)
):
    timestamp = await chat_service.send_message(
        chat_id=chat_id, 
        user_id=msg.user_id, 
        content=msg.content
    )
    return {"status": "Message sent", "timestamp": timestamp}

@router.get("/{chat_id}", response_model=GetChatHistoryResponse)
async def get_chat_history(
    chat_id: str,
    chat_service = Depends(get_chat_service)
):
    return await chat_service.get_chat_history(chat_id=chat_id)