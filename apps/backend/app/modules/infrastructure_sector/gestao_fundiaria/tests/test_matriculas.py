from __future__ import annotations

from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.deps import (
    get_matricula_service,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.matriculas import (
    router as matriculas_router,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.imovel_service import (
    ImovelService,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.matricula_imovel_service import (
    MatriculaImovelService,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    NaturezaImovel,
    StatusMatriculaImovel,
    TipoImovel,
    TipoRegistro,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import (
    MatriculaImovelNotFoundError,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories import (
    SQLAlchemyImovelRepository,
    SQLAlchemyMatriculaImovelRepository,
)


class _JusticaValida:
    async def validar_matricula(
        self, numero_matricula: str, cartorio_nome: str, livro: str, folha: str
    ) -> bool:
        _ = (numero_matricula, cartorio_nome, livro, folha)
        return True


@pytest.mark.asyncio
async def test_matricula_service_fluxo_sucesso() -> None:
    imovel_repo = SQLAlchemyImovelRepository()
    imovel_service = ImovelService(imovel_repo=imovel_repo)
    service = MatriculaImovelService(
        matricula_repo=SQLAlchemyMatriculaImovelRepository(),
        imovel_repo=imovel_repo,
        justica_adapter=_JusticaValida(),
    )
    imovel = await imovel_service.cadastrar(
        tipo=TipoImovel.URBANO,
        natureza=NaturezaImovel.PRIVADO,
        area_total=Decimal("450.00"),
        endereco="Rua da Matricula, 10",
        bairro="Centro",
        municipio="Huambo",
        provincia="Huambo",
    )
    matricula = await service.registrar(
        imovel_inscricao=imovel.inscricao_imobiliaria,
        tipo_registro=TipoRegistro.MATRICULA,
        cartorio_nome="Cartorio Central",
        livro="L1",
        folha="F100",
        comarca="Huambo",
        provincia="Huambo",
        proprietario_documento="BI123456",
    )
    assert matricula.status == StatusMatriculaImovel.ATIVA
    matricula = await service.transferir(matricula.numero_matricula, novo_documento="BI654321")
    assert matricula.status == StatusMatriculaImovel.TRANSFERIDA
    linked_imovel = await imovel_repo.get_by_inscricao(imovel.inscricao_imobiliaria)
    assert linked_imovel is not None
    assert linked_imovel.matricula_id == matricula.id


def test_endpoint_registrar_matricula_retorna_201() -> None:
    mock_item = SimpleNamespace(
        id=uuid4(),
        numero_matricula="MAT/2026/000001",
        imovel_inscricao="IMV/2026/000001",
        tipo_registro=TipoRegistro.MATRICULA,
        cartorio_nome="Cartorio Central",
        livro="L1",
        folha="F100",
        comarca="Huambo",
        provincia="Huambo",
        data_registro=date(2026, 3, 4),
        status=StatusMatriculaImovel.ATIVA,
        ativo=True,
        proprietario_documento="BI123456",
        data_atualizacao=None,
        observacoes=None,
    )
    service = SimpleNamespace(
        has_justica_adapter=lambda: True, registrar=AsyncMock(return_value=mock_item)
    )
    app = FastAPI()
    app.include_router(matriculas_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_matricula_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/gestao-fundiaria/matriculas/",
        json={
            "imovel_inscricao": "IMV/2026/000001",
            "tipo_registro": "matricula",
            "cartorio_nome": "Cartorio Central",
            "livro": "L1",
            "folha": "F100",
            "comarca": "Huambo",
            "provincia": "Huambo",
            "proprietario_documento": "BI123456",
        },
    )
    assert response.status_code == 201
    assert response.json()["numero_matricula"] == "MAT/2026/000001"


def test_endpoint_registrar_matricula_sem_adapter_retorna_503() -> None:
    service = SimpleNamespace(has_justica_adapter=lambda: False, registrar=AsyncMock())
    app = FastAPI()
    app.include_router(matriculas_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_matricula_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/gestao-fundiaria/matriculas/",
        json={
            "imovel_inscricao": "IMV/2026/000001",
            "tipo_registro": "matricula",
            "cartorio_nome": "Cartorio Central",
            "livro": "L1",
            "folha": "F100",
            "comarca": "Huambo",
            "provincia": "Huambo",
        },
    )
    assert response.status_code == 503
    assert "Adapter de Justica indisponivel" in response.json()["detail"]
    service.registrar.assert_not_awaited()


def test_endpoint_obter_matricula_retorna_404() -> None:
    service = SimpleNamespace(
        obter_por_numero=AsyncMock(
            side_effect=MatriculaImovelNotFoundError("Matricula nao encontrada")
        )
    )
    app = FastAPI()
    app.include_router(matriculas_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_matricula_service] = lambda: service
    client = TestClient(app)
    response = client.get("/gestao-fundiaria/matriculas/MAT/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Matricula nao encontrada"
