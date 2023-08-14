"""
    NBIC OpenAI integration Schema
"""
from typing import Union,Optional,List
from pydantic import BaseModel

class BookDataSchema(BaseModel):
    """
    Book data upload and update schema
    """
    id : int
    title : str
    author_name : str
    description : str
    category : str
    tagName : str

class DeleteBookSchema(BaseModel):
    """
    Book delete schema
    """
    ids : List[Union[str,int]]