from supabase import create_client, Client
from fastapi import HTTPException
from typing import Optional

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise HTTPException(status_code=500, detail="Supabase URL and key are required")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_supabase() -> Client:
    return supabase

async def get_user_id_from_token(token: str) -> Optional[str]:
    try:
        user_id = await supabase.auth().get_user(token)
        return user_id.get("user_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_user_from_id(user_id: str) -> Optional[dict]:
    try:
        user = await supabase.from_("users").select("*").eq("id", user_id).execute()
        return user.data[0] if user.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))