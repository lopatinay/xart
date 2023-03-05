from pydantic import BaseModel


class ChallengeResponse(BaseModel):
    id: int
    is_active: bool
    items_pre_challenge: int
    solved_items: int

    class Config:
        orm_mode = True
