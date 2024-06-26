from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum
from datetime import datetime

from .base import Base


class User(Base):
    __tablename__ = "service_users"

    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    surname: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    created: Mapped[datetime]
    banned: Mapped[bool] = mapped_column(default=False)

    role: Mapped[str] = mapped_column(Enum("user", "admin", name="user_roles"), default="user")

    teams: Mapped[list["Team"]] = relationship(
        secondary="user_team_association",
        back_populates="users"
    )

    password_reset_token: Mapped[str] = mapped_column(String(64), nullable=True)
    password_reset_expire: Mapped[datetime] = mapped_column(nullable=True)

    auth_tokens: Mapped[list["AuthToken"]] = relationship(
        back_populates="user"
    )
