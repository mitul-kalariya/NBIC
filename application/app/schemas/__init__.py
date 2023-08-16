"""
    INIT FILE FOR SCHEMAS
"""

from .user_schema import (
    UserCreate,
    UserUpdate,
    UserBase,
)
from .response_schema import BaseResponse, FailureResponse
from .email_schema import EmailSchema
