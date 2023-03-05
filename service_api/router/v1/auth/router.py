from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from service_api.domain.auth.authentication import authenticate_uc, create_access_token_uc
from service_api.router.v1.auth import schema
from service_api.services.database import db_conn


auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/auth/token", response_model=schema.AuthenticateResponse, tags=["Auth"])
def authenticate(payload: schema.UserAuthPayload, db: Session = Depends(db_conn)):
    user = authenticate_uc(db, email=payload.email, password=payload.password)
    if user is not None:
        return create_access_token_uc(user)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Wrong credentials"
    )


@auth_router.post("/auth/token/docs", include_in_schema=False)
def authenticate(
    payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_conn)
):
    user = authenticate_uc(db, email=payload.username, password=payload.password)
    if user is not None:
        return create_access_token_uc(user)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Wrong credentials"
    )
