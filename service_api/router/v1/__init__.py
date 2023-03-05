from fastapi import APIRouter

from service_api.router.v1.auth.router import auth_router
from service_api.router.v1.challenge.router import challenge_router
from service_api.router.v1.voting.router import voting_router

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(auth_router)
api_v1.include_router(challenge_router)
api_v1.include_router(voting_router)


__all__ = (
    "api_v1"
)
