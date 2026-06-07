from __future__ import annotations

import asyncio
from datetime import date, timedelta
from decimal import Decimal

from apps.backend.app.modules.society.assistencia_social.application.services.programa_social_service import (
    ProgramaSocialService,
)
from apps.backend.app.modules.society.assistencia_social.domain.enums import (
    PublicoAlvo,
    StatusProgramaSocial,
)
from apps.backend.app.modules.society.assistencia_social.tests._fakes import InMemoryProgramaRepo


def test_programa_social_ciclo_de_vida() -> None:

    async def scenario() -> None:
        service = ProgramaSocialService(programa_repo=InMemoryProgramaRepo())
        programa = await service.criar_programa(
            nome="Apoio Familiar Municipal",
            publico_alvo=PublicoAlvo.FAMILIA_BAIXA_RENDA,
            criterio_renda_max=Decimal("200.00"),
            valor_base=Decimal("90.00"),
            vagas=80,
            data_inicio=date.today(),
            observacoes="fase piloto",
        )
        assert programa.codigo.startswith("PRG/")
        assert programa.status == StatusProgramaSocial.RASCUNHO
        ativo = await service.ativar_programa(programa.id)
        assert ativo.status == StatusProgramaSocial.ATIVO
        suspenso = await service.suspender_programa(programa.id, "ajuste orcamental")
        assert suspenso.status == StatusProgramaSocial.SUSPENSO
        assert suspenso.observacoes == "ajuste orcamental"
        data_fim = date.today() + timedelta(days=120)
        encerrado = await service.encerrar_programa(
            programa.id, data_fim=data_fim, motivo="ciclo encerrado"
        )
        assert encerrado.status == StatusProgramaSocial.ENCERRADO
        assert encerrado.data_fim == data_fim

    asyncio.run(scenario())
