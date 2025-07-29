from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class Message(BaseModel):
    id: Optional[str] = None
    conversation_id: str
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = datetime.utcnow()

class ChatMessage(BaseModel):
    conversation_id: str
    message: str