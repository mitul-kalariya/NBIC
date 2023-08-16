from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from dateutil import parser
from langchain.vectorstores import VectorStore
from fastapi import HTTPException
from app.api.dependencies import get_vector_db
from app.schemas.nbic_schema import BookUpsertSchema
from app.parsers.nbic_json import json_parser

router = APIRouter()


@router.post("/books-embeddings", status_code=status.HTTP_201_CREATED)
async def upsert_data(
    book_data: BookUpsertSchema,
    vector_db: VectorStore = Depends(get_vector_db),
):
    """
    UPLOAD and UPDATE data api
    """
    start_time = datetime.now()
    documents, parsed_ids = json_parser(book_data.books)
    try:
        vector_db.upsert_document_with_index(documents, parsed_ids)
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
