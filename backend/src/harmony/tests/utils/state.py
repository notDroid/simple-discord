import asyncio
from collections import defaultdict
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .client import SimulationActor

@dataclass
class SimConfig:
    MAX_USERS: int = 50

class SimState:
    def __init__(self, config: SimConfig):
        self.config = config
        self.actors: List[SimulationActor] = []
        self.user_memberships = defaultdict(list) 

    def add_actor(self, actor: SimulationActor):
        self.actors.append(actor)

    def register_chat(self, chat_id: str, participant_ids: List[str]):
        """Record that these users are in this chat"""
        for uid in participant_ids:
            self.user_memberships[uid].append(chat_id)

    def get_chat_for_user(self, user_id: str) -> str | None:
        """Get a known valid chat ID for this user"""
        chats = self.user_memberships.get(user_id, [])
        if not chats: 
            return None
        return random.choice(chats)
        
    def get_random_actor(self) -> SimulationActor | None:
        if not self.actors:
            return None
        return random.choice(self.actors)