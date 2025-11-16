import json
import os

DATA_FILE = "users.json"

def load_users() -> dict:
    """Load the user database from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users_db: dict):
    """Save the user database to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(users_db, f, indent=4)