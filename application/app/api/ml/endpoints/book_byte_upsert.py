from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from langchain.vectorstores import VectorStore
from fastapi import HTTPException
from app.api.dependencies import get_vector_db
from app.schemas.nbic_schema import BookUpsertSchema
from app.parsers.nbic_json import json_parser

router = APIRouter(prefix="/book-bytes")


@router.post("/upsert", status_code=status.HTTP_201_CREATED)
async def upsert_data(
    book_data: BookUpsertSchema,
    vector_db: VectorStore = Depends(get_vector_db),
):
    """
    UPLOAD and UPDATE data api
    """
    start_time = datetime.now()
    documents, parsed_ids = json_parser(book_data.data)
    try:
        vector_db.upsert_document_with_index(documents, parsed_ids)
        return JSONResponse(
            {
                "ok": True,
                "ids": ", ".join(parsed_ids),
                "message": "vector data Upserted successfully",
                "ttl": str(datetime.now() - start_time),
            },
            status_code=status.HTTP_201_CREATED,
        )
    except HTTPException as e:
        return JSONResponse(
            {
                "ok": False,
                "ids": ", ".join(parsed_ids),
                "error": "HTTPException",
                "message": e.detail,
                "ttl": str(datetime.now() - start_time),
            },
            status_code=e.status_code,
        )
    except Exception as e:
        return JSONResponse(
            {
                "ok": False,
                "ids": ", ".join(parsed_ids),
                "error": "Internal Exception",
                "message": str(e),
                "ttl": str(datetime.now() - start_time),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
