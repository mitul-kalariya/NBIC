from typing import List, Optional

from pydantic import BaseModel, UUID4, root_validator
# from slugify import slugify

from app.schemas.user_schema import UserBase


class MessageBase(BaseModel):
    conversation_id: UUID4
    message: str
    is_agent: bool

class MessageResponse(MessageBase):
    id:UUID4


class MessageCreate(MessageBase):
    original_prompt:str



class ConversationBase(BaseModel):
    slug: Optional[str]
    title: str
    tags: List[str]

    @root_validator(pre=True)
    def generate_slug(cls, values):
        if values.get("title"):
            values["slug"] = (values.get("title"))

        return values

    class Config:
        orm_mode = True


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(ConversationBase):
    slug: Optional[str] = None
    title: Optional[str] = None
    tags: Optional[List[str]] = None


class Conversation(ConversationBase):
    user_id: UUID4
    id: UUID4
    messages: List[MessageBase]
    user: UserBase

    class Config:
        orm_mode = True
