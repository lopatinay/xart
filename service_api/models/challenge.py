from sqlalchemy.orm import Mapped, mapped_column

from service_api.models import BaseModel


class ChallengeModel(BaseModel):
    __tablename__ = "challenge"

    id: Mapped[int] = mapped_column(primary_key=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    items_pre_challenge: Mapped[int] = mapped_column(default=100)
    solved_items: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f"<Challenge(id={self.id}, is_active={self.is_active})>"
