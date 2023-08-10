from langchain.schema import Document
from app.schemas.nbic_schema import BookDataSchema

"""
Loading Json loader from langchain and adding
data of book information (id, title, author_name, description, category, tagname)
using BookDataSchema of nbic_schema

OP: Document[object] converted data of provided book
"""

def json_parser(book_data: BookDataSchema) -> None:
    """
    Loads a Json object and converts it into document object of langchain

    Args:
        book_data (BookDataSchema): A schema object with book data information
    """
    book_id = book_data.id
    meta_fields = ['title','author_name','category','tagName']
    base_data = (' title | ' + book_data.title +
        ', author_name | '+ book_data.author_name +
        ', category | '+ book_data.description +
        ', tagName | ' + book_data.tagName +
        ', description | ' + book_data.description)
    book_data = dict(book_data)
    meta = {x: book_data.get(x) for x in meta_fields}
    return book_id,base_data,meta