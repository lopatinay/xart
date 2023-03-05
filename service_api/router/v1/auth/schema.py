from pydantic import BaseModel


class UserAuthPayload(BaseModel):
    email: str
    password: str


class AuthenticateResponse(BaseModel):
    access_token: str
    expired_id: int
    token_type: str
