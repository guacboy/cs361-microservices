import uuid
import hashlib
from database import load_users, save_users

active_sessions = {}

def hash_password(password: str):
    """Securely hash the user's password."""
    return hashlib.sha256(password.encode()).hexdigest()

def handle_login(username: str, password: str):
    """Function to to validate the user's login credentials"""
    users_db = load_users()
    user = users_db.get(username)
    hashed_pwd = hash_password(password)
    if not user:
        return {"status": "failure", "error_message": "User does not exist."}

    if user["password_hash"] != hashed_pwd:
        return {"status": "failure", "error_message": "Invalid password."}

    token = str(uuid.uuid4())
    user["session_token"] = token
    users_db[username] = user
    save_users(users_db)

    return {
        "status": "success",
        "user_id": user["user_id"],
        "session_token": token
    }

def handle_registration(username: str, password: str):
    """Function to handle the user's registration request"""
    users_db = load_users()

    if username in users_db:
        return {"status": "failure", "error_message": "Username already exists."}

    if len(password) < 8 or len(password) > 12:
        return {"status": "failure", "error_message": "Password must be between 8 and 12 characters long."}

    user_id = f"u{len(users_db)+1:03d}"
    hashed_pwd = hash_password(password)
    token = str(uuid.uuid4())

    users_db[username] = {
        "user_id": user_id,
        "password_hash": hashed_pwd,
        "session_token": token
    }

    save_users(users_db)

    return {
        "status": "success",
        "user_id": user_id,
        "session_token": token
    }

def handle_logout(user_id: str, session_token: str):
    """Function to log the user out by invalidating their session token"""
    users_db = load_users()

    username = next((u for u, data in users_db.items() if data["user_id"] == user_id), None)
    if not username or users_db[username]["session_token"] != session_token:
        return {"status": "failure", "error_message": "Invalid session token."}

    users_db[username]["session_token"] = None
    save_users(users_db)

    return {"status": "success", "user_id": user_id, "session_token": None}