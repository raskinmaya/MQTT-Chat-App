import time
from typing import Optional

from pydantic import BaseModel

class ServerResponse(BaseModel):
    timestamp: Optional[int] = time.time()

class LookupResponse(ServerResponse):
    target: str
    address: str

class Message(ServerResponse):
    message: str
    content_base64: Optional[str] = ""

class ServerAck(ServerResponse):
    topic: str
    username: str
    address: Optional[str] = ""
    message: Optional[str] = ""

class ServerError(ServerAck):
    reason: Optional[str] = "An unexpected error occurred"