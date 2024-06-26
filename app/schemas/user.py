from pydantic import BaseModel, ConfigDict, EmailStr, Field, constr, field_validator
from typing import List, Optional
from datetime import datetime

from . import UsernameArgs, PasswordArgs, EmailArgs
from .team import Team


class User(PasswordArgs, EmailArgs):
    pass


class AuthorizedUser(UsernameArgs, EmailArgs):
    created: datetime
    teams: List[Team]


class UpdateProfile(UsernameArgs, EmailArgs):
    username: Optional[constr(pattern="^[A-Za-z][A-Za-z0-9_]{4,63}$")] = Field(
        None,
        examples=["New Username or None"]
    )

    email: Optional[EmailStr] = Field(None, examples=["New Email or None"])

    @field_validator("email")
    @classmethod
    def check_email(cls, value: EmailStr) -> EmailStr:
        if value is None:
            return value
        if "+" in value:
            raise ValueError("Email contains unacceptable characters")

        return value


class ResetPasswordArgs(PasswordArgs):
    old_password: str = Field(min_length=8, max_length=128, examples=["old_password"])


class UserDeleteResponse(BaseModel):
    success: bool


class DeleteUser(UsernameArgs):
    pass
