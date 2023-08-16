import re
from urllib.parse import unquote
from bs4 import BeautifulSoup
from langchain.schema import Document
from app.schemas.nbic_schema import BookByteSchema, BookFunctionalSchema
from app.utils.document_utils import count_tokens

"""
Loading Json loader from langchain and adding
data of book information (id, title, author_name, description, category, tagname)
using BookDataSchema of nbic_schema

OP: Document[object] converted data of provided book
"""


def json_parser(parsed_data: BookByteSchema) -> None:
    """
    Loads a Json object and converts it into document object of langchain

    Args:
        book_data (BookDataSchema): A schema object with book data information
    """
    meta_fields = ["title", "author", "categories", "tags"]
    parsed_ids = []
    parsed_tuples = []
    for book_data in parsed_data:
        book_id = str(book_data.id)
        parsed_ids.append(book_id)
        book_data.description = clean_description(book_data.description)
        base_data = generate_base_data(book_data)
        book_dict = dict(book_data)
        meta = {x: book_dict.get(x) for x in meta_fields}
        parsed_tuples.append(
            BookFunctionalSchema(book_id=book_id, text_content=base_data, metadata=meta)
        )

    return parsed_tuples, parsed_ids


def clean_description(document: str):
    """clean the html encoded string into pure text"""
    decoded_string = unquote(document)
    clean_data = re.sub(r"\n", "", BeautifulSoup(decoded_string, "lxml").text)
    return clean_data


def generate_base_data(book_data):
    """"""
    return (
        " title | "
        + book_data.title
        + ", author_name | "
        + book_data.author
        + ", category | "
        + book_data.categories
        + ", tagName | "
        + book_data.tags
        + ", description | "
        + book_data.description
    )
