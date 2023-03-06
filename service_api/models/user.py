import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PasswordType, EmailType, ChoiceType

from service_api.models import BaseModel


class UserRoles(str, enum.Enum):
    QA = "QA"
    ADMIN = "ADMIN"


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(EmailType, unique=True)
    password: Mapped[str] = mapped_column(PasswordType(
        schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]
    ))

    votes: Mapped["VotingModel"] = relationship(back_populates="author")

    role: Mapped[str] = mapped_column(ChoiceType(UserRoles), default=UserRoles.QA)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
