import re
from urllib.parse import unquote
from bs4 import BeautifulSoup
from langchain.schema import Document
from app.schemas.nbic_schema import BookDataSchema
from app.utils.document_utils import count_tokens

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
    book_data.description = re.sub(r"\n", "", clean_description(book_data.description))
    meta_fields = ["title", "author_name", "category", "tagName"]
    base_data = (
        " title | "
        + book_data.title
        + ", author_name | "
        + book_data.author_name
        + ", category | "
        + book_data.description
        + ", tagName | "
        + book_data.tagName
        + ", description | "
        + book_data.description
    )
    book_dict = dict(book_data)
    meta = {x: book_dict.get(x) for x in meta_fields}
    return book_id, base_data, meta


def clean_description(document: str):
    """clean the html encoded string into pure text"""
    decoded_string = unquote(document)
    return BeautifulSoup(decoded_string, "lxml").text
