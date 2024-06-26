from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Annotated, List

from app.api.dependencies.auth import validate_is_authenticated, validate_password_reset
from app.api.dependencies.user import CurrentUserDep, CurrentAdminDep
from app.api.dependencies.core import DBSessionDep
from app.crud.user import update_user_profile, create_password_token, create_new_password, delete_user, \
    delete_user_by_username, get_all_users
from app.schemas.team import UserResponse
from app.schemas.user import User, AuthorizedUser, UpdateProfile, ResetPasswordArgs, UserDeleteResponse, DeleteUser

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get(
    "/",
    response_model=List[UserResponse]
)
async def get_all_users_endpoint(
        current_user: CurrentUserDep,
        db_session: DBSessionDep
):
    users = await get_all_users(db_session)
    return [UserResponse(
        id=str(user.id),
        username=user.username,
        surname=user.surname
    ) for user in users]


@router.get(
    "/me",
    response_model=AuthorizedUser
)
async def user_details(current_user: CurrentUserDep):
    return current_user


@router.patch(
    "/change/profile",
    response_model=AuthorizedUser
)
async def change_profile(
        profile_update: UpdateProfile,
        current_user: CurrentUserDep,
        db_session: DBSessionDep
):
    try:
        updated_user = await update_user_profile(db_session, current_user, profile_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return updated_user


@router.post(
    "/make/password_reset_token"
)
async def make_password_reset_token(
        current_user: CurrentUserDep,
        db_session: DBSessionDep
):
    user = await create_password_token(db_session, current_user)

    return "Create success new password token"


@router.post(
    "/reset_password",
    response_model=UserDeleteResponse
)
async def reset_password(
        reset_password_args: ResetPasswordArgs,
        db_session: DBSessionDep,
        current_user: User = Depends(validate_password_reset),
):
    user = await create_new_password(db_session, current_user, reset_password_args)

    return {"Success": True}


@router.delete(
    "/delete/me",
    response_model=UserDeleteResponse
)
async def delete_user_me(
        current_user: CurrentUserDep,
        db_session: DBSessionDep
):
    success = await delete_user(db_session, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Server problem")
    return {"success": True}


@router.get(
    "/admin",
    response_model=AuthorizedUser
)
async def user_details(current_admin: CurrentAdminDep):
    return current_admin


@router.delete(
    "/delete",
    response_model=UserDeleteResponse
)
async def delete_user_endpoint(
        username: DeleteUser,
        admin_user: CurrentAdminDep,
        db_session: DBSessionDep
):
    success = await delete_user_by_username(db_session, username)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True}
