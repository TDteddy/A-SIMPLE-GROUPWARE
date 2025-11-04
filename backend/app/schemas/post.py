from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    is_pinned: Optional[bool] = False
    is_notice: Optional[bool] = False


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_pinned: Optional[bool] = None
    is_notice: Optional[bool] = None


class Post(PostBase):
    id: int
    author_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostWithAuthor(Post):
    author_name: str
    author_email: str
    author_picture: Optional[str] = None
