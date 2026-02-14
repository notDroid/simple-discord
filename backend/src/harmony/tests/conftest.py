import os
from harmony.tests.utils.client import AppClient
from httpx import AsyncClient
import pytest_asyncio
import pytest

API_ENDPOINT = os.getenv("API_ENDPOINT", "http://localhost:8000")
API_PATH = os.getenv("API_PATH", "/api/v1")

@pytest_asyncio.fixture
async def raw_client():
    async with AsyncClient(base_url=API_ENDPOINT) as ac:
        yield ac

@pytest_asyncio.fixture
def app_client(raw_client):
    return AppClient(raw_client)

@pytest_asyncio.fixture
async def api_path():
    return API_PATH

def pytest_configure(config):
    config.addinivalue_line("markers", "stress: Marks tests as stress tests")
    config.addinivalue_line("markers", "integration: Marks tests as integration tests")