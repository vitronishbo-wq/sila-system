from fastapi import APIRouter, HTTPException

from ..api.schemas import (
    ConsultaNascimentoResponse,
    RegistoNascimentoRequest,
    RegistoNascimentoResponse,
    RegistoObitoRequest,
    RegistoObitoResponse,
)
from ..application.services.registo_service import RegistoCivilService
from ..domain.exceptions import RegistoDuplicadoError, RegistoNaoEncontradoError
from ..domain.models import RegistoNascimento, RegistoObito

router = APIRouter(prefix="/registo-civil", tags=["Registo Civil"])
_service: RegistoCivilService | None = None


def get_service() -> RegistoCivilService:
    global _service
    if _service is None:
        _service = RegistoCivilService()
    return _service


@router.post("/nascimento/registar", response_model=RegistoNascimentoResponse)
async def registar_nascimento(request: RegistoNascimentoRequest):
    try:
        service = get_service()
        registo = RegistoNascimento(
            nome_completo=request.nome_completo,
            data_nascimento=request.data_nascimento,
            genero=request.genero,
            naturalidade=request.naturalidade,
            nome_pai=request.nome_pai,
            nome_mae=request.nome_mae,
            provincia=request.provincia,
            municipio=request.municipio,
        )
        result = await service.registar_nascimento(registo)
        return RegistoNascimentoResponse(id=str(result.id), status=result.status.value)
    except RegistoDuplicadoError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nascimento/consultar", response_model=ConsultaNascimentoResponse)
async def consultar_nascimento(registo_id: str):
    try:
        service = get_service()
        registo = await service.consultar_nascimento(registo_id)
        return ConsultaNascimentoResponse(
            id=str(registo.id),
            nome_completo=registo.nome_completo,
            data_nascimento=registo.data_nascimento,
            genero=registo.genero,
            naturalidade=registo.naturalidade,
            nome_pai=registo.nome_pai,
            nome_mae=registo.nome_mae,
            provincia=registo.provincia,
            municipio=registo.municipio,
            status=registo.status.value,
        )
    except RegistoNaoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/obito/registar", response_model=RegistoObitoResponse)
async def registar_obito(request: RegistoObitoRequest):
    try:
        service = get_service()
        registo = RegistoObito(
            falecido_nome=request.falecido_nome,
            falecido_bi=request.falecido_bi,
            data_obito=request.data_obito,
            causa=request.causa,
            local_obito=request.local_obito,
            provincia=request.provincia,
            municipio=request.municipio,
        )
        result = await service.registar_obito(registo)
        return RegistoObitoResponse(id=str(result.id), status=result.status.value)
    except RegistoDuplicadoError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
