from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.post import Post
from auth import CurrentUser
from database import get_db
from schemas import PostCreate, PostResponse, PostUpdate
from dependencies import post_service

router = APIRouter()


@router.get("", response_model=list[PostResponse])
async def get_posts(
    service: Annotated[AsyncSession, Depends(post_service)]
    ):
    
    posts = await service.get_all_posts()
    return posts


@router.post("",
             response_model=PostResponse,
             status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    current_user: CurrentUser,
    service: Annotated[AsyncSession, Depends(post_service)]
    ):
    
    new_post = await service.create_post(user_id=current_user.id, post=post)
    return new_post


@router.get("/{post_id}", 
            response_model=PostResponse)
async def get_post(post_id: int, 
                   service: Annotated[AsyncSession, Depends(post_service)]):
    post = await service.get_single_post(post_id=post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post_full(
    post_id: int,
    post_data: PostCreate,
    current_user: CurrentUser,
    service: Annotated[AsyncSession, Depends(post_service)],
):
    
    edited_post = await service.edit_post(post_id=post_id, post_data=post_data, user_id=current_user.id)
    
    return edited_post


@router.patch("/{post_id}", response_model=PostResponse)
async def update_post_partial(
    post_id: int,
    post_data: PostUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(post_service)],
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post, attribute_names=["author"])
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post",
        )

    await db.delete(post)
    await db.commit()
