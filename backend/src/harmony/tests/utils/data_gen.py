import uuid
import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_user_data():
    uid = str(uuid.uuid4())[:8]
    return {
        "username": f"user_{uid}",
        "email": f"user_{uid}@{random_string(6)}.com",
        "password": random_string(12),
    }