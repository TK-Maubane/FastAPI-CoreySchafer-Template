from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

        