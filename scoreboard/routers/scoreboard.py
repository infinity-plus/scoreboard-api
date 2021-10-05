from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from scoreboard.models import Score, Team
from scoreboard.routers.login import User, get_current_active_user

Score_Pydantic = pydantic_model_creator(Score, name="Score")
Team_Pydantic = pydantic_model_creator(Team, name="Team")

router = APIRouter(
    responses={
        401: {
            "detail": "Incorrect username or password",
        },
        400: {
            "detail": "Inactive user",
        },
    },
)


@router.get(
    "/scoreBoard",
    response_model=List[Team_Pydantic],
)
async def get_score():
    return await Team_Pydantic.from_queryset(Team.all())


@router.get("/score/{team_name}", response_model=Team_Pydantic)
async def get_team_score(team_name: str):
    return await Team_Pydantic.from_queryset_single(Team.get(name=team_name))


@router.put(
    "/score",
    response_model=Score_Pydantic,
    responses={
        status.HTTP_404_NOT_FOUND: {"detail": "Team not found"},
        status.HTTP_401_UNAUTHORIZED: {
            "detail": "Incorrect username or password",
        },
        status.HTTP_400_BAD_REQUEST: {
            "detail": "Inactive user",
        },
    },
)
async def post_score(
    name: str,
    score: int,
    current_user: User = Depends(get_current_active_user),
):
    team_obj = await Team.get_or_none(name=name)
    if team_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team {name} not found",
        )
    a = await Score.create(team=team_obj, score=score)
    await a.save()
    return Score_Pydantic.from_orm(a)


@router.post("/team", response_model=Team_Pydantic)
async def create_team(
    team: str,
    current_user: User = Depends(get_current_active_user),
):
    created_team = await Team.get_or_create(name=team)
    await created_team[0].save()
    return await Team_Pydantic.from_tortoise_orm(created_team[0])
