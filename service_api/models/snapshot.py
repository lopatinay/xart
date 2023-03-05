import os

from sqlalchemy.orm import Mapped, mapped_column, relationship

from service_api.configs import RuntimeConfig
from service_api.models import BaseModel


class SnapshotModel(BaseModel):
    __tablename__ = "snapshot"

    id: Mapped[int] = mapped_column(primary_key=True)

    file_name: Mapped[str] = mapped_column(unique=True)
    votes: Mapped["VotingModel"] = relationship(back_populates="snapshot")

    @property
    def path(self):
        return os.path.join(RuntimeConfig.products_dir, self.file_name)

    def __repr__(self) -> str:
        return f"<Snapshot(id={self.id}, image={self.file_name})>"
