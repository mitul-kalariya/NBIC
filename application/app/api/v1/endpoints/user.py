"""
    ADMIN ENDPOINTS
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schema import (
    UserBase,
    UserCreate,
    JwtTokenSchema,
    AccessTokenSchema,
    RefreshTokenSchema,
)

from app.crud.user import UserCrud
from app.api.dependencies import get_user_crud, get_current_user
from app.core.security import (
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_password,
    decode_jwt_payload,
)
from app.exception.base_exception import (
    user_already_exists,
    invalid_jwt_token,
    user_not_found,
)


router = APIRouter()


@router.post("/signup", response_model=UserBase)
def create_user(user: UserCreate, user_crud: UserCrud = Depends(get_user_crud)):
    if user_crud.get_user_by_username(user.username):
        raise user_already_exists

    # hash the password before storing it in database
    user.password = get_password_hash(user.password)
    user = user_crud.create_user(user)
    return UserBase(username=user.username,email=user.email)


@router.post("/login")
def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_crud: UserCrud = Depends(get_user_crud),
):
    username = form_data.username
    password = form_data.password

    user = user_crud.get_user_by_username(username)

    # if the user does not exists or password is wrong then raise exception
    if user is None or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return JwtTokenSchema(
        token_type="bearer",
        access_token=create_access_token(username),
        refresh_token=create_refresh_token(username),
    )


@router.post("/refresh_token", response_model=AccessTokenSchema)
def refresh_access_token(
    refresh_token: RefreshTokenSchema, user_crud: UserCrud = Depends(get_user_crud)
):
    decoded_refresh_token = decode_jwt_payload(refresh_token)
    username = decoded_refresh_token.get("sub")
    if not username:
        raise invalid_jwt_token

    user = user_crud.get_user_by_username(username)
    if not user:
        raise user_not_found

    return AccessTokenSchema(
        token_type="bearer", access_token=create_access_token(user.username)
    )


@router.get("/me/", response_model=UserBase)
def read_users_me(current_user=Depends(get_current_user)):
    return UserBase(**current_user.__dict__)
