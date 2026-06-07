from fastapi import APIRouter, HTTPException

from ..api.schemas import (
    TipoDocumentoResponse,
    VerificarDocumentoRequest,
    VerificarDocumentoResponse,
)
from ..application.services.verificacao_service import (
    VerificacaoDocumentalService,
)
from ..domain.exceptions import (
    TipoDocumentoNaoSuportadoError,
)
from ..domain.models import TipoDocumento

router = APIRouter(prefix="/integracao-nacional/verificacao-documental", tags=["Verificacao Documental"])
_service: VerificacaoDocumentalService | None = None


def get_service() -> VerificacaoDocumentalService:
    global _service
    if _service is None:
        _service = VerificacaoDocumentalService()
    return _service


@router.post("/verificar", response_model=VerificarDocumentoResponse)
async def verificar_documento(request: VerificarDocumentoRequest):
    try:
        tipo = TipoDocumento(request.tipo)
        service = get_service()
        result = await service.verificar(tipo, request.conteudo_base64)
        return VerificarDocumentoResponse(
            valido=result.valido,
            status=result.status.value,
            metodo=result.metodo.value,
            confianca_global=result.confianca_global,
            problemas=result.problemas,
        )
    except TipoDocumentoNaoSuportadoError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Tipo de documento invalido: {request.tipo}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tipos", response_model=list[TipoDocumentoResponse])
async def listar_tipos_documentais():
    service = get_service()
    return [
        TipoDocumentoResponse(tipo=t.value, nome=t.name, suportado=t in service.TIPOS_SUPORTADOS)
        for t in TipoDocumento
    ]
