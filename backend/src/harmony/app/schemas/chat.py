from pydantic import BaseModel

class ChatDataItem(BaseModel):
    chat_id: str
    created_at: str

class ChatMessage(BaseModel):
    chat_id: str
    ulid: str
    timestamp: str
    user_id: str
    content: str

class ChatHistoryItem(ChatMessage):
    pass

class UserChatItem(BaseModel):
    chat_id: str
    user_id: str