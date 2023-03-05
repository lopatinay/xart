from pydantic import BaseModel

from service_api.models.voting import VotingStatuses


class VotingPayload(BaseModel):
    product_id: int
    snapshot_id: int
    decision: bool


class Product(BaseModel):
    id: int
    path: str

    class Config:
        orm_mode = True


class AllVotingResponse(BaseModel):
    id: int
    status: VotingStatuses
    product: Product
    snapshot: Product

    class Config:
        orm_mode = True


class VotingResponse(BaseModel):
    id: int
    status: VotingStatuses
    product: Product
    snapshot: Product
    count: int

    class Config:
        orm_mode = True


class VotingNextResponse(BaseModel):
    id: int
    status: VotingStatuses
    product: Product
    snapshot: Product
    count: int

    class Config:
        orm_mode = True
