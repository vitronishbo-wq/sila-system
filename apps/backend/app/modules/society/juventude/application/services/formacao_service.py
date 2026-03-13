from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.society.juventude.application.ports.formacao_repository_port import FormacaoRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.programa_repository_port import ProgramaRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.society.juventude.domain.enums import StatusFormacao
from apps.backend.app.modules.society.juventude.domain.models.formacao_juvenil import FormacaoJuvenil

class FormacaoService:

    def __init__(self, *, formacao_repo: FormacaoRepositoryPort, jovem_repo: JovemRepositoryPort, programa_repo: ProgramaRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.formacao_repo = formacao_repo
        self.jovem_repo = jovem_repo
        self.programa_repo = programa_repo
        self.request_service = request_service

    async def registrar_formacao(self, *, jovem_id: UUID, nome_curso: str, instituicao: str, carga_horaria: int, data_inicio: date, programa_id: UUID | None=None, data_fim: date | None=None, observacoes: str | None=None) -> FormacaoJuvenil:
        jovem = await self.jovem_repo.get_by_id(jovem_id)
        if jovem is None:
            raise ValueError('Jovem nao encontrado para registro de formacao')
        if programa_id is not None:
            programa = await self.programa_repo.get_by_id(programa_id)
            if programa is None:
                raise ValueError('Programa informado nao encontrado')
        codigo = await self.formacao_repo.next_codigo()
        formacao = FormacaoJuvenil.registrar(codigo_formacao=codigo, jovem_id=jovem_id, nome_curso=nome_curso, instituicao=instituicao, carga_horaria=carga_horaria, data_inicio=data_inicio, programa_id=programa_id, data_fim=data_fim, observacoes=observacoes)
        saved = await self.formacao_repo.save(formacao)
        if jovem.formacoes is None:
            jovem.formacoes = []
        if saved.id not in jovem.formacoes:
            jovem.formacoes.append(saved.id)
            await self.jovem_repo.save(jovem)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='REGISTRO_FORMACAO_JUVENIL', entity_id=saved.id, citizen_id=jovem.citizen_id, numero_processo=saved.codigo_formacao, metadata={'codigo_formacao': saved.codigo_formacao, 'jovem_id': str(saved.jovem_id), 'nome_curso': saved.nome_curso})
        return saved

    async def buscar_formacao(self, formacao_id: UUID) -> FormacaoJuvenil:
        formacao = await self.formacao_repo.get_by_id(formacao_id)
        if formacao is None:
            raise ValueError('Formacao nao encontrada')
        return formacao

    async def listar_formacoes(self, *, jovem_id: UUID | None=None, programa_id: UUID | None=None, status: StatusFormacao | None=None) -> list[FormacaoJuvenil]:
        if jovem_id is not None:
            return await self.formacao_repo.list_by_jovem(jovem_id)
        if programa_id is not None:
            return await self.formacao_repo.list_by_programa(programa_id)
        if status is not None:
            return await self.formacao_repo.list_by_status(status)
        return await self.formacao_repo.list_all()

    async def atualizar_status(self, *, formacao_id: UUID, status: StatusFormacao, certificado_emitido: bool | None=None) -> FormacaoJuvenil:
        formacao = await self.buscar_formacao(formacao_id)
        formacao.atualizar_status(status, certificado_emitido)
        return await self.formacao_repo.save(formacao)

    async def remover_formacao(self, formacao_id: UUID) -> None:
        deleted = await self.formacao_repo.delete(formacao_id)
        if not deleted:
            raise ValueError('Formacao nao encontrada')