"""
    ROUTER FILE
"""
from fastapi import APIRouter

from app.api.ml.endpoints import (
    upload_book_vector,
    delete_book_vector,
)

api_router = APIRouter()
api_router.include_router(upload_book_vector.router, tags=["NBIC-Data-Upload"])
api_router.include_router(delete_book_vector.router, tags=["NBIC-Data-Delete"])
