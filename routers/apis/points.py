from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.post import Post
from auth import CurrentUser
from database import get_db
from schemas import PointResponse, PointCreate
from dependencies import point_service

router = APIRouter()

@router.get("", response_model=list[PointResponse])
async def get_points(
    service: Annotated[AsyncSession, Depends(point_service)]
    ):
    
    all_points = await service.get_all_points()
    return all_points


@router.get("/user_points/{user_id}", response_model=list[PointResponse])
async def get_user_points(
    user_id: int,
    service: Annotated[AsyncSession, Depends(point_service)]
    ):
    
    user_points = await service.get_user_points(user_id=user_id)
    return user_points


@router.post("/award_point", response_model=PointResponse)
async def award_point(
    current_user: CurrentUser,
    point_data: PointCreate,
    service: Annotated[AsyncSession, Depends(point_service)]
    ):
    
    result = await service.award_point(user_id=current_user.id,
                                        point_data=point_data)
    return result