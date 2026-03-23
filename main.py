from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
import logging

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase_url = SUPABASE_URL
supabase_key = SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)

# Initialize FastAPI app
app = FastAPI()

# Initialize CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize JWT authentication
security = HTTPBearer()

async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        user = await supabase.from_("User").select("*").eq("username", username).execute()
        if not user.data:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        return user.data[0]
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )

# Include routes
from routes import User, Todo

app.include_router(User.router)
app.include_router(Todo.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)

# Error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )