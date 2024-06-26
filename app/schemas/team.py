from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from . import NameArgs, UsernameArgs
from datetime import datetime


class Team(NameArgs):
    created: datetime


class GetTeam(NameArgs):
    pass


class TeamCreate(BaseModel):
    name: str = Field(..., max_length=64)
    usernames: List[str]


class UserResponse(BaseModel):
    id: UUID4
    username: str
    surname: Optional[str] = None


class TeamResponse(BaseModel):
    id: UUID4
    name: str
    created: datetime
    users: List[UserResponse]


class TeamUpdate(NameArgs):
    new_name: Optional[str] = Field(None, pattern="^[A-Za-z][A-Za-z0-9_]{4,63}$", examples=["Crew"])
    usernames: Optional[List[str]]


class AddUserToTheTeam(NameArgs):
    pass


class AddUserToTeamByUsername(NameArgs):
    username: str


class RemoveUserFromTheTeam(NameArgs):
    pass


class RemoveCurrentUserFromTheTeam(UsernameArgs, NameArgs):
    pass


class RemoveTeam(NameArgs):
    pass
