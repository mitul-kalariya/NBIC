from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from langchain.vectorstores import VectorStore
from fastapi import HTTPException
from app.api.dependencies import get_vector_db
from app.schemas.nbic_schema import BookDataSchema
from app.parsers.nbic_json import json_parser


from app.exception.base_exception import (
    vector_index_not_created,
)

router = APIRouter()


@router.post("/upload-book-vector", status_code=status.HTTP_201_CREATED)
async def upload_data(
    book_data: BookDataSchema,
    vector_db: VectorStore = Depends(get_vector_db),
    vectordb_name="nbic_pinecone",
):
    """
    Target Json Payload format
    { "id": 0,
    "title": "Friday",
    "author_name": "Robert Glaze",
    "description": "string",
    "category": "7 Books You Should Have Read By Now",
    "tagName": "Career" }
    """
    book_id, docs, metadata = json_parser(book_data)
    try:
        vector_db.insert_document_with_index(book_id, docs, meta=metadata)
        return JSONResponse(
            {
                "message": "vector data inserted successfully",
            },
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        raise vector_index_not_created
