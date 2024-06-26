from . import BaseModel, datetime_pd, UsernameArgs, PasswordArgs, EmailArgs
from pydantic import Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None


class TokenData(BaseModel):
    email: str


class TokenResponse(BaseModel):
    expiration: datetime_pd = Field(examples=[1686088809])
    created: datetime_pd = Field(examples=[1686088809])
    secret: str = Field(
        examples=["CQE-CTXVFCYoUpxz_6VKrHhzHaUZv68XvxV-3AvQbnA"]
    )


class Signup(UsernameArgs, PasswordArgs, EmailArgs):
    surname: str = Field(pattern="^[A-Za-z][A-Za-z0-9_]{4,63}$", examples=["Surname"])


class LoginArgs(PasswordArgs, EmailArgs):
    pass

