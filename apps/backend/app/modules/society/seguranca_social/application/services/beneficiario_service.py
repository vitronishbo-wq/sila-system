from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID
from apps.backend.app.modules.society.seguranca_social.application.ports import BeneficiarioRepositoryPort, CitizenServicePort, EmpregoServicePort, RequestServicePort
from apps.backend.app.modules.society.seguranca_social.domain.enums import EstadoBeneficiario, RegimeSegurancaSocial, TipoBeneficiario
from apps.backend.app.modules.society.seguranca_social.domain.models.beneficiario import Beneficiario
from apps.backend.app.modules.society.seguranca_social.exceptions import BeneficiarioAlreadyExistsError, BeneficiarioNotFoundError, CandidatoEmpregoRequiredError, CitizenNotFoundError

class BeneficiarioService:

    def __init__(self, *, beneficiario_repo: BeneficiarioRepositoryPort, citizen_repo: CitizenServicePort, emprego_service: EmpregoServicePort, request_service: RequestServicePort):
        self.beneficiario_repo = beneficiario_repo
        self.citizen_repo = citizen_repo
        self.emprego_service = emprego_service
        self.request_service = request_service

    async def inscrever_beneficiario(self, *, citizen_id: UUID, tipo: TipoBeneficiario, regime: RegimeSegurancaSocial) -> Beneficiario:
        citizen = await self.citizen_repo.get_citizen(citizen_id)
        if not citizen:
            raise CitizenNotFoundError(f'Cidadao {citizen_id} nao encontrado')
        existente = await self.beneficiario_repo.get_by_citizen(citizen_id)
        if existente and existente.estado != EstadoBeneficiario.CANCELADO:
            raise BeneficiarioAlreadyExistsError('Cidadao ja possui inscricao ativa ou pendente')
        if tipo == TipoBeneficiario.DESEMPREGADO:
            candidato_registrado = await self.emprego_service.is_candidato_registrado(citizen_id)
            if not candidato_registrado:
                raise CandidatoEmpregoRequiredError('Cidadao nao esta registrado como candidato no modulo emprego')
        numero = await self.beneficiario_repo.next_numero_beneficiario(date.today().year)
        beneficiario = Beneficiario.criar(citizen_id=citizen_id, tipo=tipo, regime=regime, numero_beneficiario=numero)
        saved = await self.beneficiario_repo.save(beneficiario)
        await self.request_service.create_request(request_type='inscricao_seguranca_social', entity_id=saved.id, citizen_id=saved.citizen_id, numero_processo=saved.numero_beneficiario, metadata={'tipo': saved.tipo.value, 'regime': saved.regime.value})
        return saved

    async def ativar_beneficiario(self, *, beneficiario_id: UUID) -> Beneficiario:
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if not beneficiario:
            raise BeneficiarioNotFoundError('Beneficiario nao encontrado')
        beneficiario.ativar()
        updated = await self.beneficiario_repo.save(beneficiario)
        await self.request_service.complete_request(entity_id=beneficiario_id, actor_id=updated.citizen_id, metadata={'ativacao_data': date.today().isoformat()})
        return updated

    async def obter_por_id(self, beneficiario_id: UUID) -> Optional[Beneficiario]:
        return await self.beneficiario_repo.get_by_id(beneficiario_id)

    async def listar_beneficiarios(self, *, tipo: Optional[TipoBeneficiario]=None, estado: Optional[EstadoBeneficiario]=None, regime: Optional[RegimeSegurancaSocial]=None) -> list[Beneficiario]:
        return await self.beneficiario_repo.list_by_filtros(tipo=tipo, estado=estado, regime=regime)