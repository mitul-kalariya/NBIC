"""
    NBIC OpenAI integration Schema
"""
from typing import Union,Optional
from pydantic import BaseModel

class BookDataSchema(BaseModel):
    """
    Book data upload schema
    """
    id : int
    title : str
    author_name : str
    description : str
    category : str
    tagName : str
