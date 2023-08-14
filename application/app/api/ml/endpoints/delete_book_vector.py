from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from langchain.vectorstores import VectorStore
from fastapi import HTTPException
from app.api.dependencies import get_vector_db
from app.schemas.nbic_schema import DeleteBookSchema
from app.parsers.nbic_json import json_parser


from app.exception.base_exception import (
    vector_index_not_created,
)

router = APIRouter()


@router.post("/delete-book-vector", status_code=status.HTTP_200_OK)
async def delete_data(
    ids: DeleteBookSchema,
    vector_db: VectorStore = Depends(get_vector_db),
):
    """
    Target Json Payload format
    { "id": 0,}
    """
    delete_book_ids = ids.ids
    try:
        vector_db.delete_document_with_index(delete_book_ids)
        return JSONResponse(
            {
                "message": "vector data deleted successfully",
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise vector_index_not_created
