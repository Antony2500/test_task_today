from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from jwt import PyJWTError

from app import models
from app.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.api.dependencies.core import DBSessionDep
from app.crud.user import get_user_by_email, get_admin_user_by_email
from app.schemas.auth import TokenData
from app.services.auth import get_access_token, get_email_from_token_payload
from app.errors import credentials_exception


async def get_current_user(token: Annotated[str, Depends(get_access_token)], db_session: DBSessionDep) -> models.User:
    try:
        email = get_email_from_token_payload(token)
        token_data = TokenData(email=email)
    except PyJWTError as e:
        raise credentials_exception

    user = await get_user_by_email(db_session, token_data.email)
    if user is None:
        raise credentials_exception

    return user


CurrentUserDep = Annotated[models.User, Depends(get_current_user)]


async def get_admin_user(token: Annotated[str, Depends(get_access_token)], db_session: DBSessionDep) -> models.User:
    try:
        email = get_email_from_token_payload(token)
        token_data = TokenData(email=email)
    except PyJWTError as e:
        raise credentials_exception

    user = await get_admin_user_by_email(db_session, token_data.email)
    if user is None:
        raise credentials_exception

    return user


CurrentAdminDep = Annotated[models.User, Depends(get_admin_user)]
