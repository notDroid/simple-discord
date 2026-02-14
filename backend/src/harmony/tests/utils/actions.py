import uuid
from httpx import HTTPStatusError

import random
from harmony.tests.utils.client import AppClient, SimulationActor
from harmony.tests.utils.data_gen import generate_user_data
from .state import SimState

# ==========================================
# ACTION REGISTRY
# ==========================================
ACTION_REGISTRY = {}

def simulation_action(name: str, weight: int):
    def decorator(func):
        ACTION_REGISTRY[name] = {
            "func": func, 
            "weight": weight,
            "name": name
        }
        return func
    return decorator

# ==========================================
# HAPPY PATH ACTIONS
# ==========================================

@simulation_action(name="create_user", weight=10)
async def action_create_user(client: AppClient, state: SimState):
    # Throttle locally
    if len(state.actors) >= state.config.MAX_USERS:
        return 
        
    data = generate_user_data()
    # We allow this to bubble up exceptions if the API fails
    uid = await client.create_user(**data)
    
    actor = SimulationActor(uid, data['username'], client)
    state.add_actor(actor)

@simulation_action(name="create_chat", weight=20)
async def action_create_chat(client: AppClient, state: SimState):
    # Need at least 2 users to chat
    if len(state.actors) < 2: 
        return
        
    # Guaranteed to exist because we own the state
    creator, other = random.sample(state.actors, 2)
    
    chat_id = await creator.create_chat_with([other])
    state.register_chat(chat_id, [creator.user_id, other.user_id])

@simulation_action(name="send_message", weight=50)
async def action_send_message(client: AppClient, state: SimState):
    actor = state.get_random_actor()
    if not actor: return

    chat_id = state.get_chat_for_user(actor.user_id)
    if not chat_id: 
        # User exists but has no chats yet. 
        # This is a valid simulation state, so we just return.
        return

    await actor.send_message(chat_id, "Happy path payload")

@simulation_action(name="read_history", weight=40)
async def action_read_history(client: AppClient, state: SimState):
    actor = state.get_random_actor()
    if not actor: return

    chat_id = state.get_chat_for_user(actor.user_id)
    if not chat_id: return

    await actor.get_history(chat_id)

# ==========================================
# SAD PATH / FAILURE SCENARIO ACTIONS
# ==========================================

@simulation_action(name="fail_unauthorized_read", weight=15)
async def action_fail_unauthorized_read(client: AppClient, state: SimState):
    """
    Scenario: A user tries to read the history of a chat they are NOT a member of.
    Expected Result: 403 Forbidden (or 404 Not Found, depending on security design).
    """
    actor = state.get_random_actor()
    if not actor: return

    # 1. Find a chat ID that belongs to someone else, but NOT this actor
    target_chat_id = None
    my_chats = set(state.user_memberships.get(actor.user_id, []))
    
    # Scan all registered chats in the state
    all_chats = set(chat_id for chat_list in state.user_memberships.values() for chat_id in chat_list)
    forbidden_chats = list(all_chats - my_chats)

    if not forbidden_chats:
        return # No forbidden chats exist yet

    target_chat_id = random.choice(forbidden_chats)

    # 2. Attempt access and assert failure
    try:
        await actor.get_history(target_chat_id)
        # If we reach here, it's a security bug!
        print(f"CRITICAL: User {actor.username} successfully read chat {target_chat_id} they don't belong to!")
    except HTTPStatusError as e:
        # We expect a 403 or 404. 
        if e.response.status_code not in [403, 404]:
            print(f"Unexpected error code during unauthorized read: {e.response.status_code}")
            raise e

@simulation_action(name="fail_message_nonexistent_chat", weight=10)
async def action_fail_message_ghost_chat(client: AppClient, state: SimState):
    """
    Scenario: User sends a message to a UUID that doesn't exist.
    Expected Result: 404 Not Found.
    """
    actor = state.get_random_actor()
    if not actor: return

    # Generate a random UUID that definitely doesn't exist
    fake_chat_id = str(uuid.uuid4())

    try:
        await actor.send_message(fake_chat_id, "Hello into the void")
        print(f"CRITICAL: API accepted message to non-existent chat {fake_chat_id}")
    except HTTPStatusError as e:
        if e.response.status_code != 404:
            print(f"Expected 404 for ghost chat, got {e.response.status_code}")
            raise e

@simulation_action(name="chaos_delete_user", weight=5)
async def action_chaos_delete_user(client: AppClient, state: SimState):
    """
    Scenario: A user deletes their account. 
    This is a 'Sad Path' generator because it breaks existing chats for other users.
    """
    actor = state.get_random_actor()
    if not actor: return
    
    # Don't delete if it's the last user (keeps sim running)
    if len(state.actors) <= 1: return

    # 1. Perform deletion
    try:
        await actor.delete_self()
    except HTTPStatusError as e:
        print(f"Failed to delete user {actor.user_id}: {e}")
        return

    # 2. Update Simulation State 
    # (Crucial: prevent the sim from choosing this actor again)
    if actor in state.actors:
        state.actors.remove(actor)
    
    # Note: We do NOT remove the chat memberships immediately.
    # This allows testing "Scenario 5" (messaging a deleted user) naturally
    # as other actors might still try to message a chat involving this deleted user.

@simulation_action(name="fail_message_deleted_user", weight=10)
async def action_fail_message_deleted_user(client: AppClient, state: SimState):
    """
    Scenario: Attempt to message a chat where the OTHER user has been deleted.
    Depending on your API logic, this might succeed (ghost user) or fail.
    Let's assume we want it to fail or at least handle it gracefully.
    """
    actor = state.get_random_actor()
    if not actor: return

    chat_id = state.get_chat_for_user(actor.user_id)
    if not chat_id: return

    # Try to send. If the other user in this chat was deleted by 
    # 'chaos_delete_user', the API might throw an error.
    try:
        await actor.send_message(chat_id, "Are you still there?")
    except HTTPStatusError as e:
        # If your API is designed to close chats when a user leaves, 
        # this 404/403 is actually a success for the test.
        if e.response.status_code in [403, 404]:
            # Clean up state so we don't keep retrying this dead chat
            if chat_id in state.user_memberships[actor.user_id]:
                state.user_memberships[actor.user_id].remove(chat_id)
        else:
            raise e