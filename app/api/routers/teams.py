import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.user import CurrentUserDep

from app.api.dependencies.core import DBSessionDep
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate, AddUserToTheTeam, UserResponse, \
    AddUserToTeamByUsername, RemoveTeam, RemoveUserFromTheTeam, GetTeam, RemoveCurrentUserFromTheTeam
from app.crud.team import create_team, update_team, add_user_to_the_team, remove_user_from_the_team, \
    add_user_to_team_by_username, delete_team, get_team, get_all_teams, remove_current_user_from_the_team

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/create",
    response_model=TeamResponse
)
async def create_team_endpoint(
        team: TeamCreate,
        current_user: CurrentUserDep,
        db_session: DBSessionDep
):
    new_team = await create_team(db_session, team)
    print("GOOOOD")
    return new_team


@router.put(
    "/update",
    response_model=TeamResponse
)
async def update_team_endpoint(
    team_update_data: TeamUpdate,
    current_user: CurrentUserDep,
    db_session: DBSessionDep
):
    logger.info(f"Received update request for team: {team_update_data.dict()}")
    updated_team = await update_team(db_session, team_update_data)
    logger.info(f"Successfully updated team: {updated_team}")
    return updated_team


@router.patch(
    "/add_user",
    response_model=TeamResponse
)
async def add_user_in_the_team(
        current_user: CurrentUserDep,
        info_for_update: AddUserToTheTeam,
        db_session: DBSessionDep
):
    team = await add_user_to_the_team(db_session, current_user, info_for_update)
    return TeamResponse(
        id=str(team.id),
        name=team.name,
        created=team.created,
        users=[UserResponse(id=str(user.id), username=user.username) for user in team.users]
    )


@router.post(
    "/add_user_to_team",
    response_model=TeamResponse
)
async def add_user_to_team_by_username_endpoint(
        current_user: CurrentUserDep,
        info: AddUserToTeamByUsername,
        db_session: DBSessionDep
):
    team = await add_user_to_team_by_username(db_session, info)
    return TeamResponse(
        id=str(team.id),
        name=team.name,
        created=team.created,
        users=[UserResponse(id=str(user.id), username=user.username) for user in team.users]
    )


@router.patch(
    "/remove_me",
    response_model=TeamResponse
)
async def remove_user_from_the_team_endpoint(
        current_user: CurrentUserDep,
        info_for_update: RemoveUserFromTheTeam,
        db_session: DBSessionDep
):
    team = await remove_user_from_the_team(db_session, current_user, info_for_update)
    return TeamResponse(
        id=str(team.id),
        name=team.name,
        created=team.created,
        users=[UserResponse(id=str(user.id), username=user.username) for user in team.users]
    )


@router.patch(
    "/remove_user",
    response_model=TeamResponse
)
async def remove_user_from_the_team_endpoint(
        current_user: CurrentUserDep,
        info_for_update: RemoveCurrentUserFromTheTeam,
        db_session: DBSessionDep
):
    team = await remove_current_user_from_the_team(db_session, info_for_update)
    return TeamResponse(
        id=str(team.id),
        name=team.name,
        created=team.created,
        users=[UserResponse(id=str(user.id), username=user.username) for user in team.users]
    )


@router.delete(
    "/delete_team}",
    status_code=204
)
async def delete_team_endpoint(
        current_user: CurrentUserDep,
        team_name: RemoveTeam,
        db_session: DBSessionDep
):
    await delete_team(db_session, team_name)


@router.get(
    "/team/{team_name}",
    response_model=TeamResponse
)
async def get_team_endpoint(
        current_user: CurrentUserDep,
        team_name: str,
        db_session: DBSessionDep
):
    team = await get_team(db_session, team_name)
    logger.info(f"Team details: ID={team.id}, Name={team.name}, Created={team.created}")
    for user in team.users:
        logger.info(f"User in team: ID={user.id}, Username={user.username}")
    return TeamResponse(
        id=str(team.id),
        name=team.name,
        created=team.created,
        users=[UserResponse(id=str(user.id), username=user.username) for user in team.users]
    )


@router.get(
    "/teams",
    response_model=List[TeamResponse]
)
async def get_all_teams_endpoint(
        current_user: CurrentUserDep,
        db_session: DBSessionDep
):
    teams = await get_all_teams(db_session)
    return [TeamResponse(
        id=str(team.id),
        name=team.name,
        created=team.created,
        users=[UserResponse(id=str(user.id), username=user.username) for user in team.users]
    ) for team in teams]
