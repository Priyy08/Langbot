from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
    created_at: datetime.datetime
    last_login: datetime.datetime

class TokenData(BaseModel):
    user_id: str