from fastapi import HTTPException, status, Depends
from ..models.user import User
from ..api.auth import get_current_user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    관리자 권한을 확인합니다.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
