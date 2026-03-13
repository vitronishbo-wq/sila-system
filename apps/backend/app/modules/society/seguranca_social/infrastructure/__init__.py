from apps.backend.app.modules.society.seguranca_social.infrastructure.models import BeneficiarioModel, PensaoModel
from apps.backend.app.modules.society.seguranca_social.infrastructure.repositories import SQLAlchemyBeneficiarioRepository, SQLAlchemyPensaoRepository
__all__ = ['BeneficiarioModel', 'PensaoModel', 'SQLAlchemyBeneficiarioRepository', 'SQLAlchemyPensaoRepository']