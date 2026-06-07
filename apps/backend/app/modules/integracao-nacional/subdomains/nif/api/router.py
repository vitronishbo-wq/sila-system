from fastapi import APIRouter, HTTPException

from ..api.schemas import (
    NifConsultaResponse,
    NifConsultarRequest,
    NifVerificacaoResponse,
    NifValidarRequest,
)
from ..application.services.nif_service import NifService
from ..domain.exceptions import (
    NifNaoEncontradoError,
    NifNumeroInvalidoError,
)
from ..infrastructure.adapters import NifMockAdapter

router = APIRouter(prefix="/integracao-nacional/nif", tags=["NIF - Numero de Identificacao Fiscal"])
_service: NifService | None = None


def get_nif_service() -> NifService:
    global _service
    if _service is None:
        _service = NifService(provider=NifMockAdapter())
    return _service


@router.post("/validar", response_model=NifVerificacaoResponse)
async def validar_nif(request: NifValidarRequest):
    try:
        service = get_nif_service()
        result = await service.validar(request.nif)
        return NifVerificacaoResponse(
            nif=result.nif,
            valido=result.valido,
            status=result.status.value,
            contribuinte_encontrado=result.contribuinte_encontrado,
            verificacao_timestamp=result.verificacao_timestamp,
        )
    except NifNumeroInvalidoError:
        raise HTTPException(status_code=400, detail="Numero de NIF invalido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/consultar", response_model=NifConsultaResponse)
async def consultar_nif(request: NifConsultarRequest):
    try:
        service = get_nif_service()
        dados = await service.consultar(request.nif)
        return NifConsultaResponse(
            nif=dados.nif,
            encontrado=True,
            full_name=dados.full_name,
            tipo=dados.tipo.value if dados.tipo else None,
            status=dados.status.value if dados.status else None,
            bi_numero=dados.bi_numero,
            morada=dados.morada,
            atividade_economica=dados.atividade_economica,
        )
    except NifNaoEncontradoError:
        raise HTTPException(status_code=404, detail="NIF nao encontrado")
    except NifNumeroInvalidoError:
        raise HTTPException(status_code=400, detail="Numero de NIF invalido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
