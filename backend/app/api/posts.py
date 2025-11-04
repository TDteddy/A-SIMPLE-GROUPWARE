from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from ..core.database import get_db
from ..models.user import User
from ..models.post import Post
from ..schemas.post import Post as PostSchema, PostCreate, PostUpdate, PostWithAuthor
from .auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[PostWithAuthor])
async def get_posts(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    게시글 목록을 반환합니다.
    공지사항과 고정 게시글이 먼저 표시됩니다.
    """
    posts = (
        db.query(Post, User)
        .join(User, Post.author_id == User.id)
        .order_by(desc(Post.is_notice), desc(Post.is_pinned), desc(Post.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []
    for post, author in posts:
        result.append(
            PostWithAuthor(
                id=post.id,
                title=post.title,
                content=post.content,
                author_id=post.author_id,
                is_pinned=post.is_pinned,
                is_notice=post.is_notice,
                view_count=post.view_count,
                created_at=post.created_at,
                updated_at=post.updated_at,
                author_name=author.name,
                author_email=author.email,
                author_picture=author.picture,
            )
        )

    return result


@router.get("/{post_id}", response_model=PostWithAuthor)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    특정 게시글을 반환합니다.
    조회수가 증가합니다.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # 조회수 증가
    post.view_count += 1
    db.commit()

    author = db.query(User).filter(User.id == post.author_id).first()

    return PostWithAuthor(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        is_pinned=post.is_pinned,
        is_notice=post.is_notice,
        view_count=post.view_count,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author_name=author.name,
        author_email=author.email,
        author_picture=author.picture,
    )


@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    새 게시글을 작성합니다.
    """
    db_post = Post(
        title=post.title,
        content=post.content,
        author_id=current_user.id,
        is_pinned=post.is_pinned,
        is_notice=post.is_notice,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.put("/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    게시글을 수정합니다.
    작성자 본인 또는 관리자만 수정할 수 있습니다.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # 권한 확인 (작성자 본인 또는 관리자)
    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # 업데이트
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    게시글을 삭제합니다.
    작성자 본인 또는 관리자만 삭제할 수 있습니다.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # 권한 확인 (작성자 본인 또는 관리자)
    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    db.delete(post)
    db.commit()
    return None
