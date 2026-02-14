from pydantic import BaseModel, EmailStr

class UserMetaData(BaseModel):
    username: str
    email: EmailStr
    created_at: str | None

class UserDataItem(BaseModel):
    user_id: str
    tombstone: bool
    hashed_password: str | None = None
    metadata: UserMetaData

class UserCreate(BaseModel):
    username: str | None 
    email: EmailStr | None
    password: str | None = None # Optional for third-party auth flows