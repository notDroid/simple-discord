from pydantic import BaseModel
from .user import UserMetaData

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(BaseModel):
    password: str
    metadata: UserMetaData

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"