import pytest
from harmony.tests.utils.data_gen import generate_user_data
from harmony.tests.utils.client import AppClient

@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_user_flow(app_client: AppClient):
    # Arrange
    user_data = generate_user_data()

    # Act
    user_id = await app_client.create_user(**user_data)

    # Assert
    assert isinstance(user_id, str)
    assert len(user_id) > 0

    # Verify side effects (e.g., getting chat list should return empty list initially)
    chats = await app_client.get_user_chats(user_id)
    assert chats == []

@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_user_flow(app_client: AppClient):
    # Arrange
    user_data = generate_user_data()

    # Act
    user_id = await app_client.create_user(**user_data)

    # Assert
    assert isinstance(user_id, str)
    assert len(user_id) > 0

    # Verify side effects (e.g., getting chat list should return empty list initially)
    chats = await app_client.get_user_chats(user_id)
    assert chats == []

    # Act - Delete the user
    await app_client.delete_user(user_id)

    # nothing to assert here, just ensure no exceptions and user is effectively deleted