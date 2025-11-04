from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import timedelta

from ..core.database import get_db
from ..core.config import settings
from ..core.security import create_access_token, verify_token
from ..models.user import User
from ..schemas.token import Token
from ..schemas.user import User as UserSchema

router = APIRouter()
security = HTTPBearer()


@router.post("/google", response_model=Token)
async def google_auth(credential: dict, db: Session = Depends(get_db)):
    """
    Google OAuth 로그인
    프론트엔드에서 받은 Google ID 토큰을 검증하고 JWT 토큰을 발급합니다.
    """
    try:
        # Google ID 토큰 검증
        idinfo = id_token.verify_oauth2_token(
            credential["credential"],
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        # 이메일 도메인 확인 (회사 워크스페이스만 허용)
        email = idinfo.get("email")
        if not email.endswith(f"@{settings.ALLOWED_DOMAIN}"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Only @{settings.ALLOWED_DOMAIN} emails are allowed"
            )

        google_id = idinfo.get("sub")
        name = idinfo.get("name")
        picture = idinfo.get("picture")

        # 사용자 조회 또는 생성
        user = db.query(User).filter(User.google_id == google_id).first()

        if not user:
            user = User(
                email=email,
                google_id=google_id,
                name=name,
                picture=picture
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # 기존 사용자 정보 업데이트
            user.name = name
            user.picture = picture
            db.commit()

        # JWT 토큰 생성
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "google_id": user.google_id, "user_id": user.id},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    현재 로그인한 사용자 정보를 반환합니다.
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    현재 로그인한 사용자의 정보를 반환합니다.
    """
    return current_user
