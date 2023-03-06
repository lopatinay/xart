from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
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
    challenge = use_case.create(current_user)

    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You already have an active challenge",
        )

    return challenge


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
    challenge = use_case.get_active_challenge(current_user)

    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No active challenge",
        )

    return challenge


@challenge_router.get(
    "/challenges/{challenge_id}/results",
    response_model=List[schema.ChallengeResultsResponse]
)
def create_challenge(
    challenge_id: int,
    db: Session = Depends(db_conn),
):
    repo = ChallengeRepo(db)
    use_case = ChallengeUseCases(repo)
    challenge = use_case.get_results(challenge_id)

    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No active challenge",
        )

    return challenge
