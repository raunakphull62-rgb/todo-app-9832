from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import SupabaseError
from jose import jwt
from datetime import datetime
from typing import List, Optional
from config import settings
from auth import verify_token

router = APIRouter()

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class Todo(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    completed: Optional[bool]
    due_date: Optional[datetime]
    user_id: int

@router.get("/todos", response_model=List[Todo])
async def get_todos(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = verify_token(token.credentials)
        user_id = payload["sub"]
        data = supabase.from_("todos").select("*").eq("user_id", user_id)
        todos = data.execute()
        return todos.data
    except SupabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = verify_token(token.credentials)
        user_id = payload["sub"]
        data = supabase.from_("todos").select("*").eq("id", todo_id).eq("user_id", user_id)
        todo = data.execute()
        if not todo.data:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo.data[0]
    except SupabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/todos", response_model=Todo)
async def create_todo(todo: Todo, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = verify_token(token.credentials)
        user_id = payload["sub"]
        todo.user_id = user_id
        data = supabase.from_("todos").insert([todo.dict()])
        new_todo = data.execute()
        return new_todo.data[0]
    except SupabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = verify_token(token.credentials)
        user_id = payload["sub"]
        data = supabase.from_("todos").update({"id": todo_id, "user_id": user_id}, todo.dict())
        updated_todo = data.execute()
        if not updated_todo.data:
            raise HTTPException(status_code=404, detail="Todo not found")
        return updated_todo.data[0]
    except SupabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = verify_token(token.credentials)
        user_id = payload["sub"]
        data = supabase.from_("todos").delete().eq("id", todo_id).eq("user_id", user_id)
        deleted_todo = data.execute()
        if not deleted_todo.data:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"message": "Todo deleted successfully"}
    except SupabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))