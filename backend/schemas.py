import datetime as _dt
import pydantic as _pydantic


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

class MessagePayload(BaseModel):
    conversation_id: int
    text_content: str
    author_id: int