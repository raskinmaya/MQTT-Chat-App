import time
from typing import Optional

from pydantic import BaseModel

class ServerMessage(BaseModel):
    timestamp: Optional[int] = time.time()

class LookupResponse(ServerMessage):
    target: str
    address: str

class ChatMessage(ServerMessage):
    message: str
    content_base64: Optional[str] = ""

class ServerAck(ServerMessage):
    topic: str
    username: str
    address: Optional[str] = ""
    message: Optional[str] = ""

class ServerError(ServerAck):
    reason: Optional[str] = "An unexpected error occurred"