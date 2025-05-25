import time
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class ServerMessage(BaseModel):
    request_id: Optional[str] = str(uuid4())
    timestamp: Optional[float] = time.time()

class LookupResponse(ServerMessage):
    target: str = Field(...)
    address: str = Field(...)

class ChatMessage(ServerMessage):
    message: str = Field(...)
    content_base64: Optional[str] = ""
    filename: Optional[str] = ""

class ServerAck(ServerMessage):
    topic: str = Field(...)
    username: str = Field(...)
    address: Optional[str] = ""
    message: Optional[str] = ""

class ServerError(ServerAck):
    reason: str = Field(...)