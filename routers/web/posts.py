from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi.templating import Jinja2Templates

from models.post import Post
from auth import CurrentUser
from database import get_db
from schemas import PostCreate, PostResponse, PostUpdate

from dependencies import post_service


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", include_in_schema=False, name="home")
@router.get("/posts", include_in_schema=False, name="posts")
async def home(
    request: Request, service: Annotated[AsyncSession, Depends(post_service)]
):

    posts = await service.get_all_posts()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"posts": posts, "title": "Home"},
    )


@router.get("/posts/{post_id}", include_in_schema=False)
async def post_page(
    request: Request,
    post_id: int,
    service: Annotated[AsyncSession, Depends(post_service)],
):

    post = await service.get_single_post(post_id=post_id)

    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            request=request,
            name="post.html",
            context={"post": post, "title": title},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



@router.get("/posts/user_posts/{user_id}", include_in_schema=False, name="user_posts")
async def user_posts_page(
    request: Request,
    user_id: int,
    service: Annotated[AsyncSession, Depends(post_service)],
):
    posts = await service.get_user_posts(user_id=user_id)
    if posts:
        user = posts[0].author
    
    
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )