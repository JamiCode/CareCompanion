import datetime as _dt
import pydantic as _pydantic
from typing import Optional


class _UserBase(_pydantic.BaseModel):
    email:str
    first_name:str
    last_name:str

class UserCreate(_UserBase):
    hashed_password:str

    class Config:
        from_attributes  = True

class User(_UserBase):
    id: int

    class Config:
        from_attributes = True

# Pydantic model for creating a conversation
class ConversationCreate(_pydantic.BaseModel):
    title: str

class MessagePayload(_pydantic.BaseModel):
    text_content: str
    

class MessageSchema(_pydantic.BaseModel):
    id: int
    text_content: str 
    is_bot_message: bool

    class Config:
        orm_mode = True
    def __getitem__(self, item):
        return getattr(self, item, None)
