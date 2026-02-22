#!/usr/bin/env python3
"""
Script de inicialização do módulo Citizenship.

Popula o banco de dados com serviços básicos de cidadania
para permitir o funcionamento imediato do sistema.
"""

import asyncio
import logging
import sys
from datetime import datetime

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append("/opt/sila-system/backend")

from core.db.session import get_db
from modules.citizenship.models.citizenship_models import CitizenshipService
from modules.citizenship.schemas.citizenship import PriorityLevel
from modules.citizenship.services.citizenship_service import DEFAULT_SERVICES

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def initialize_citizenship_services():
    """
    Inicializa serviços básicos de cidadania no banco de dados.

    Cria os serviços padrão se eles não existirem.
    """
    logger.info("Iniciando população de serviços de cidadania...")

    try:
        # Criar sessão do banco
        async with get_db() as db:
            for service_data in DEFAULT_SERVICES:
                # Verificar se o serviço já existe
                existing_service = (
                    await db.query(CitizenshipService)
                    .filter(CitizenshipService.code == service_data["code"])
                    .first()
                )

                if existing_service:
                    logger.info(f"Serviço {service_data['code']} já existe, pulando...")
                    continue

                # Criar novo serviço
                new_service = CitizenshipService(
                    id=service_data.get("id"),
                    code=service_data["code"],
                    name=service_data["name"],
                    description=service_data["description"],
                    category=service_data["category"],
                    estimated_days=service_data["estimated_days"],
                    requirements=str(
                        service_data["requirements"]
                    ),  # Converter para string
                    is_active=True,
                    priority=PriorityLevel.NORMAL,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )

                db.add(new_service)
                logger.info(f"Serviço {service_data['code']} criado com sucesso")

            # Commit das alterações
            await db.commit()
            logger.info("Todos os serviços básicos criados com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao inicializar serviços: {e}")
        raise


def sync_initialize_services():
    """
    Função síncrona wrapper para compatibilidade.
    """
    asyncio.run(initialize_citizenship_services())


if __name__ == "__main__":
    logger.info("=== INICIALIZAÇÃO DO MÓDULO CITIZENSHIP ===")
    sync_initialize_services()
    logger.info("=== INICIALIZAÇÃO CONCLUÍDA ===")
