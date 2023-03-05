from datetime import datetime, timedelta

import arrow
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from service_api.configs import RuntimeConfig
from service_api.models import UserModel
from service_api.services.database import db_conn


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token/docs", scheme_name="JWT"
)


def authenticate_uc(db, email: str, password: str):
    user = db.query(UserModel).filter_by(email=email).scalar()
    if user and user.password == password:
        return user


def create_access_token_uc(
    user: UserModel, expires_delta: timedelta | None = None
):
    to_encode = {"id": user.id, "email": user.email, "role": user.role.value}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, RuntimeConfig.jwt_secret_key, algorithm=RuntimeConfig.jwt_algorithm
    )
    response = {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "expired_id": (arrow.get(expire) - arrow.utcnow()).seconds
    }
    return response


def get_current_user(
    db: Session = Depends(db_conn), token: str = Depends(oauth2_scheme)
) -> UserModel:
    try:
        payload = jwt.decode(
            token,
            RuntimeConfig.jwt_secret_key,
            algorithms=[RuntimeConfig.jwt_algorithm],
        )
        email: str = payload.get("email")
        if email is None:
            raise Exception("credentials_exception")
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(UserModel).filter_by(email=email).scalar()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
