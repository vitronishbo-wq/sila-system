from __future__ import annotations
import asyncio
from unittest.mock import AsyncMock
from uuid import uuid4
from apps.backend.app.modules.tourism.application.services.meio_hospedagem_service import MeioHospedagemService
from apps.backend.app.modules.tourism.domain.enums import ClassificacaoHoteleira, TipoMeioHospedagem

def test_cadastrar_hotel_sucesso() -> None:
    hotel_repo = AsyncMock()
    citizen_service = AsyncMock()
    request_service = AsyncMock()
    proprietario_id = uuid4()
    citizen_service.is_citizen_active.return_value = True
    hotel_repo.get_by_cnpj.return_value = None
    hotel_repo.next_cadastur.return_value = 'LUANDA/2026/0001'

    async def save_side_effect(hotel):
        return hotel
    hotel_repo.save.side_effect = save_side_effect
    service = MeioHospedagemService(hotel_repo=hotel_repo, citizen_service=citizen_service, request_service=request_service)
    result = asyncio.run(service.cadastrar_hotel(nome='Hotel Luanda', tipo=TipoMeioHospedagem.HOTEL, classificacao=ClassificacaoHoteleira.SUPERIOR, cnpj='12.345.678/0001-90', endereco='Av. Marginal', numero='100', bairro='Ingombotas', municipio='Luanda', provincia='Luanda', cep='1000', telefone='222123456', email='contato@hoteluanda.ao', quartos=50, capacidade_maxima=100, proprietario_id=proprietario_id))
    assert result.cadastur == 'LUANDA/2026/0001'
    hotel_repo.save.assert_called_once()
    request_service.create_request.assert_called_once()