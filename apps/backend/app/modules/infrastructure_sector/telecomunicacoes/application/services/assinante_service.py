from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.assinante_repository_port import AssinanteRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.citizen_service_port import CitizenServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import OperadoraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusAssinante, TipoPlano, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.assinante import Assinante

class AssinanteService:

    def __init__(self, *, assinante_repo: AssinanteRepositoryPort, operadora_repo: OperadoraRepositoryPort, citizen_service: CitizenServicePort | None=None, request_service: RequestServicePort | None=None) -> None:
        self.assinante_repo = assinante_repo
        self.operadora_repo = operadora_repo
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def cadastrar_assinante(self, *, operadora_id: UUID, tipo_plano: TipoPlano, servico_principal: TipoServico, municipio: str, provincia: str, nome: str | None=None, citizen_id: UUID | None=None, telefone_contato: str | None=None, email_contato: str | None=None, contrato_numero: str | None=None, valor_mensal: float | None=None, observacoes: str | None=None) -> Assinante:
        operadora = await self.operadora_repo.get_by_id(operadora_id)
        if operadora is None:
            raise ValueError('Operadora nao encontrada para cadastro do assinante')
        if servico_principal not in operadora.servicos_autorizados:
            raise ValueError('Servico informado nao esta autorizado para a operadora')
        if citizen_id is not None and self.citizen_service is not None:
            if not await self.citizen_service.is_citizen_active(citizen_id):
                raise ValueError('Cidadao nao encontrado ou inativo')
            existente = await self.assinante_repo.get_by_citizen(citizen_id)
            if existente is not None and existente.ativo:
                raise ValueError('Cidadao ja possui assinante ativo')
        codigo = await self.assinante_repo.next_codigo()
        assinante = Assinante.cadastrar(codigo_assinante=codigo, operadora_id=operadora_id, tipo_plano=tipo_plano, servico_principal=servico_principal, municipio=municipio, provincia=provincia, nome=nome, citizen_id=citizen_id, telefone_contato=telefone_contato, email_contato=email_contato, contrato_numero=contrato_numero, valor_mensal=valor_mensal, observacoes=observacoes)
        saved = await self.assinante_repo.save(assinante)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_ASSINANTE_TELECOM', entity_id=saved.id, citizen_id=saved.citizen_id, numero_processo=saved.codigo_assinante, metadata={'codigo_assinante': saved.codigo_assinante, 'operadora_id': str(saved.operadora_id), 'servico_principal': saved.servico_principal.value, 'tipo_plano': saved.tipo_plano.value})
        return saved

    async def buscar_assinante(self, assinante_id: UUID) -> Assinante:
        assinante = await self.assinante_repo.get_by_id(assinante_id)
        if assinante is None:
            raise ValueError('Assinante nao encontrado')
        return assinante

    async def listar_assinantes(self, *, operadora_id: UUID | None=None, municipio: str | None=None, somente_ativos: bool=True) -> list[Assinante]:
        if operadora_id is not None:
            return await self.assinante_repo.list_by_operadora(operadora_id)
        if municipio:
            return await self.assinante_repo.list_by_municipio(municipio)
        if somente_ativos:
            return await self.assinante_repo.list_ativos()
        return await self.assinante_repo.list_all()

    async def atualizar_status(self, *, assinante_id: UUID, status: StatusAssinante) -> Assinante:
        assinante = await self.buscar_assinante(assinante_id)
        assinante.atualizar_status(status)
        return await self.assinante_repo.save(assinante)

    async def remover_assinante(self, assinante_id: UUID) -> None:
        deleted = await self.assinante_repo.delete(assinante_id)
        if not deleted:
            raise ValueError('Assinante nao encontrado')