from apps.backend.app.core.db import Base
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column


class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    module_slug: Mapped[str | None] = mapped_column(String(100), nullable=True)
    definition: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(50), default="active")
