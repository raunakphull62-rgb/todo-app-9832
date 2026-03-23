from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import SupabaseError
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from config import settings
from auth import verify_token

router = APIRouter()

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class User(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str

@router.post("/register")
async def register(user: User):
    try:
        data = supabase.from_("users").insert([{"username": user.username, "password": user.password}]).execute()
        return UserResponse(id=data[0]["id"], username=data[0]["username"])
    except SupabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: User):
    try:
        data = supabase.from_("users").select("id, username").eq("username", user.username).execute()
        if len(data) == 0 or data[0]["username"] != user.username:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        if data[0]["password"] != user.password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=60),
            "iat": datetime.utcnow(),
            "sub": data[0]["id"],
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return {"token": token}
    except SupabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me")
async def get_me(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = verify_token(token.credentials)
        data = supabase.from_("users").select("id, username").eq("id", payload["sub"]).execute()
        return UserResponse(id=data[0]["id"], username=data[0]["username"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except SupabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))