from email import message
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    temprature: float = 0.7

class ChatResponse(BaseModel):
    message: str
    reply: str