"""
    ROUTER FILE
"""
from fastapi import APIRouter

from app.api.ml.endpoints import book_byte_delete, book_byte_upsert, chat

api_router = APIRouter()
api_router.include_router(book_byte_upsert.router, tags=["Book-Bytes-Upsert"])
api_router.include_router(book_byte_delete.router, tags=["Book-Bytes-Delete"])
api_router.include_router(chat.router, tags=["chat"])
