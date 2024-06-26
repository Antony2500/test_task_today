from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

user_team_association = Table(
    "user_team_association",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("service_users.id"), primary_key=True),
    Column("team_id", UUID(as_uuid=True), ForeignKey("service_teams.id"), primary_key=True)
)
