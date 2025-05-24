import time
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

class ClientMessage(BaseModel):
    request_id: Optional[str] = str(uuid4())
    timestamp: Optional[float] = time.time()

class RegisterMessage(ClientMessage):
    username: str = Field(...)
    address: str = Field(...)

class DisconnectMessage(ClientMessage):
    username: str = Field(...)
    address: str = Field(...)

class SendTextMessage(ClientMessage):
    from_user: str = Field(...)
    to_user: str = Field(...)
    message: str = Field(...)

class SendFileMessage(ClientMessage):
    from_user: str = Field(...)
    to_user: str = Field(...)
    filename: str = Field(...)
    content_base64: str = Field(...)
    message: Optional[str] = ""

class LookupMessage(ClientMessage):
    requester: str = Field(...)
    target: str = Field(...)