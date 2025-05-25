import time
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel

class ServerMessage(BaseModel):
    request_id: Optional[str] = str(uuid4())
    timestamp: Optional[float] = time.time()

class LookupResponse(ServerMessage):
    target: str
    address: str

class ChatMessage(ServerMessage):
    message: str
    content_base64: Optional[str] = ""
    filename: Optional[str] = ""

class ServerAck(ServerMessage):
    topic: str
    username: str
    address: Optional[str] = ""
    message: Optional[str] = ""

class ServerError(ServerAck):
    reason: Optional[str] = "An unexpected error occurred"