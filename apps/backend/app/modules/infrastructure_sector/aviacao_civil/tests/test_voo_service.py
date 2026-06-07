from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.services.aeronave_service import (
    AeronaveService,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.services.voo_service import (
    VooService,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import (
    CategoriaAeronave,
    NaturezaVoo,
    RegrasVoo,
    StatusVoo,
    TipoAeronave,
    TipoVoo,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.persistence.outbox import (
    InMemoryOutbox,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.repositories.inmemory_aeronave_repository import (
    InMemoryAeronaveRepository,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.repositories.inmemory_voo_repository import (
    InMemoryVooRepository,
)


@pytest.mark.asyncio
async def test_programar_decolar_pousar_voo() -> None:
    aeronave_repo = InMemoryAeronaveRepository()
    voo_repo = InMemoryVooRepository()
    outbox = InMemoryOutbox()
    aeronave_service = AeronaveService(aeronave_repo=aeronave_repo, outbox=outbox)
    voo_service = VooService(voo_repo=voo_repo, aeronave_repo=aeronave_repo, outbox=outbox)
    aeronave = await aeronave_service.registrar_aeronave(
        matricula="D2-ABC",
        tipo=TipoAeronave.AVIAO,
        categoria=CategoriaAeronave.TRANSPORTE_PASSAGEIRO,
        fabricante="Boeing",
        modelo="737-800",
        numero_serie="SN12345",
        ano_fabricacao=2017,
        proprietario_cpf_cnpj="12345678901",
        capacidade_passageiros=160,
    )
    partida = datetime.utcnow() + timedelta(hours=2)
    chegada = partida + timedelta(hours=1, minutes=20)
    voo = await voo_service.programar_voo(
        numero_voo="DT1001",
        empresa_id=uuid4(),
        aeronave_id=aeronave.id,
        aeroporto_origem_id=uuid4(),
        aeroporto_destino_id=uuid4(),
        data_hora_partida=partida,
        data_hora_chegada=chegada,
        tipo=TipoVoo.REGULAR,
        natureza=NaturezaVoo.DOMESTICO,
        regras=RegrasVoo.IFR,
        passageiros=120,
        tripulantes=[{"funcao": "piloto", "nome": "Comandante A"}],
    )
    assert voo.status == StatusVoo.PROGRAMADO
    decolagem_real = partida + timedelta(minutes=20)
    voo = await voo_service.registrar_decolagem(voo_id=voo.id, data_hora=decolagem_real)
    assert voo.status == StatusVoo.EM_VOO
    pouso_real = decolagem_real + timedelta(hours=1, minutes=15)
    voo = await voo_service.registrar_pouso(voo_id=voo.id, data_hora=pouso_real)
    assert voo.status == StatusVoo.POUSADO
    aeronave_atualizada = await aeronave_repo.get_by_id(aeronave.id)
    assert aeronave_atualizada is not None
    assert aeronave_atualizada.horas_voadas_total > 0
    eventos = await outbox.list_events()
    assert len(eventos) >= 3
