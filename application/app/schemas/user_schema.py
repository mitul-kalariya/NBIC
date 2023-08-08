"""
    USER SCHEMA FILE
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4


class UserBase(BaseModel):
    """
    User Base Schema
    """

    username: str
    email: Optional[EmailStr] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    """
    User Create Schema
    """

    password: str

    class Config:
        """
        ORM Config
        """

        orm_mode = True


# Properties to receive via API on update
class UserUpdate(UserBase):
    """
    User Update Schema
    """

    id: UUID4
    password: Optional[str] = None

    class Config:
        """
        ORM Config
        """

        orm_mode = True


class AccessTokenSchema(BaseModel):
    access_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class JwtTokenSchema(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
