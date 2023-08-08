"""
    ROUTER FILE
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    conference_search,
    user,
    test,
    document_search,
    file_upload,
    nbic_data_upload,
    url_upload,
    vectorstore_from_database,
    chat,
    conversation,
)

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(test.router, prefix="/test", tags=["Test"])
api_router.include_router(
    conference_search.router, prefix="/conference", tags=["conference"]
)
api_router.include_router(document_search.router, tags=["Document-search"])
api_router.include_router(file_upload.router, tags=["File-upload"])
api_router.include_router(nbic_data_upload.router, tags=["NBIC-Data-Upload"])
api_router.include_router(url_upload.router, tags=["Url-upload"])
api_router.include_router(
    vectorstore_from_database.router,
    tags=["Create vectorstore from database"],
)
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(conversation.router, tags=["conversation"])
