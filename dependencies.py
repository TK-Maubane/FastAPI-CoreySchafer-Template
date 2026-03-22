from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from services.posts import PostService
from services.points import PointService
from services.users import UserService


def post_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PostService:
    return PostService(db)


def point_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PointService:
    return PointService(db)