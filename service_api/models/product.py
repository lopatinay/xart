import os

from sqlalchemy.orm import Mapped, mapped_column

from service_api.configs import RuntimeConfig
from service_api.models import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)

    file_name: Mapped[str] = mapped_column(unique=True)

    @property
    def path(self):
        return os.path.join(RuntimeConfig.products_dir, self.file_name)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, image={self.file_name})>"
