"""Factories for society repositories used by cross-domain composition roots.

Keeping these imports in `app.core` avoids direct module-to-module wiring in
feature packages while preserving concrete runtime behavior.
"""
from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession

def make_assistencia_beneficiario_repository(db: AsyncSession):
    from app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_beneficiario_repository import SQLAlchemyBeneficiarioRepository
    return SQLAlchemyBeneficiarioRepository(db)

def make_assistencia_beneficio_repository(db: AsyncSession):
    from app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_beneficio_repository import SQLAlchemyBeneficioRepository
    return SQLAlchemyBeneficioRepository(db)

def make_assistencia_visita_repository(db: AsyncSession):
    from app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_visita_domiciliar_repository import SQLAlchemyVisitaDomiciliarRepository
    return SQLAlchemyVisitaDomiciliarRepository(db)

def make_educacao_matricula_repository(db: AsyncSession):
    from app.modules.society.educacao.infrastructure.repositories.sqlalchemy_matricula_repository import SQLAlchemyMatriculaRepository
    return SQLAlchemyMatriculaRepository(db)

def make_educacao_propina_repository(db: AsyncSession):
    from app.modules.society.educacao.infrastructure.repositories.sqlalchemy_propina_repository import SQLAlchemyPropinaRepository
    return SQLAlchemyPropinaRepository(db)

def make_educacao_turma_repository(db: AsyncSession):
    from app.modules.society.educacao.infrastructure.repositories.sqlalchemy_turma_repository import SQLAlchemyTurmaRepository
    return SQLAlchemyTurmaRepository(db)

def make_educacao_escola_repository(db: AsyncSession):
    from app.modules.society.educacao.infrastructure.repositories.sqlalchemy_escola_repository import SQLAlchemyEscolaRepository
    return SQLAlchemyEscolaRepository(db)

def make_emprego_candidato_repository(db: AsyncSession):
    from app.modules.society.emprego.infrastructure.repositories.sqlalchemy_candidato_repository import SQLAlchemyCandidatoRepository
    return SQLAlchemyCandidatoRepository(db)

def make_emprego_contrato_repository(db: AsyncSession):
    from app.modules.society.emprego.infrastructure.repositories.sqlalchemy_contrato_repository import SQLAlchemyContratoRepository
    return SQLAlchemyContratoRepository(db)

def make_juventude_jovem_repository(db: AsyncSession):
    from app.modules.society.juventude.infrastructure.repositories.sqlalchemy_jovem_repository import SQLAlchemyJovemRepository
    return SQLAlchemyJovemRepository(db)

def make_juventude_auxilio_repository(db: AsyncSession):
    from app.modules.society.juventude.infrastructure.repositories.sqlalchemy_auxilio_repository import SQLAlchemyAuxilioRepository
    return SQLAlchemyAuxilioRepository(db)

def make_juventude_bolsa_estudo_repository(db: AsyncSession):
    from app.modules.society.juventude.infrastructure.repositories.sqlalchemy_bolsa_estudo_repository import SQLAlchemyBolsaEstudoRepository
    return SQLAlchemyBolsaEstudoRepository(db)

def make_juventude_programa_repository(db: AsyncSession):
    from app.modules.society.juventude.infrastructure.repositories.sqlalchemy_programa_repository import SQLAlchemyProgramaRepository
    return SQLAlchemyProgramaRepository(db)

def make_saude_appointment_repository(db: AsyncSession):
    from app.modules.saude.infrastructure.repositories.appointment_repository import (
        AppointmentRepository,
    )
    return AppointmentRepository(db)

def make_saude_health_unit_repository(db: AsyncSession):
    from app.modules.saude.infrastructure.repositories.health_unit_repository import (
        HealthUnitRepository,
    )
    return HealthUnitRepository(db)

def make_saude_medical_record_repository(db: AsyncSession):
    from app.modules.saude.infrastructure.repositories.medical_record_repository import (
        MedicalRecordRepository,
    )
    return MedicalRecordRepository(db)
