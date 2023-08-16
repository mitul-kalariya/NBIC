"""
    DEPENDENCIES FILE FOR ROUTES
"""
from typing import Generator, Optional, Annotated
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from langchain.vectorstores import VectorStore
from app import models, schemas
from app.crud import user, conversation
from app.core import security
from app.core.configuration import settings
from app.db.session import SessionLocal
from app.exception.base_exception import (
    invalid_credentials,
    expired_jwt_token,
    invalid_jwt_token,
    user_not_found,
)

from vectorstore.vector_db_mappings import VECTOR_DB_MAPPING

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/user/login")


# defaults to pinecone but you can use different vector db for different request
def get_vector_db(vectordb_name: str = "pinecone") -> Optional[VectorStore]:
    """
    Get the vector database object based on the specified database name.

    Args:
        vectordb_name (str, optional): The name of the vector database to retrieve.
            Default is 'pinecone'.

    Returns:
        VectorStore: An instance of the vector database object corresponding to the specified database name.

    Raises:
        HTTPException: If the specified database name is not supported or if there is an internal server error.

    Note:
        This function relies on the global dictionary VECTOR_DB_MAPPING to map database names to vector database objects.
        If the provided vectordb_name is not found in the mapping, a ValueError is raised.
    """
    try:
        vector_db = VECTOR_DB_MAPPING.get(vectordb_name)
        if vector_db:
            return vector_db
        else:
            raise ValueError(f"Unsupported database: {vectordb_name}")

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported database: {vectordb_name}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="connection to vector database not established",
        )


def authorize_user_id(user_id: str = Header(...)):
    #TODO: User Id authentication code with postgres cli
    if user_id != "approved":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")

def get_db() -> Generator:
    """
    Returns a new database session
    """
    try:
        db_session = SessionLocal()
        yield db_session
    finally:
        db_session.close()


def get_user_crud(db: Session = Depends(get_db)):
    return user.UserCrud(db)


def get_conversation_crud(db: Session = Depends(get_db)):
    return conversation.ConversationCrud(db)


def get_current_user(
    token: str = Depends(reusable_oauth2),
    user_crud: user.UserCrud = Depends(get_user_crud),
):
    try:
        payload = security.decode_jwt_payload(token)
        token_data = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise expired_jwt_token

    except jwt.InvalidTokenError:
        raise invalid_jwt_token

    except (jwt.JWTError, ValidationError) as excep:
        raise invalid_credentials from excep

    user = user_crud.get_user_by_username(token_data)

    if not user:
        raise user_not_found

    return user


# def get_current_user(
#     db_session: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> models.User:
#     """
#     Return the current user
#     """
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )

#         token_data = schemas.TokenPayload(**payload)
#     except (jwt.JWTError, ValidationError) as excep:
#         raise invalid_credentials from excep

#     user = get_by_email(db_session, email=token_data.sub)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
    user_crud: user.UserCrud = Depends(get_user_crud),
) -> models.User:
    """
    Return the current active user
    """
    if not user_crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
    user_crud: user.UserCrud = Depends(get_user_crud),
) -> models.User:
    """
    Return the current active superuser
    """
    if not user_crud.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges!"
        )
    return current_user
