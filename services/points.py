from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.point import Point
from models.user import User

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status



class PointService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    
    async def award_point(self, user_id: int, point_data):
        # 1. Fetch the recipient AND their points in one move (eager loading)
        # This prevents the "MissingGreenlet" explosion when we append later.
        result = await self.db.execute(
            select(User)
            .where(User.id == point_data.recipient_id)
            .options(selectinload(User.points)) 
        )
        recipient = result.scalars().first()
        
        if not recipient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # 2. Create the point object
        new_point = Point(
            issuer_id=user_id,
            recipient_id=point_data.recipient_id,
            value=point_data.value,
            reason=point_data.reason
        )

        # 3. Use the relationship magic
        # Since we used selectinload, this is now safe and synchronous in memory
        recipient.points.append(new_point)

        # 4. Flush/Commit everything at once
        # This keeps the transaction atomic. If the append fails, nothing hits the DB.
        await self.db.commit()
        
        # 5. Refresh if you need the generated IDs/timestamps back
        await self.db.refresh(new_point)

        return new_point
    
    
    async def get_all_points(self) -> list[Point]:
        result = await self.db.execute(
            select(Point)
            .options(selectinload(Point.issued_by))
            .order_by(Point.created_at.desc()),
        )
        
        all_posts = result.scalars().all()
        return all_posts
    
    
    
    async def get_user_points(self, user_id) -> Point:
        result = await self.db.execute(
            select(Point)
            .where(Point.recipient_id == user_id)
            .options(selectinload(Point.issued_by))
            .options(selectinload(Point.recipient)),
        )
        
        
        user_points = result.scalars().all()
        return user_points