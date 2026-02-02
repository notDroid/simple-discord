from simple_discord.app.schemas import *
from .dependencies import get_user_service

from fastapi import Depends
from fastapi import APIRouter

router = APIRouter()

'''
API endpoints for user operations.

Create User:
    - POST /
    - Request: CreateUserRequest (username, email)
    - Response: CreateUserResponse (user_id)
    desc: Create a new user with a username and email.
'''

@router.post("/", response_model=CreateUserResponse)
async def create_user(
    msg: CreateUserRequest,
    user_service = Depends(get_user_service)
):
    user_id = await user_service.create_user(msg)
    print(f"Created user with ID: {user_id}")
    return {"user_id": user_id}