from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from apps.backend.app.modules.society.seguranca_social.application.ports import BeneficiarioRepositoryPort, PensaoRepositoryPort, RequestServicePort
from apps.backend.app.modules.society.seguranca_social.domain.enums import EstadoBeneficiario, StatusPensao, TipoPensao
from apps.backend.app.modules.society.seguranca_social.domain.models.pensao import Pensao
from apps.backend.app.modules.society.seguranca_social.exceptions import BeneficiarioNotEligibleError, BeneficiarioNotFoundError, PensaoAlreadyExistsError, PensaoNotFoundError

class PensaoService:

    def __init__(self, *, pensao_repo: PensaoRepositoryPort, beneficiario_repo: BeneficiarioRepositoryPort, request_service: RequestServicePort):
        self.pensao_repo = pensao_repo
        self.beneficiario_repo = beneficiario_repo
        self.request_service = request_service

    async def solicitar_pensao(self, *, beneficiario_id: UUID, tipo: TipoPensao, valor_mensal: Decimal, conta_bancaria: str | None=None, iban: str | None=None) -> Pensao:
        if valor_mensal <= 0:
            raise ValueError('Valor mensal deve ser maior que zero')
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if not beneficiario:
            raise BeneficiarioNotFoundError('Beneficiario nao encontrado')
        if beneficiario.estado != EstadoBeneficiario.ATIVO:
            raise BeneficiarioNotEligibleError('Apenas beneficiarios ativos podem solicitar pensao')
        existentes = await self.pensao_repo.list_by_filtros(beneficiario_id=beneficiario_id, tipo=tipo)
        if any((item.status != StatusPensao.CANCELADA for item in existentes)):
            raise PensaoAlreadyExistsError('Ja existe pensao nao cancelada deste tipo para o beneficiario')
        numero = await self.pensao_repo.next_numero_processo(date.today().year)
        pensao = Pensao.solicitar(beneficiario_id=beneficiario_id, tipo=tipo, valor_mensal=valor_mensal, numero_processo=numero, conta_bancaria=conta_bancaria, iban=iban)
        saved = await self.pensao_repo.save(pensao)
        await self.request_service.create_request(request_type='solicitacao_pensao', entity_id=saved.id, citizen_id=beneficiario.citizen_id, numero_processo=saved.numero_processo, metadata={'tipo': saved.tipo.value, 'status': saved.status.value, 'valor_mensal': str(saved.valor_mensal)})
        return saved

    async def aprovar_pensao(self, *, pensao_id: UUID, actor_id: UUID) -> Pensao:
        pensao = await self._get_or_raise(pensao_id)
        pensao.aprovar()
        updated = await self.pensao_repo.save(pensao)
        await self.request_service.complete_request(entity_id=updated.id, actor_id=actor_id, metadata={'status': updated.status.value})
        return updated

    async def suspender_pensao(self, *, pensao_id: UUID, motivo: str) -> Pensao:
        pensao = await self._get_or_raise(pensao_id)
        pensao.suspender(motivo)
        return await self.pensao_repo.save(pensao)

    async def cancelar_pensao(self, *, pensao_id: UUID, motivo: str) -> Pensao:
        pensao = await self._get_or_raise(pensao_id)
        pensao.cancelar(motivo)
        return await self.pensao_repo.save(pensao)

    async def obter_por_id(self, pensao_id: UUID) -> Optional[Pensao]:
        return await self.pensao_repo.get_by_id(pensao_id)

    async def listar_pensoes(self, *, beneficiario_id: UUID | None=None, tipo: TipoPensao | None=None, status: StatusPensao | None=None) -> list[Pensao]:
        return await self.pensao_repo.list_by_filtros(beneficiario_id=beneficiario_id, tipo=tipo, status=status)

    async def _get_or_raise(self, pensao_id: UUID) -> Pensao:
        pensao = await self.pensao_repo.get_by_id(pensao_id)
        if not pensao:
            raise PensaoNotFoundError('Pensao nao encontrada')
        return pensao