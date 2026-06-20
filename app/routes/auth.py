from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.vault import create_user, get_user
from app.core.security import hash_password, verify_password, create_token

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str
    scope: list[str] = []

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(req: RegisterRequest):
    if get_user(req.username):
        raise HTTPException(status_code=400, detail="User already exists")
    create_user(req.username, hash_password(req.password), req.scope or [req.username])
    return {"message": "User created"}

@router.post("/login")
def login(req: LoginRequest):
    user = get_user(req.username)
    if not user or not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user["username"], "scope": user["scope"]})
    return {"access_token": token, "token_type": "bearer"}
