from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from app.modules.society.assistencia_social.application.ports import CadastroUnicoRepositoryPort, CitizenServicePort, EducacaoServicePort, JuventudeServicePort, RequestServicePort
from app.modules.society.assistencia_social.application.services._codegen import next_codigo
from app.modules.society.assistencia_social.domain.models import CadastroUnico

class CadastroUnicoService:

    def __init__(self, *, cadastro_repo: CadastroUnicoRepositoryPort, citizen_service: CitizenServicePort, educacao_service: EducacaoServicePort, juventude_service: JuventudeServicePort, request_service: RequestServicePort | None=None) -> None:
        self.cadastro_repo = cadastro_repo
        self.citizen_service = citizen_service
        self.educacao_service = educacao_service
        self.juventude_service = juventude_service
        self.request_service = request_service

    async def registrar_cadastro(self, *, citizen_id_responsavel: UUID, renda_per_capita: Decimal, composicao_familiar: list[dict], condicoes_moradia: str, acesso_agua: bool, acesso_energia: bool, observacoes: str | None=None) -> tuple[CadastroUnico, list[str], list[str]]:
        if not await self.citizen_service.is_citizen_active(citizen_id_responsavel):
            raise ValueError('Responsavel familiar nao encontrado ou inativo')
        existente = await self.cadastro_repo.get_by_citizen(citizen_id_responsavel)
        if existente is not None:
            raise ValueError('Responsavel ja possui Cadastro Unico ativo')
        codigo = next_codigo('CAD', len(await self.cadastro_repo.list_all()))
        cadastro = CadastroUnico.registrar(codigo=codigo, citizen_id_responsavel=citizen_id_responsavel, renda_per_capita=renda_per_capita, composicao_familiar=composicao_familiar, condicoes_moradia=condicoes_moradia, acesso_agua=acesso_agua, acesso_energia=acesso_energia, observacoes=observacoes)
        saved = await self.cadastro_repo.save(cadastro)
        alertas: list[str] = []
        for membro in composicao_familiar:
            idade = int(membro.get('idade', 0) or 0)
            citizen_id_raw = membro.get('citizen_id')
            citizen_id = UUID(citizen_id_raw) if isinstance(citizen_id_raw, str) else citizen_id_raw
            if citizen_id is None:
                continue
            if 4 <= idade <= 17 and (not await self.educacao_service.is_estudante_ativo(citizen_id)):
                alertas.append(f'CRIANCA_FORA_ESCOLA:{citizen_id}')
            if 15 <= idade <= 29 and await self.juventude_service.is_jovem_em_risco(citizen_id):
                alertas.append(f'JOVEM_EM_RISCO_SOCIAL:{citizen_id}')
        if self.request_service is not None:
            for idx, alerta in enumerate(alertas, start=1):
                await self.request_service.create_request(request_type='ASSISTENCIA_ALERTA_FAMILIAR', entity_id=saved.id, citizen_id=saved.citizen_id_responsavel, numero_processo=f'{saved.codigo}-AL{idx:02d}', metadata={'alerta': alerta})
        return (saved, saved.calcular_programas_elegiveis(), alertas)

    async def buscar_cadastro(self, cadastro_id: UUID) -> CadastroUnico:
        item = await self.cadastro_repo.get_by_id(cadastro_id)
        if item is None:
            raise ValueError('Cadastro Unico nao encontrado')
        return item

    async def listar_cadastros(self) -> list[CadastroUnico]:
        return await self.cadastro_repo.list_all()

    async def remover_cadastro(self, cadastro_id: UUID) -> None:
        if not await self.cadastro_repo.delete(cadastro_id):
            raise ValueError('Cadastro Unico nao encontrado')