from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from langchain.vectorstores import VectorStore
from fastapi import HTTPException
from app.api.dependencies import get_vector_db
from app.schemas.nbic_schema import BookDeleteSchema
from app.parsers.nbic_json import json_parser

router = APIRouter(prefix="//books-embeddings")


@router.post("/_delete", status_code=status.HTTP_200_OK)
async def delete_data(
    ids: BookDeleteSchema,
    vector_db: VectorStore = Depends(get_vector_db),
):
    """
    Delete data api
    """
    start_time = datetime.now()
    delete_book_ids = ids.book_ids
    try:
        vector_db.delete_document_with_index(delete_book_ids)
        return JSONResponse(
            {
                "ok": True,
                "ttl": str((datetime.now() - start_time).isoformat()),
            },
            status_code=status.HTTP_200_OK,
        )
    except HTTPException as e:
        return JSONResponse(
            {
                "ok": False,
                "error": "HTTPException",
                "message": e.detail,
            },
            status_code=e.status_code,
        )
    except Exception as e:
        return JSONResponse(
            {
                "ok": False,
                "error": "Internal Exception",
                "message": str(e),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
