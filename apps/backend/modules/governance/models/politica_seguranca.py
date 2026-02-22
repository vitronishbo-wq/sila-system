"""Security Policy Model for SILA Governance Module"""

from sqlalchemy import JSON, Column, DateTime, Integer, String

from config.database import Base


class PoliticaSeguranca(Base):
    """Model for tracking security policies and compliance."""

    __tablename__ = "governance_politicas_seguranca"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    policy_name = Column(String(200), nullable=False)
    policy_version = Column(String(50))
    description = Column(String(2000))
    scope = Column(String(500))
    status = Column(String(50), default="draft")  # draft, active, deprecated
    effective_date = Column(DateTime)
    review_date = Column(DateTime)
    compliance_requirements = Column(JSON)  # JSON array of requirements
    responsible_party = Column(String(200))

    def __repr__(self):
        return f"<PoliticaSeguranca(id={self.id}, policy_name={self.policy_name}, status={self.status})>"

