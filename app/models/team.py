from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from datetime import datetime

from .base import Base


class Team(Base):
    __tablename__ = "service_teams"

    name: Mapped[str] = mapped_column(String(64), unique=True)
    created: Mapped[datetime]

    users: Mapped[list["User"]] = relationship(
        secondary="user_team_association",
        back_populates="teams"
    )
