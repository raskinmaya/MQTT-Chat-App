from pydantic import BaseModel

class RegisterMessage(BaseModel):
    username: str
    address: str

class ChatMessage(BaseModel):
    from_user: str
    to_user: str
    message: str
    timestamp: str

class LookupMessage(BaseModel):
    requester: str
    target: str
