import logging
from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, Request, HTTPException

from app.schemas.auth import TokenData
from app.api.dependencies.core import DBSessionDep
from app.api.dependencies.auth import validate_signup, validate_login, validate_is_authenticated
from app.schemas.auth import Signup, Token, TokenInfo
from app.crud.user import create_user, get_user_by_email
from app.crud.auth import create_auth_token
from app.models.user import User
from app.constants import REFRESH_TOKEN_TYPE
from app.services.auth import create_access_token, create_refresh_token, get_token_payload, validate_token_type

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    summary="Signup",
)
async def signup(
        request: Request,
        db_session: DBSessionDep,
        signup: Signup = Depends(validate_signup),
):
    logging.debug(f"Signup request received with username: {signup.username}, email: {signup.email}")
    user = await create_user(db_session, signup)

    await create_auth_token(db_session, user)

    refresh_token = create_refresh_token(user)
    access_token = create_access_token(user)

    TokenInfo(access_token=access_token, refresh_token=refresh_token)

    request.session["refresh_token"] = refresh_token
    request.session["access_token"] = access_token
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/login",
    summary="Login"
)
async def login(
        request: Request,
        user: User = Depends(validate_login),
):
    refresh_token = create_refresh_token(user)
    access_token = create_access_token(user)

    request.session["refresh_token"] = refresh_token
    request.session["access_token"] = access_token
    return TokenInfo(access_token=access_token)


@router.post(
    "/refresh"
)
async def auth_refresh_token(
        request: Request,
        db_session: DBSessionDep,
):
    try:
        payload = get_token_payload(token=request.session["refresh_token"])

        validate_token_type(payload, REFRESH_TOKEN_TYPE)

        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        if not TokenData(email=email):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = await get_user_by_email(db_session, email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(user)
    request.session["access_token"] = access_token

    return access_token


@router.get(
    "/logout",
    dependencies=[Depends(validate_is_authenticated)],
)
async def logout(request: Request):
    access_token = request.session.get("access_token")
    print(f"{access_token}")
    del request.session["access_token"]
    del request.session["refresh_token"]
    return "Logout successful"
