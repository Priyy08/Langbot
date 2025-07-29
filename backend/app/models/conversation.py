from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConversationCreate(BaseModel):
    title: str

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    is_pinned: Optional[bool] = None

class ConversationInDB(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    last_message: Optional[str] = None
    last_message_timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True # For compatibility with ORM-like objects