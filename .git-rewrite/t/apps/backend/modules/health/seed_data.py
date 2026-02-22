"""
Seed data script for Health module.

This script populates the health_services table with initial medical services.
Run this after migrations to have services available for appointments.
"""

import asyncio
import logging
import sys
from uuid import uuid4

# Add backend to path
sys.path.insert(0, sys.path[0] + "/.." if sys.path[0] else "..")


from core.db import AsyncSessionLocal
from modules.health.models import HealthService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Default health services data
DEFAULT_HEALTH_SERVICES = [
    {
        "name": "Consulta Clínica Geral",
        "description": "Consulta médica básica para avaliação geral de saúde",
        "category": "consulta",
        "status": "available",
        "estimated_duration": "30 minutos",
        "requirements": "Identificação, Cartão SUS",
    },
    {
        "name": "Exame de Sangue",
        "description": "Hemograma completo e exames laboratoriais básicos",
        "category": "exame",
        "status": "available",
        "estimated_duration": "15 minutos",
        "requirements": "Jejum de 12 horas, Identificação",
    },
    {
        "name": "Vacinação COVID-19",
        "description": "Aplicação de vacinas contra COVID-19",
        "category": "vacina",
        "status": "available",
        "estimated_duration": "10 minutos",
        "requirements": "Identificação, Cartão de Vacinação",
    },
    {
        "name": "Consulta Cardiológica",
        "description": "Avaliação especializada do sistema cardiovascular",
        "category": "consulta",
        "status": "available",
        "estimated_duration": "45 minutos",
        "requirements": "Identificação, Exames anteriores (se houver)",
    },
    {
        "name": "Consulta Pediátrica",
        "description": "Avaliação médica especializada para crianças",
        "category": "consulta",
        "status": "available",
        "estimated_duration": "30 minutos",
        "requirements": "Identificação da criança, Cartão de Vacinação",
    },
    {
        "name": "Consulta Ginecológica",
        "description": "Avaliação médica especializada em saúde da mulher",
        "category": "consulta",
        "status": "available",
        "estimated_duration": "30 minutos",
        "requirements": "Identificação",
    },
    {
        "name": "Consulta Psiquiátrica",
        "description": "Avaliação e acompanhamento em saúde mental",
        "category": "consulta",
        "status": "available",
        "estimated_duration": "45 minutos",
        "requirements": "Identificação, Encaminhamento médico (recomendado)",
    },
    {
        "name": "Raio-X",
        "description": "Exame de imagem radiológica",
        "category": "exame",
        "status": "available",
        "estimated_duration": "20 minutos",
        "requirements": "Identificação, Encaminhamento médico",
    },
    {
        "name": "Ultra-sonografia",
        "description": "Exame de imagem por ultra-som",
        "category": "exame",
        "status": "available",
        "estimated_duration": "30 minutos",
        "requirements": "Identificação, Encaminhamento médico",
    },
    {
        "name": "Internação Hospitalar",
        "description": "Internação para tratamento médico especializado",
        "category": "internacao",
        "status": "unavailable",
        "estimated_duration": "Variável",
        "requirements": "Encaminhamento médico, Autorização prévia",
    },
]


async def seed_health_services():
    """Seed health services table with initial data."""
    logger.info("🌱 Iniciando seed de health_services...")

    async with AsyncSessionLocal() as session:
        try:
            # Import HealthService model
            from sqlalchemy import select

            created_count = 0
            skipped_count = 0

            for service_data in DEFAULT_HEALTH_SERVICES:
                # Check if service already exists (by name)
                stmt = select(HealthService).where(
                    HealthService.name == service_data["name"]
                )
                result = await session.execute(stmt)
                existing = result.scalar_one_or_none()

                if existing:
                    logger.info(
                        f"⏭️  Serviço '{service_data['name']}' já existe, pulando..."
                    )
                    skipped_count += 1
                    continue

                # Create new service
                service = HealthService(
                    id=uuid4(),
                    name=service_data["name"],
                    description=service_data["description"],
                    category=service_data["category"],
                    status=service_data["status"],
                    estimated_duration=service_data["estimated_duration"],
                    requirements=service_data["requirements"],
                )
                session.add(service)
                created_count += 1
                logger.info(f"✅ Serviço '{service_data['name']}' criado")

            await session.commit()
            logger.info(
                f"🎉 Seed concluído: {created_count} serviços criados, {skipped_count} já existiam"
            )
            return {"created": created_count, "skipped": skipped_count}

        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Erro ao fazer seed: {e}")
            raise


async def main():
    """Main entry point for seed script."""
    try:
        result = await seed_health_services()
        print(f"\n✅ Seed concluído com sucesso!")
        print(f"   - Criados: {result['created']}")
        print(f"   - Já existiam: {result['skipped']}")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao executar seed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
