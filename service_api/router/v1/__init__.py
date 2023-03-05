from fastapi import APIRouter

from service_api.router.v1.auth.router import auth_router

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(auth_router)


__all__ = (
    "api_v1"
)
