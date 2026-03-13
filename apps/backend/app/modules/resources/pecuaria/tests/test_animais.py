from __future__ import annotations
from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.pecuaria.api.deps import get_animal_service
from apps.backend.app.modules.resources.pecuaria.api.endpoints.animais import router as animais_router
from apps.backend.app.modules.resources.pecuaria.application.services.animal_service import AnimalService
from apps.backend.app.modules.resources.pecuaria.domain.enums import Sexo, StatusAnimal, TipoAnimal

@pytest.mark.asyncio
async def test_cadastrar_animal_sucesso():
    animal_repo = AsyncMock()
    propriedade_repo = AsyncMock()
    rebanho_repo = AsyncMock()
    proprietario_id = uuid4()
    propriedade_id = uuid4()
    raca_id = uuid4()
    propriedade_repo.get_by_id.return_value = {'id': propriedade_id}
    animal_repo.get_by_brinco.return_value = None
    animal_repo.save.side_effect = lambda item: item
    service = AnimalService(animal_repo=animal_repo, propriedade_repo=propriedade_repo, rebanho_repo=rebanho_repo)
    result = await service.cadastrar_animal(brinco='FAZ/2026/0001', tipo=TipoAnimal.BOVINO, raca_id=raca_id, sexo=Sexo.FEMEA, data_nascimento=date.today() - timedelta(days=365), proprietario_id=proprietario_id, propriedade_id=propriedade_id)
    assert result.brinco == 'FAZ/2026/0001'
    assert result.status == StatusAnimal.ATIVO
    animal_repo.save.assert_called_once()

def test_endpoint_obter_animal_retorna_404():
    service = SimpleNamespace(buscar_animal=AsyncMock(side_effect=ValueError('Animal nao encontrado')))
    app = FastAPI()
    app.include_router(animais_router, prefix='/pecuaria')
    app.dependency_overrides[get_animal_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/pecuaria/animais/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Animal nao encontrado'