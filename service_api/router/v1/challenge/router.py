from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from service_api.domain.auth.authentication import get_current_user
from service_api.domain.challenge.use_case import ChallengeUseCases
from service_api.models import UserModel
from service_api.repository.challenge import ChallengeRepo
from service_api.router.v1.challenge import schema
from service_api.services.database import db_conn


challenge_router = APIRouter(tags=["Challenges"])


@challenge_router.post(
    "/challenges",
    response_model=schema.ChallengeResponse
)
def create_challenge(
    db: Session = Depends(db_conn),
    current_user: UserModel = Depends(get_current_user)
):
    repo = ChallengeRepo(db)
    use_case = ChallengeUseCases(repo)
    return use_case.create(current_user)


@challenge_router.get(
    "/challenges",
    response_model=schema.ChallengeResponse
)
def create_challenge(
    db: Session = Depends(db_conn),
    current_user: UserModel = Depends(get_current_user)
):
    repo = ChallengeRepo(db)
    use_case = ChallengeUseCases(repo)
    return use_case.get_active_challenge(current_user)
