"""
Identity model for external provider authentication.

This model stores the relationship between local users and external
identity providers (OAuth, SSO, etc.) for authentication purposes.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from core.db.base_class import Base


class Identity(Base):
    """
    Model for storing external identity provider relationships.

    Links local users to external authentication providers,
    enabling OAuth/SSO functionality while maintaining
    user identity consistency across systems.
    """

    __tablename__ = "identity_identities"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(
        String(50), nullable=False, index=True
    )  # e.g., "google", "facebook", "github"
    external_id = Column(
        String(255), nullable=False, index=True
    )  # ID from the provider
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Metadata
    provider_data = Column(String(2000))  # JSON string with additional provider info
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<Identity(id={self.id}, provider='{self.provider}', external_id='{self.external_id[:20]}...', user_id={self.user_id})>"
