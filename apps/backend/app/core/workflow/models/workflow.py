from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class Workflow(Base):
    __tablename__ = 'workflows'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    module_slug: Mapped[str | None] = mapped_column(String(100), nullable=True)
    definition: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(50), default='active')