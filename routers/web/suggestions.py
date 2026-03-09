from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi.templating import Jinja2Templates

import models
from auth import CurrentUser
from database import get_db
from schemas import PostCreate, PostResponse, PostUpdate

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/suggestions", include_in_schema=False, name="suggestions")
async def suggestions(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    # result = await db.execute(
    #     select(models.Post)
    #     .options(selectinload(models.Post.author))
    #     .order_by(models.Post.date_posted.desc()),
    # )
    # posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "suggestions.html",
    )