from sqlalchemy import Column, String

from apps.backend.app.core.db import Base


class SupplierModel(Base):
    __tablename__ = "procurement_suppliers"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    tax_id = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
