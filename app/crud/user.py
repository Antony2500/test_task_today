import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import timedelta

from app.models import User as DBModelUser
from app.schemas.auth import Signup
from app.schemas.user import UpdateProfile, ResetPasswordArgs, DeleteUser
from app.utils.auth import hash_password, utc_now, is_protected_username, verify_password
from app.services.auth import new_token


logging.basicConfig(level=logging.DEBUG)


async def get_all_users(db_session: AsyncSession) -> List[DBModelUser]:

    stmt = select(DBModelUser)
    result = await db_session.execute(stmt)
    users = result.scalars().all()

    return users


async def get_user(db_session: AsyncSession, user_id: int):
    user = (await db_session.execute(select(DBModelUser).where(DBModelUser.id == user_id))).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_username(db_session: AsyncSession, username: str) -> DBModelUser | None:
    stmt = select(DBModelUser).options(
        selectinload(DBModelUser.teams)).filter(
            func.lower(DBModelUser.username) == username.lower()
        )
    result = await db_session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(db_session: AsyncSession, email: str):
    stmt = select(DBModelUser).options(
        selectinload(DBModelUser.teams)).filter(
            func.lower(DBModelUser.email) == email.lower()
        )
    result = await db_session.execute(stmt)
    return result.scalar_one_or_none()


async def get_admin_user_by_email(db_session: AsyncSession, email: str):
    stmt = select(DBModelUser).options(
        selectinload(DBModelUser.teams)).filter(
            func.lower(DBModelUser.email) == email.lower(),
            DBModelUser.role == "admin"
        )
    result = await db_session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db_session: AsyncSession, signup: Signup) -> DBModelUser:
    password_hash = hash_password(signup.password)
    activation_token = new_token()
    now = utc_now()

    user = DBModelUser(
        username=signup.username,
        surname=signup.surname,
        email=signup.email,
        hashed_password=password_hash,
        created=now,
    )

    db_session.add(user)
    await db_session.commit()

    return user


async def update_user_profile(db_session: AsyncSession, current_user: DBModelUser, profile_update: UpdateProfile):
    if profile_update.username:
        if is_protected_username(profile_update.username):
            logging.debug(f"Invalid username detected: {profile_update.username}")
            raise HTTPException(status_code=400, detail="Invalid username")

        if await get_user_by_username(db_session, profile_update.username):
            logging.debug(f"Username already exists: {profile_update.username}")
            raise HTTPException(status_code=400, detail="Username already exists")

        current_user.username = profile_update.username

    if profile_update.email:
        if await get_user_by_email(db_session, profile_update.email):
            logging.debug(f"Email already    exists: {profile_update.email}")
            raise HTTPException(status_code=400, detail="Email already exists")

        current_user.email = profile_update.email

    await db_session.commit()

    return current_user


async def create_password_token(db_session: AsyncSession, user: DBModelUser):
    user.password_reset_expire = utc_now() + timedelta(hours=1)
    user.password_reset_token = new_token()

    db_session.add(user)
    await db_session.commit()

    return user


async def create_new_password(db_session: AsyncSession, user: DBModelUser, reset_password_args: ResetPasswordArgs):
    if verify_password(hash_password(reset_password_args.old_password), user.hashed_password):
        user.hashed_password = hash_password(reset_password_args.password)
        user.password_reset_expire = None
        user.password_reset_token = None

        db_session.add(user)
        await db_session.commit()
    else:
        raise HTTPException(status_code=400, detail="Not correct the old password")



async def delete_user(db_session: AsyncSession, user: DBModelUser) -> bool:
    if user:
        await db_session.delete(user)
        await db_session.commit()
        return True
    else:
        return False


async def delete_user_by_username(db_session: AsyncSession, username: DeleteUser) -> bool:
    stmt = select(DBModelUser).filter(func.lower(DBModelUser.username) == username.username.lower())
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db_session.delete(user)
    await db_session.commit()
    return True
