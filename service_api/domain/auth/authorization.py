from fastapi import Security, HTTPException
from starlette import status

from service_api.domain.auth.authentication import get_current_user
from service_api.models import UserAccountModel
from service_api.models.user_account import UserRoles


def super_admin_authorization(user: UserAccountModel = Security(get_current_user)):
    if user.role != UserRoles.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Forbidden",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def active_user_authorization(user: UserAccountModel = Security(get_current_user)):
    return user
