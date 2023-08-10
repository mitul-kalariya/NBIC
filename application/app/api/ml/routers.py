"""
    ROUTER FILE
"""
from fastapi import APIRouter

from app.api.ml.endpoints import nbic_data_upload

api_router = APIRouter()
api_router.include_router(nbic_data_upload.router, tags=["NBIC-Data-Upload"])
