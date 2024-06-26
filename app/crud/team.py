import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import  selectinload
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from typing import List
from uuid import UUID
from app.models.user import User
from app.models.team import Team
from app.models import User as DBModelUser
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate, AddUserToTheTeam, RemoveUserFromTheTeam, \
    AddUserToTeamByUsername, RemoveTeam, GetTeam, RemoveCurrentUserFromTheTeam
from app.utils.auth import utc_now
from app.crud.user import get_user_by_username


async def create_team(db_session: AsyncSession, team_data: TeamCreate) -> TeamResponse:
    stmt_existing_team = select(Team).where(Team.name == team_data.name)
    existing_team = await db_session.execute(stmt_existing_team)
    if existing_team.scalar():
        raise HTTPException(status_code=400, detail=f"Team with name '{team_data.name}' already exists")

    stmt = select(User).where(User.username.in_(team_data.usernames))
    result = await db_session.execute(stmt)
    users = result.scalars().all()

    if len(users) != len(team_data.usernames):
        existing_usernames = {user.username.lower() for user in users}
        missing_usernames = [username for username in team_data.usernames if username.lower() not in existing_usernames]
        raise HTTPException(status_code=404, detail=f"Users not found: {', '.join(missing_usernames)}")

    new_team = Team(name=team_data.name, created=utc_now())

    db_session.add(new_team)

    new_team.users.extend(users)

    await db_session.commit()

    team_response = TeamResponse(
        id=new_team.id,
        name=new_team.name,
        created=new_team.created,
        users=[{'id': user.id, 'username': user.username} for user in users]
    )
    return team_response


async def update_team(db_session: AsyncSession, team_data: TeamUpdate) -> TeamResponse:
    stmt = select(Team).where(Team.name == team_data.name).options(
        selectinload(Team.users)
    )
    result = await db_session.execute(stmt)
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if team_data.new_name:
        team.name = team_data.new_name

    if team_data.usernames:

        stmt = select(User).where(User.username.in_(team_data.usernames))
        result = await db_session.execute(stmt)
        users = result.scalars().all()

        if len(users) != len(team_data.usernames):
            existing_usernames = {user.username.lower() for user in users}
            missing_usernames = [username for username in team_data.usernames if
                                 username.lower() not in existing_usernames]

            raise HTTPException(status_code=404, detail=f"Users not found: {', '.join(missing_usernames)}")

        team.users = users

    await db_session.merge(team)
    await db_session.commit()

    team_response = TeamResponse(
        id=team.id,
        name=team.name,
        created=team.created,
        users=[{'id': user.id, 'username': user.username} for user in team.users]
    )
    return team_response


async def add_user_to_the_team(db_session: AsyncSession, user: DBModelUser, info_for_update: AddUserToTheTeam) -> Team:
    stmt = select(Team).where(Team.name == info_for_update.name).options(
        selectinload(Team.users)
    )
    result = await db_session.execute(stmt)
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    list_of_users = team.users
    if user not in list_of_users:
        list_of_users.append(user)
        await db_session.commit()
    else:
        raise HTTPException(status_code=400, detail="User already in team")

    return team


async def add_user_to_team_by_username(db_session: AsyncSession, info: AddUserToTeamByUsername) -> Team:
    stmt = select(Team).where(Team.name == info.name).options(selectinload(Team.users))
    result = await db_session.execute(stmt)
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    stmt = select(User).where(User.username == info.username)
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user not in team.users:
        team.users.append(user)
        await db_session.commit()
    else:
        raise HTTPException(status_code=400, detail="User already in team")

    return team


async def remove_user_from_the_team(db_session: AsyncSession, user: DBModelUser, info_for_update: RemoveUserFromTheTeam) -> Team:
    stmt = select(Team).where(Team.name == info_for_update.name).options(
        selectinload(Team.users)
    )
    result = await db_session.execute(stmt)
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    list_of_users = team.users
    if user in list_of_users:
        list_of_users.remove(user)
        await db_session.commit()
    else:
        raise HTTPException(status_code=400, detail="User not in team")

    return team


async def remove_current_user_from_the_team(db_session: AsyncSession, info_for_update: RemoveCurrentUserFromTheTeam) -> Team:
    stmt = select(Team).where(Team.name == info_for_update.name).options(
        selectinload(Team.users)
    )
    result = await db_session.execute(stmt)
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    user = await get_user_by_username(db_session, info_for_update.username)

    list_of_users = team.users
    if user in list_of_users:
        list_of_users.remove(user)
        await db_session.commit()
    else:
        raise HTTPException(status_code=400, detail="User not in team")

    return team


async def delete_team(db_session: AsyncSession, team_name: RemoveTeam) -> None:
    stmt = select(Team).where(Team.name == team_name.name)
    result = await db_session.execute(stmt)
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    await db_session.delete(team)
    await db_session.commit()


async def get_team(db_session: AsyncSession, team_name: str) -> Team:
    stmt = select(Team).where(Team.name == team_name).options(selectinload(Team.users))
    result = await db_session.execute(stmt)
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return team


async def get_all_teams(db_session: AsyncSession) -> List[Team]:
    stmt = select(Team).options(selectinload(Team.users))
    result = await db_session.execute(stmt)
    teams = result.scalars().all()

    return teams
