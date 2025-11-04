from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from ..core.database import get_db
from ..models.user import User
from ..models.post import Post
from ..schemas.user import User as UserSchema
from ..middleware.admin import get_admin_user
from pydantic import BaseModel

router = APIRouter()


class UserUpdate(BaseModel):
    is_admin: bool = None
    is_active: bool = None


class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_posts: int
    total_views: int
    recent_users_count: int  # 최근 7일 내 가입
    recent_posts_count: int  # 최근 7일 내 작성


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    대시보드 통계 데이터를 반환합니다.
    """
    # 총 사용자 수
    total_users = db.query(func.count(User.id)).scalar()

    # 활성 사용자 수
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()

    # 총 게시글 수
    total_posts = db.query(func.count(Post.id)).scalar()

    # 총 조회수
    total_views = db.query(func.sum(Post.view_count)).scalar() or 0

    # 최근 7일 내 가입한 사용자 수
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_users = db.query(func.count(User.id)).filter(
        User.created_at >= seven_days_ago
    ).scalar()

    # 최근 7일 내 작성된 게시글 수
    recent_posts = db.query(func.count(Post.id)).filter(
        Post.created_at >= seven_days_ago
    ).scalar()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_posts": total_posts,
        "total_views": total_views,
        "recent_users_count": recent_users,
        "recent_posts_count": recent_posts
    }


@router.get("/users", response_model=List[UserSchema])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    모든 사용자 목록을 반환합니다. (관리자 전용)
    """
    users = db.query(User).order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    return users


@router.patch("/users/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    사용자 정보를 수정합니다. (관리자 전용)
    관리자 권한 부여/해제, 계정 활성화/비활성화
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 자기 자신의 관리자 권한은 해제할 수 없음
    if user.id == admin_user.id and user_update.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove your own admin privileges"
        )

    # 업데이트
    if user_update.is_admin is not None:
        user.is_admin = user_update.is_admin
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    db.commit()
    db.refresh(user)
    return user


@router.get("/posts")
async def get_all_posts_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    모든 게시글 목록을 반환합니다. (관리자 전용)
    """
    posts = (
        db.query(Post, User)
        .join(User, Post.author_id == User.id)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []
    for post, author in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "author_name": author.name,
            "author_email": author.email,
            "is_pinned": post.is_pinned,
            "is_notice": post.is_notice,
            "view_count": post.view_count,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        })

    return result


@router.delete("/posts/{post_id}")
async def delete_post_admin(
    post_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    게시글을 삭제합니다. (관리자 전용)
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
