"""Risk Management Model for SILA Governance Module"""

from sqlalchemy import JSON, Column, DateTime, Integer, String

from config.database import Base


class GestaoRisco(Base):
    """Model for tracking risk management activities."""

    __tablename__ = "governance_gestao_riscos"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    risk_type = Column(String(100), nullable=False)
    description = Column(String(1000))
    severity = Column(String(50))  # low, medium, high, critical
    probability = Column(String(50))  # unlikely, possible, likely, certain
    mitigation_plan = Column(String(2000))
    status = Column(
        String(50), default="identified"
    )  # identified, assessed, mitigated, resolved
    responsible_party = Column(String(200))
    due_date = Column(DateTime)
    related_documents = Column(JSON)  # JSON array of document references

    def __repr__(self):
        return f"<GestaoRisco(id={self.id}, risk_type={self.risk_type}, status={self.status})>"

