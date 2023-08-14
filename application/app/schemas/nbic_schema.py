"""
    NBIC OpenAI integration Schema
"""
from typing import Union, Optional, List
from pydantic import BaseModel

class BookDataSchema(BaseModel):
    """
    Book Information
    """

    id: int
    title: str
    author_name: str
    description: str
    category: str
    tagName: str


class BookPayloadSchema(BaseModel):
    """
    Book data upload and update schema
    """
    data: List[BookDataSchema]


class DeleteBookSchema(BaseModel):
    """
    Book delete schema
    """

    ids: List[Union[str, int]]

class BookFunctionalSchema(BaseModel):
    """Book schema to use with internal logic"""
    book_id: Union[str,int]
    text_content : str
    metadata : dict
