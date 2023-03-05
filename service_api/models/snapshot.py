from sqlalchemy.orm import Mapped, mapped_column

from service_api.models import BaseModel


class SnapshotModel(BaseModel):
    __tablename__ = "snapshot"

    id: Mapped[int] = mapped_column(primary_key=True)

    image_path: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"<Snapshot(id={self.id}, image={self.image_path})>"
