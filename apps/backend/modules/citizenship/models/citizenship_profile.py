from config.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

class CitizenshipProfile(Base):
    __tablename__ = "citizenship_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Exemplo: Número de registo de nascimento ou outros dados
    registration_number: Mapped[str] = mapped_column(String(50), nullable=True)

    user = relationship("User", back_populates="citizenship_profile")
