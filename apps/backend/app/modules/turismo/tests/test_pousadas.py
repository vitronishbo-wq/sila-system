
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock
from uuid import uuid4

from app.modules.turismo.application.services.meio_hospedagem_service import MeioHospedagemService
from app.modules.turismo.domain.enums import ClassificacaoHoteleira


def test_cadastrar_pousada_sucesso() -> None:
    hotel_repo = AsyncMock()
    pousada_repo = AsyncMock()
    citizen_service = AsyncMock()

    proprietario_id = uuid4()
    citizen_service.is_citizen_active.return_value = True
    pousada_repo.get_by_cnpj.return_value = None
    pousada_repo.next_cadastur.return_value = "PO/LUANDA/2026/0001"

    async def save_side_effect(pousada):
        return pousada

    pousada_repo.save.side_effect = save_side_effect

    service = MeioHospedagemService(
        hotel_repo=hotel_repo,
        pousada_repo=pousada_repo,
        citizen_service=citizen_service,
    )

    result = asyncio.run(
        service.cadastrar_pousada(
            nome="Pousada Ilha",
            classificacao=ClassificacaoHoteleira.CONFORT,
            cnpj="98.765.432/0001-10",
            endereco="Rua da Ilha",
            numero="15",
            bairro="Ilha",
            municipio="Luanda",
            provincia="Luanda",
            cep="1000",
            telefone="222000111",
            email="contato@pousadailha.ao",
            quartos=20,
            capacidade_maxima=40,
            proprietario_id=proprietario_id,
        )
    )

    assert result.cadastur == "PO/LUANDA/2026/0001"
    assert result.classificacao == ClassificacaoHoteleira.CONFORT
    pousada_repo.save.assert_called_once()
