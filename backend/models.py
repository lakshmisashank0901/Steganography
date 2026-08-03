from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hashed_password: Optional[str] = None
    profile_image: Optional[str] = None
    is_admin: bool = False

class EncodedImage(BaseModel):
    id: int
    filename: str
    filepath: str
    num_secrets: int = 0
    created_at: Optional[datetime] = None
    owner_id: int

class Message(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    filename: str
    filepath: str
    timestamp: Optional[datetime] = None
    is_read: bool = False

