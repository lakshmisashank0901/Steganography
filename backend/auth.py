
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import supabase
from models import User

# Configuration for Supabase Auth
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not SUPABASE_JWT_SECRET:
        raise HTTPException(status_code=500, detail="SUPABASE_JWT_SECRET is not configured.")
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
        
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise credentials_exception
        email = user_response.user.email
    except Exception as e:
        print(f"Supabase auth error: {e}")
        raise credentials_exception
    
    response = supabase.table("users").select("*").eq("email", email).execute()
    if not response.data or len(response.data) == 0:
        raise credentials_exception
    user_data = response.data[0]
    if user_data.get("is_admin") is None:
        user_data["is_admin"] = False
    return User(**user_data)

async def get_current_user_optional(token: str = Depends(oauth2_scheme)):
    if not token or not SUPABASE_JWT_SECRET:
        return None
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            return None
        email = user_response.user.email
    except Exception:
        return None
    
    response = supabase.table("users").select("*").eq("email", email).execute()
    if not response.data or len(response.data) == 0:
        return None
    user_data = response.data[0]
    if user_data.get("is_admin") is None:
        user_data["is_admin"] = False
    return User(**user_data)
