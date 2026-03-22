from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


############### USER SCHEM  ##############################
class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    image_file: str | None
    image_path: str
    total_points: int 


class UserPrivate(UserPublic):
    email: EmailStr


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)


class Token(BaseModel):
    access_token: str
    token_type: str



############### POST SCHEM  ##############################

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date_posted: datetime
    author: UserPublic


############### POINT SCHEM  ##############################

class PointBase(BaseModel):
    value: int = Field(default=1)
    reason: str = Field(min_length=1, default="Well behaved")
    
    
class PointCreate(PointBase):
    recipient_id: int


class PointResponse(PointBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    issued_by: UserPublic
    recipient: UserPublic
    created_at: datetime
    