from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import OperadoraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import TipoOperadora, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.operadora import Operadora

class OperadoraService:

    def __init__(self, *, operadora_repo: OperadoraRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.operadora_repo = operadora_repo
        self.request_service = request_service

    async def cadastrar_operadora(self, *, cnpj: str, razao_social: str, tipo: TipoOperadora, servicos_autorizados: list[TipoServico], endereco: str, municipio: str, provincia: str, telefone: str, email: str, representante_legal: str, representante_documento: str, representante_cargo: str, nome_fantasia: str | None=None, observacoes: str | None=None) -> Operadora:
        existente = await self.operadora_repo.get_by_cnpj(cnpj)
        if existente is not None:
            raise ValueError('Operadora ja cadastrada com este CNPJ')
        operadora = Operadora.cadastrar(cnpj=cnpj, razao_social=razao_social, tipo=tipo, servicos_autorizados=servicos_autorizados, endereco=endereco, municipio=municipio, provincia=provincia, telefone=telefone, email=email, representante_legal=representante_legal, representante_documento=representante_documento, representante_cargo=representante_cargo, nome_fantasia=nome_fantasia, observacoes=observacoes)
        saved = await self.operadora_repo.save(operadora)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_OPERADORA_TELECOM', entity_id=saved.id, numero_processo=saved.cnpj, metadata={'cnpj': saved.cnpj, 'razao_social': saved.razao_social, 'tipo': saved.tipo.value, 'servicos': [item.value for item in saved.servicos_autorizados]})
        return saved

    async def buscar_operadora(self, operadora_id: UUID) -> Operadora:
        operadora = await self.operadora_repo.get_by_id(operadora_id)
        if operadora is None:
            raise ValueError('Operadora nao encontrada')
        return operadora

    async def listar_operadoras(self, *, servico: TipoServico | None=None, municipio: str | None=None, somente_ativas: bool=False) -> list[Operadora]:
        if servico is not None:
            return await self.operadora_repo.list_by_servico(servico)
        if municipio:
            return await self.operadora_repo.list_by_municipio(municipio)
        if somente_ativas:
            return await self.operadora_repo.list_ativas()
        return await self.operadora_repo.list_all()

    async def autorizar_operadora(self, *, operadora_id: UUID, outorga_id: UUID, data_autorizacao: date, data_validade: date) -> Operadora:
        operadora = await self.buscar_operadora(operadora_id)
        operadora.autorizar(outorga_id=outorga_id, data_autorizacao=data_autorizacao, data_validade=data_validade)
        return await self.operadora_repo.save(operadora)

    async def remover_operadora(self, operadora_id: UUID) -> None:
        deleted = await self.operadora_repo.delete(operadora_id)
        if not deleted:
            raise ValueError('Operadora nao encontrada')