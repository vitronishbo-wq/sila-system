from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.api.deps import get_current_user
from apps.backend.app.modules.educacao.api.deps import (
    get_wizard_matricula_service,
)
from apps.backend.app.modules.educacao.api.schemas.wizard_schema import (
    EscolaFilterParams,
    Passo1EstudanteCreate,
    Passo1EstudanteResponse,
    Passo2EncarregadoCreate,
    Passo2EncarregadoResponse,
    Passo3SelecaoCreate,
    Passo3SelecaoResponse,
    Passo4DocumentosResponse,
    Passo5ElegibilidadeResponse,
    Passo6PagamentoResponse,
    Passo7ConfirmacaoResponse,
    PassoStatus,
    TimelineEvent,
    WizardResumoResponse,
)
from apps.backend.app.modules.educacao.application.canonical.wizard_matricula_service import (
    WizardMatriculaService,
)

router = APIRouter(
    prefix="/matriculas/wizard",
    tags=["Educacao - Wizard Matricula"],
)

current_user_dep = Depends(get_current_user)
wizard_service_dep = Depends(get_wizard_matricula_service)


@router.post("/iniciar", response_model=WizardResumoResponse, status_code=status.HTTP_201_CREATED)
async def iniciar_wizard(
    _: dict = current_user_dep,
    service: WizardMatriculaService = wizard_service_dep,
):
    citizen_id = _.get("citizen_id", _.get("sub"))
    if not citizen_id:
        raise HTTPException(status_code=400, detail="citizen_id nao encontrado no token")
    session = await service.iniciar_wizard(UUID(citizen_id))
    return _resumo_response(session)


@router.get("/{wizard_id}", response_model=WizardResumoResponse)
async def obter_wizard(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    session = await service.get_wizard(wizard_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessao wizard nao encontrada")
    return _resumo_response(session)


# ─── Passo 1: Estudante ─────────────────────────────────────────────


@router.post("/{wizard_id}/passo1/estudante", response_model=Passo1EstudanteResponse)
async def salvar_passo1(
    wizard_id: UUID,
    dados: Passo1EstudanteCreate,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    try:
        session = await service.salvar_passo1(wizard_id, dados)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Passo1EstudanteResponse(
        wizard_id=session.id,
        passo=1,
        status=PassoStatus.CONFIRMADO,
        dados=dados,
    )


@router.get("/{wizard_id}/passo1/estudante", response_model=Passo1EstudanteResponse)
async def obter_passo1(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    session = await service.get_wizard(wizard_id)
    if not session or not session.dados_estudante:
        raise HTTPException(status_code=404, detail="Dados do estudante nao encontrados")
    return Passo1EstudanteResponse(
        wizard_id=session.id,
        passo=1,
        status=PassoStatus.CONFIRMADO,
        dados=session.dados_estudante,
    )


# ─── Passo 2: Encarregado ───────────────────────────────────────────


@router.post("/{wizard_id}/passo2/encarregado", response_model=Passo2EncarregadoResponse)
async def salvar_passo2(
    wizard_id: UUID,
    dados: Passo2EncarregadoCreate,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    try:
        session = await service.salvar_passo2(wizard_id, dados)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Passo2EncarregadoResponse(
        wizard_id=session.id,
        passo=2,
        status=PassoStatus.CONFIRMADO,
        dados=dados,
    )


@router.get("/{wizard_id}/passo2/encarregado", response_model=Passo2EncarregadoResponse)
async def obter_passo2(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    session = await service.get_wizard(wizard_id)
    if not session or not session.dados_encarregado:
        raise HTTPException(status_code=404, detail="Dados do encarregado nao encontrados")
    return Passo2EncarregadoResponse(
        wizard_id=session.id,
        passo=2,
        status=PassoStatus.CONFIRMADO,
        dados=session.dados_encarregado,
    )


# ─── Passo 3: Escola ────────────────────────────────────────────────


@router.post("/{wizard_id}/passo3/selecionar", response_model=Passo3SelecaoResponse)
async def selecionar_escola(
    wizard_id: UUID,
    dados: Passo3SelecaoCreate,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    try:
        session = await service.salvar_passo3(wizard_id, dados)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Passo3SelecaoResponse(
        wizard_id=session.id,
        passo=3,
        status=PassoStatus.CONFIRMADO,
        dados=dados,
    )


@router.get("/{wizard_id}/passo3/selecionar", response_model=Passo3SelecaoResponse)
async def obter_selecao_escola(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    session = await service.get_wizard(wizard_id)
    if not session or not session.selecao_escola:
        raise HTTPException(status_code=404, detail="Selecao de escola nao encontrada")
    return Passo3SelecaoResponse(
        wizard_id=session.id,
        passo=3,
        status=PassoStatus.CONFIRMADO,
        dados=session.selecao_escola,
    )


# ─── Passo 4: Documentos ────────────────────────────────────────────


@router.post("/{wizard_id}/passo4/documentos/upload", response_model=Passo4DocumentosResponse)
async def upload_documento(
    wizard_id: UUID,
    tipo: str = Query(..., pattern=r"^(bi_estudante|bi_encarregado|fotografia|certificado_anterior|boletim_anterior|comprovativo_morada)$"),
    _: dict = current_user_dep,
    service: WizardMatriculaService = wizard_service_dep,
):
    documento = {
        "document_id": str(UUID(int=0)),
        "tipo": tipo,
        "nome_original": f"{tipo}.pdf",
        "tamanho_bytes": 0,
        "content_type": "application/pdf",
        "url": f"/api/v1/educacao/documentos/{wizard_id}/{tipo}",
    }
    try:
        session = await service.salvar_passo4(wizard_id, documento)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    tipos_existentes = {d.get("tipo") for d in (session.documentos or [])}
    obrigatorios = {"bi_estudante", "bi_encarregado", "fotografia"}
    pendentes = list(obrigatorios - tipos_existentes)

    return Passo4DocumentosResponse(
        wizard_id=session.id,
        passo=4,
        status=PassoStatus.CONFIRMADO,
        documentos=session.documentos or [],
        obrigatorios_pendentes=pendentes,
    )


@router.get("/{wizard_id}/passo4/documentos", response_model=Passo4DocumentosResponse)
async def listar_documentos(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    session = await service.get_wizard(wizard_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada")

    tipos_existentes = {d.get("tipo") for d in (session.documentos or [])}
    obrigatorios = {"bi_estudante", "bi_encarregado", "fotografia"}
    pendentes = list(obrigatorios - tipos_existentes)

    return Passo4DocumentosResponse(
        wizard_id=session.id,
        passo=4,
        status=PassoStatus.CONFIRMADO if not pendentes else PassoStatus.PREENCHIDO,
        documentos=session.documentos or [],
        obrigatorios_pendentes=pendentes,
    )


# ─── Passo 5: Elegibilidade ─────────────────────────────────────────


@router.post("/{wizard_id}/passo5/elegibilidade", response_model=Passo5ElegibilidadeResponse)
async def verificar_elegibilidade(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    try:
        resultado = await service.executar_elegibilidade(wizard_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Passo5ElegibilidadeResponse(**resultado)


@router.get("/{wizard_id}/passo5/elegibilidade", response_model=Passo5ElegibilidadeResponse)
async def obter_elegibilidade(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    session = await service.get_wizard(wizard_id)
    if not session or not session.resultado_elegibilidade:
        raise HTTPException(status_code=404, detail="Elegibilidade ainda nao calculada")
    return Passo5ElegibilidadeResponse(**session.resultado_elegibilidade)


# ─── Passo 6: Pagamento ─────────────────────────────────────────────


@router.post("/{wizard_id}/passo6/pagamento/gerar-referencia", response_model=Passo6PagamentoResponse)
async def gerar_referencia(
    wizard_id: UUID,
    modalidade: str = Query("referencia", pattern=r"^(multicaixa|referencia|wallet)$"),
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    session = await service.get_wizard(wizard_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessao wizard nao encontrada")
    citizen_id = session.citizen_id
    pagamento_service = getattr(service, "_pagamento_service", None)
    if pagamento_service:
        ref = await pagamento_service.gerar_referencia(
            wizard_id=wizard_id,
            citizen_id=citizen_id,
            amount=2500.0,
        )
        pagamento_data = {
            "modalidade": modalidade,
            "entidade": ref.entity,
            "referencia": ref.reference,
            "valor": f"{ref.amount:.2f}",
            "moeda": ref.currency,
            "status": ref.status,
            "comprovativo_url": None,
        }
    else:
        pagamento_data = {
            "modalidade": modalidade,
            "entidade": "12345",
            "referencia": f"{abs(hash(str(wizard_id))) % 10**9:09d}",
            "valor": "2500.00",
            "moeda": "AOA",
            "status": "PENDENTE",
            "comprovativo_url": None,
        }
    try:
        session = await service.confirmar_pagamento(wizard_id, pagamento_data)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Passo6PagamentoResponse(
        wizard_id=session.id,
        passo=6,
        status=PassoStatus.CONFIRMADO,
        pagamento=pagamento_data,
    )


@router.get("/{wizard_id}/passo6/pagamento", response_model=Passo6PagamentoResponse)
async def obter_pagamento(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    session = await service.get_wizard(wizard_id)
    if not session or not session.pagamento:
        raise HTTPException(status_code=404, detail="Dados de pagamento nao encontrados")
    return Passo6PagamentoResponse(
        wizard_id=session.id,
        passo=6,
        status=PassoStatus.CONFIRMADO,
        pagamento=session.pagamento,
    )


# ─── Passo 7: Confirmacao ───────────────────────────────────────────


@router.post("/{wizard_id}/passo7/confirmar", response_model=Passo7ConfirmacaoResponse)
async def confirmar_matricula(
    wizard_id: UUID,
    service: WizardMatriculaService = wizard_service_dep,
    _: dict = current_user_dep,
):
    resultado = await service.confirmar_matricula(wizard_id)
    if "erro" in resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado["erro"],
        )
    return Passo7ConfirmacaoResponse(**resultado)


@router.get("/{wizard_id}/passo7/comprovativo")
async def obter_comprovativo(
    wizard_id: UUID,
    _: dict = current_user_dep,
):
    return {"url": f"/api/v1/educacao/matriculas/wizard/{wizard_id}/comprovativo"}


@router.get("/{wizard_id}/qrcode")
async def obter_qrcode(
    wizard_id: UUID,
    _: dict = current_user_dep,
):
    return {"url": f"/api/v1/educacao/matriculas/wizard/{wizard_id}/qrcode"}


# ─── Helper ─────────────────────────────────────────────────────────


def _resumo_response(session) -> WizardResumoResponse:
    passos = {}
    for i in range(1, 8):
        key = f"passo{i}"
        if i == 1 and session.dados_estudante:
            passos[key] = PassoStatus.CONFIRMADO
        elif i == 2 and session.dados_encarregado:
            passos[key] = PassoStatus.CONFIRMADO
        elif i == 3 and session.selecao_escola:
            passos[key] = PassoStatus.CONFIRMADO
        elif i == 4 and session.documentos:
            passos[key] = PassoStatus.CONFIRMADO
        elif i == 5 and session.resultado_elegibilidade:
            passos[key] = PassoStatus.CONFIRMADO
        elif i == 6 and session.pagamento:
            passos[key] = PassoStatus.CONFIRMADO
        elif i == 7 and session.matricula_id:
            passos[key] = PassoStatus.CONFIRMADO
        else:
            passos[key] = PassoStatus.RASCUNHO

    has_estudante = bool(session.dados_estudante)
    has_encarregado = bool(session.dados_encarregado)
    has_escola = bool(session.selecao_escola)
    has_docs = bool(session.documentos)
    has_elegibilidade = bool(session.resultado_elegibilidade)
    has_pagamento = bool(session.pagamento)
    has_matricula = bool(session.matricula_id)

    timeline = [
        TimelineEvent(etapa="Pedido criado", concluido=True),
        TimelineEvent(etapa="Documentos recebidos", concluido=has_docs),
        TimelineEvent(etapa="Validacao concluida", concluido=has_elegibilidade),
        TimelineEvent(etapa="Pagamento confirmado", concluido=has_pagamento),
        TimelineEvent(etapa="Matricula emitida", concluido=has_matricula),
        TimelineEvent(etapa="Concluido", concluido=has_matricula),
    ]

    if has_matricula:
        proxima_acao = "Acompanhar o estado no portal do cidadao"
    elif has_pagamento:
        proxima_acao = "Confirmar matricula no passo 7"
    elif has_elegibilidade:
        proxima_acao = "Efectuar pagamento da taxa de inscricao"
    elif has_docs:
        proxima_acao = "Verificar elegibilidade no passo 5"
    elif has_escola:
        proxima_acao = "Anexar documentos do estudante no passo 4"
    elif has_encarregado:
        proxima_acao = "Selecionar escola e turma no passo 3"
    elif has_estudante:
        proxima_acao = "Preencher dados do encarregado no passo 2"
    else:
        proxima_acao = "Preencher dados do estudante no passo 1"

    return WizardResumoResponse(
        wizard_id=session.id,
        citizen_id=session.citizen_id,
        numero_pedido=f"EDU-{session.id.hex[:8].upper()}" if has_matricula else None,
        status=session.status,
        passo_atual=session.passo_atual,
        sla_previsto="3 dias uteis",
        proxima_acao=proxima_acao,
        timeline=timeline,
        passos=passos,
        created_at=session.created_at,
        updated_at=session.updated_at,
        expires_at=session.expires_at,
    )
