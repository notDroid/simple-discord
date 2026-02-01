from pydantic import BaseModel

__ALL__ = [
    "ChatMessage",
    "SendMessageRequest",
    "SendMessageResponse",
    "GetChatHistoryResponse",
]

class ChatMessage(BaseModel):
    chat_id: str
    ulid: str
    timestamp: str
    user_id: str
    content: str

class SendMessageRequest(BaseModel):
    user_id: str
    content: str

class SendMessageResponse(BaseModel):
    status: str
    timestamp: str

class GetChatHistoryResponse(BaseModel):
    messages: list[ChatMessage]