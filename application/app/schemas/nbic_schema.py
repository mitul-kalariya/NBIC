"""
    NBIC OpenAI integration Schema
"""
from typing import Union, List, Optional
from pydantic import BaseModel


class BookByteSchema(BaseModel):
    """
    Book Information
    """

    id: int
    title: str
    author_name: str
    description: str
    category: str
    tagName: str


class BookUpsertSchema(BaseModel):
    """
    Book data upload and update schema
    """

    data: List[BookByteSchema]


class BookDeleteSchema(BaseModel):
    """
    Book delete schema
    """

    ids: List[Union[str, int]]


class BookFunctionalSchema(BaseModel):
    """Book schema to use with internal logic"""

    book_id: Union[str, int]
    text_content: str
    metadata: dict


class ChatSchema(BaseModel):
    """Message Format Schema for Chat with Book-Bytes"""

    user_id: str
    question: str
    book_byte_id: Optional[Union[str, int]]
    book_byte_title: Optional[str]
