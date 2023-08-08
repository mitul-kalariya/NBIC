"""
    BASE EXCEPTION FILE
"""
from fastapi import HTTPException, status

user_not_found = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User Does Not Exist! Please Register First.",
    headers={"WWW-Authenticate": "Bearer"},
)

user_already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists.",
    headers={"WWW-Authenticate": "Bearer"},
)

incorrect_keyword = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Search keyword can't be more than two words!",
    headers={"WWW-Authenticate": "Bearer"},
)


email_already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with this email already exists!",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_password = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid password!",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials!",
    headers={"WWW-Authenticate": "Bearer"},
)

email_not_sent = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Email not sent",
    headers={"WWW-Authenticate": "Bearer"},
)

file_extension_not_supported = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="this file extension is not supported currently",
)

url_type_not_supported = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="this url type is not supported currently",
)

vector_index_not_created = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="unable to create vector index",
)

invalid_jwt_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="provided token is invalid"
)

expired_jwt_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="provided token has expired"
)
