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
    GROUP_REVIEW = "GROUP_REVIEW"
    GROUP_FINISHED = "GROUP_FINISHED"


class VotingModel(BaseModel):
    __tablename__ = "voting"

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[str] = mapped_column(
        ChoiceType(VotingStatuses), default=VotingStatuses.IN_PROGRESS
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    author: Mapped[UserModel] = relationship(backref="votes")

    snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshot.id", ondelete="CASCADE"))
    snapshot: Mapped[SnapshotModel] = relationship(backref="votes")

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    product: Mapped[ProductModel] = relationship(backref="votes")

    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenge.id", ondelete="CASCADE"))
    challenge: Mapped[ChallengeModel] = relationship(backref="votes")

    def __repr__(self) -> str:
        return f"<Voting(id={self.id}, author_id={self.author_id}, status={self.status.value})>"


class MajorityReviewersModel(BaseModel):
    __tablename__ = "majority_reviewers"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped[UserModel] = relationship(backref="majority_reviewers")

    voting_id: Mapped[int] = mapped_column(ForeignKey("voting.id", ondelete="CASCADE"))
    voting: Mapped[VotingModel] = relationship(backref="majority_reviewers")
