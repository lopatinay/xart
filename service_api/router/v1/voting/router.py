from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from service_api.domain.auth.authentication import get_current_user
from service_api.domain.voting.use_case import VotingUseCases, VotingPermissionDeniedError
from service_api.models import UserModel
from service_api.repository.challenge import ChallengeRepo
from service_api.repository.voting import VotingRepo, ExtraVotingAlreadyExist
from service_api.router.v1.voting import schema
from service_api.router.v1.voting.schema import VotingPayload
from service_api.services.database import db_conn


voting_router = APIRouter(tags=["Challenges"])


@voting_router.post(
    "/voting",
    response_model=schema.VotingResponse | None
)
def create_challenge(
    payload: VotingPayload,
    db: Session = Depends(db_conn),
    current_user: UserModel = Depends(get_current_user)
):
    voting_repo = VotingRepo(db)
    challenge_repo = ChallengeRepo(db)
    use_case = VotingUseCases(voting_repo, challenge_repo)
    return use_case.vote(current_user, payload.dict())


@voting_router.get(
    "/voting",
    response_model=List[schema.AllVotingResponse]
)
def create_challenge(
    db: Session = Depends(db_conn),
    current_user: UserModel = Depends(get_current_user)
):
    repo = VotingRepo(db)
    use_case = VotingUseCases(repo)
    return use_case.all(current_user)


@voting_router.get(
    "/voting/next",
    response_model=schema.VotingNextResponse
)
def create_challenge(
    db: Session = Depends(db_conn),
    current_user: UserModel = Depends(get_current_user)
):
    voting_repo = VotingRepo(db)
    challenge_repo = ChallengeRepo(db)
    use_case = VotingUseCases(voting_repo, challenge_repo)
    next_voting = use_case.get(current_user)
    if next_voting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active challenge not found",
        )
    return next_voting


@voting_router.post(
    "/voting/{voting_id}/to-group-review",
    response_model=List[schema.ExtraVotingResponse]
)
def to_group_review(
    voting_id: int,
    db: Session = Depends(db_conn),
    current_user: UserModel = Depends(get_current_user)
):
    repo = VotingRepo(db)
    use_case = VotingUseCases(repo)
    try:
        return use_case.to_group_review(current_user, voting_id)
    except VotingPermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ExtraVotingAlreadyExist as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=str(e),
        )
