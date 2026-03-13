from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.society.desporto.application.ports.competicao_repository_port import CompeticaoRepositoryPort
from apps.backend.app.modules.society.desporto.application.ports.educacao_service_port import EducacaoServicePort
from apps.backend.app.modules.society.desporto.application.ports.obras_publicas_service_port import ObrasPublicasServicePort
from apps.backend.app.modules.society.desporto.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.society.desporto.application.ports.turismo_service_port import TurismoServicePort
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusCompeticao, TipoCompeticao
from apps.backend.app.modules.society.desporto.domain.models.competicao import Competicao

class CompeticaoService:

    def __init__(self, *, competicao_repo: CompeticaoRepositoryPort, turismo_service: TurismoServicePort | None=None, educacao_service: EducacaoServicePort | None=None, obras_publicas_service: ObrasPublicasServicePort | None=None, request_service: RequestServicePort | None=None) -> None:
        self.competicao_repo = competicao_repo
        self.turismo_service = turismo_service
        self.educacao_service = educacao_service
        self.obras_publicas_service = obras_publicas_service
        self.request_service = request_service

    async def cadastrar_competicao(self, *, nome: str, tipo: TipoCompeticao, modalidade: ModalidadeDesportiva, data_inicio: date, data_fim: date, municipio: str, provincia: str, organizador_id: UUID, codigo_obra_instalacao: str | None=None, atracao_turistica_id: UUID | None=None, instituicao_educacional_id: UUID | None=None, premiacao_total: Decimal | None=None, observacoes: str | None=None) -> Competicao:
        await self._validar_integracoes(codigo_obra_instalacao=codigo_obra_instalacao, atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id)
        codigo = await self.competicao_repo.next_codigo()
        competicao = Competicao.criar(codigo_competicao=codigo, nome=nome, tipo=tipo, modalidade=modalidade, data_inicio=data_inicio, data_fim=data_fim, municipio=municipio, provincia=provincia, organizador_id=organizador_id, codigo_obra_instalacao=codigo_obra_instalacao, atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id, premiacao_total=premiacao_total, observacoes=observacoes)
        saved = await self.competicao_repo.save(competicao)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_COMPETICAO', entity_id=saved.id, metadata={'codigo': saved.codigo_competicao, 'nome': saved.nome, 'tipo': saved.tipo.value, 'modalidade': saved.modalidade.value}, numero_processo=saved.codigo_competicao)
        return saved

    async def buscar_competicao(self, competicao_id: UUID) -> Competicao:
        item = await self.competicao_repo.get_by_id(competicao_id)
        if item is None:
            raise ValueError('Competicao nao encontrada')
        return item

    async def listar_competicoes(self, *, tipo: TipoCompeticao | None=None, modalidade: ModalidadeDesportiva | None=None, status: StatusCompeticao | None=None, data_inicio: date | None=None, data_fim: date | None=None, somente_ativas: bool=True) -> list[Competicao]:
        if data_inicio is not None and data_fim is not None:
            itens = await self.competicao_repo.list_by_periodo(data_inicio, data_fim)
        elif modalidade is not None:
            itens = await self.competicao_repo.list_by_modalidade(modalidade)
        elif status is not None:
            itens = await self.competicao_repo.list_by_status(status)
        elif tipo is not None:
            itens = await self.competicao_repo.list_by_tipo(tipo)
        else:
            itens = await self.competicao_repo.list_all()
        if somente_ativas:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_competicao(self, *, competicao_id: UUID, nome: str | None=None, tipo: TipoCompeticao | None=None, modalidade: ModalidadeDesportiva | None=None, data_inicio: date | None=None, data_fim: date | None=None, municipio: str | None=None, provincia: str | None=None, codigo_obra_instalacao: str | None=None, atracao_turistica_id: UUID | None=None, instituicao_educacional_id: UUID | None=None, premiacao_total: Decimal | None=None, inscricoes_abertas: bool | None=None, status: StatusCompeticao | None=None, ativo: bool | None=None, observacoes: str | None=None) -> Competicao:
        item = await self.buscar_competicao(competicao_id)
        await self._validar_integracoes(codigo_obra_instalacao=codigo_obra_instalacao, atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id)
        item.atualizar(nome=nome, tipo=tipo, modalidade=modalidade, data_inicio=data_inicio, data_fim=data_fim, municipio=municipio, provincia=provincia, codigo_obra_instalacao=codigo_obra_instalacao, atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id, premiacao_total=premiacao_total, inscricoes_abertas=inscricoes_abertas, status=status, ativo=ativo, observacoes=observacoes)
        return await self.competicao_repo.save(item)

    async def remover_competicao(self, competicao_id: UUID) -> None:
        deleted = await self.competicao_repo.delete(competicao_id)
        if not deleted:
            raise ValueError('Competicao nao encontrada')

    async def _validar_integracoes(self, *, codigo_obra_instalacao: str | None, atracao_turistica_id: UUID | None, instituicao_educacional_id: UUID | None) -> None:
        if codigo_obra_instalacao and self.obras_publicas_service is not None:
            obra_ok = await self.obras_publicas_service.obra_exists(codigo_obra_instalacao)
            if not obra_ok:
                raise ValueError('Obra de instalacao informada nao encontrada')
        if atracao_turistica_id is not None and self.turismo_service is not None:
            atracao_ok = await self.turismo_service.atracao_exists(atracao_turistica_id)
            if not atracao_ok:
                raise ValueError('Atracao turistica informada nao encontrada')
        if instituicao_educacional_id is not None and self.educacao_service is not None:
            instituicao_ok = await self.educacao_service.instituicao_exists(instituicao_educacional_id)
            if not instituicao_ok:
                raise ValueError('Instituicao educacional informada nao encontrada')