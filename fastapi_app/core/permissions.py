from fastapi import HTTPException, status
from fastapi_app.models.auth_model import User

"""Permission helpers for role-based access control."""


def require_super_admin(user: User) -> None:
    if user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin privileges required"
        )

