from pydantic import BaseModel

from service_api.models.voting import VotingStatuses


class ChallengeResponse(BaseModel):
    id: int
    is_active: bool
    items_pre_challenge: int
    solved_items: int

    class Config:
        orm_mode = True


class ChallengeResultsResponse(BaseModel):
    majority: int
    snapshot_id: int
    product_id: int
    status: VotingStatuses
