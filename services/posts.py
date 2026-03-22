from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.post import Post
from models.user import User

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status


class PostService:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_posts(self) -> list[Post]:
        result = await self.db.execute(
            select(Post)
            .options(selectinload(Post.author))
            .order_by(Post.date_posted.desc()),
        )
        
        all_posts = result.scalars().all()
        return all_posts
    
    
    async def get_single_post(self, post_id) -> Post:
        result = await self.db.execute(
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.id == post_id),
        )
        
        post = result.scalars().first()
        return post
    
    
    
    async def get_user_posts(self, user_id: int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        result = await self.db.execute(
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.user_id == user_id)
            .order_by(Post.date_posted.desc()),
        )
        
        user_posts = result.scalars().all()
        return user_posts
    
    
    
    async def create_post(self, user_id: int, post):
        new_post = Post(
            title=post.title,
            content=post.content,
            user_id=user_id,
            )
        
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post, attribute_names=["author"])
        return new_post
    
    
    async def edit_post_full(self, post_id, post_data, user_id):
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        post = result.scalars().first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post",
            )

        post.title = post_data.title
        post.content = post_data.content

        await self.db.commit()
        await self.db.refresh(post, attribute_names=["author"])
        return post
            
            
