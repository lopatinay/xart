import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType

from service_api.models import BaseModel
from service_api.models.challenge import ChallengeModel
from service_api.models.product import ProductModel
from service_api.models.snapshot import SnapshotModel
from service_api.models.user import UserModel


class VotingStatuses(str, enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    MATCH = "MATCH"
    UNMATCH = "UNMATCH"


class VotingModel(BaseModel):
    __tablename__ = "voting"

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[str] = mapped_column(ChoiceType(VotingStatuses), nullable=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    author: Mapped[UserModel] = relationship(uselist=False, back_populates="votes")

    snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshot.id", ondelete="CASCADE"))
    snapshot: Mapped[SnapshotModel] = relationship(back_populates="votes", lazy="joined")

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"), nullable=True)
    product: Mapped[ProductModel] = relationship(backref="votes", lazy="joined")

    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenge.id", ondelete="CASCADE"), nullable=True)
    challenge: Mapped[ChallengeModel] = relationship(backref="votes")

    def __repr__(self) -> str:
        return f"<Voting(id={self.id}, author_id={self.author_id}, status={self.status.value})>"
