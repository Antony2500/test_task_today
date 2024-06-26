from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.models import User as DBModelUser
from app.models import AuthToken
from app.services.auth import new_token
from app.utils.auth import utc_now


async def create_auth_token(db_session: AsyncSession, user: DBModelUser) -> AuthToken:
    now = utc_now()

    token = AuthToken(
        **{
            "expiration": now + timedelta(minutes=30),
            "secret": new_token(),
            "created": now,
            "user": user
        }
    )

    db_session.add(token)
    await db_session.commit()

    return token



