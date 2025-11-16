from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth import handle_login, handle_registration, handle_logout

# initialize FastAPI application
app = FastAPI(title= "Login")

class LoginRequest(BaseModel):
    # data model for login request
    username: str
    password: str

class RegisterRequest(BaseModel):
    # data model for registration requests
    username: str
    password: str

class LogoutRequest(BaseModel):
    # data model for logout requests
    user_id: str
    session_token: str

class AuthorizationResponse(BaseModel):
    # data model for responses
    status: str
    user_id: str | None = None
    session_token: str | None = None
    profile_data: dict | None = None
    error_message: str | None = None

# API endpoints
@app.post("/login", response_model=AuthorizationResponse)
def login(request: LoginRequest):
    """Login endpoint accepts username and password"""
    result = handle_login(request.username, request.password)
    if result["status"] == "failure":
        raise HTTPException(status_code=401, detail=result["error_message"])
    return result

@app.post("/register", response_model=AuthorizationResponse)
def register(request: RegisterRequest):
    """Registration endpoint accepts username and password"""
    result = handle_registration(request.username, request.password)
    if result["status"] == "failure":
        raise HTTPException(status_code=400, detail=result["error_message"])
    return result

@app.post("/logout", response_model=AuthorizationResponse)
def logout(request: LogoutRequest):
    """Logs the user out by invalidating the session token"""
    result = handle_logout(request.user_id, request.session_token)
    if result["status"] == "failure":
        raise HTTPException(status_code=400, detail=result["error_message"])
    return result