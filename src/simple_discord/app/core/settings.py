from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_REGION: str = "us-east-1"
    DYNAMODB_ENDPOINT: str = "http://localhost:8000"
    CHAT_HISTORY_TABLE_NAME: str = "ChatHistory"

settings = Settings()