
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi.templating import Jinja2Templates

from models.user import User
from models.post import Post
from auth import CurrentUser
from database import get_db
from schemas import PostCreate, PostResponse, PostUpdate

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
async def user_posts_page(
    request: Request,
    user_id: int,
    service: Annotated[AsyncSession, Depends(get_db)],
):
    posts = await service.get_user_posts()
    
    
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )
