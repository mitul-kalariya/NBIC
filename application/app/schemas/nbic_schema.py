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
    author: str
    description: str
    categories: str
    tags: str


class BookUpsertSchema(BaseModel):
    """
    Book data upload and update schema
    """

    books: List[BookByteSchema]


class BookDeleteSchema(BaseModel):
    """
    Book delete schema
    """

    book_ids: List[Union[str, int]]


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
