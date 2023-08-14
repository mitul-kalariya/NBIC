from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from langchain.vectorstores import VectorStore
from fastapi import HTTPException
from app.api.dependencies import get_vector_db
from app.schemas.nbic_schema import BookPayloadSchema
from app.parsers.nbic_json import json_parser
from app.exception.base_exception import vector_db_upsert_issue

from app.exception.base_exception import (
    vector_index_not_created,
)

router = APIRouter()


@router.post("/upload-book-vector", status_code=status.HTTP_201_CREATED)
async def upload_data(
    book_data: BookPayloadSchema,
    vector_db: VectorStore = Depends(get_vector_db),
):
    """
    UPLOAD and UPDATE data api
    """
    start_time = datetime.now()
    documents, parsed_ids = json_parser(book_data.data)
    try:
        for document in documents:
            vector_db.upsert_document_with_index(
                document.book_id, document.text_content, meta=document.metadata
            )
        return JSONResponse(
            {
                "ok": True,
                "upserted_ids": str(parsed_ids),
                "message": "vector data inserted successfully",
                "ttl": str(datetime.now() - start_time),
            },
            status_code=status.HTTP_201_CREATED,
        )
    except HTTPException as e:
        raise JSONResponse(
            {
                "ok": False,
                "requested_ids": parsed_ids,
                "error": e,
                "message": e.detail,
                "ttl": datetime.now() - start_time,
            },
            status_code=e.status_code,
        )
