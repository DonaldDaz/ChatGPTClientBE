from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Role = Literal["system", "user", "assistant"]

class ChatMessage(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    model: str = Field(default="gpt-4o-mini")
    messages: List[ChatMessage]
    temperature: float = 0.2
    max_output_tokens: Optional[int] = None
    stream: bool = False

class ChatResponse(BaseModel):
    content: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
