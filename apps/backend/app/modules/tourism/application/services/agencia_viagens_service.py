from __future__ import annotations
from uuid import UUID
from app.modules.tourism.application.ports.agencia_viagens_repository_port import AgenciaViagensRepositoryPort
from app.modules.tourism.application.ports.citizen_service_port import CitizenServicePort
from app.modules.tourism.application.ports.comercio_servicos_service_port import ComercioServicosServicePort
from app.modules.tourism.application.ports.request_service_port import RequestServicePort
from app.modules.tourism.domain.models.agencia_viagens import AgenciaViagens

class AgenciaViagensService:

    def __init__(self, *, repository: AgenciaViagensRepositoryPort, citizen_service: CitizenServicePort, comercio_service: ComercioServicosServicePort | None=None, request_service: RequestServicePort | None=None) -> None:
        self.repository = repository
        self.citizen_service = citizen_service
        self.comercio_service = comercio_service
        self.request_service = request_service

    async def cadastrar(self, *, nome_fantasia: str, razao_social: str, cnpj: str, email: str, telefone: str, endereco: str, numero: str, bairro: str, municipio: str, provincia: str, cep: str, proprietario_id: UUID, especialidades: list[str] | None=None, site: str | None=None, observacoes: str | None=None) -> AgenciaViagens:
        proprietario_ativo = await self.citizen_service.is_citizen_active(proprietario_id)
        if not proprietario_ativo:
            raise ValueError('Proprietario nao encontrado ou inativo')
        existente = await self.repository.get_by_cnpj(cnpj)
        if existente:
            raise ValueError('Agencia ja cadastrada com este CNPJ')
        if self.comercio_service is not None:
            cnpj_ativo = await self.comercio_service.agencia_cnpj_ativo(cnpj=cnpj)
            if not cnpj_ativo:
                raise ValueError('CNPJ sem conformidade no cadastro comercial')
        agencia = AgenciaViagens.cadastrar(nome_fantasia=nome_fantasia, razao_social=razao_social, cnpj=cnpj, email=email, telefone=telefone, endereco=endereco, numero=numero, bairro=bairro, municipio=municipio, provincia=provincia, cep=cep, proprietario_id=proprietario_id, especialidades=especialidades, site=site, observacoes=observacoes)
        agencia.registro = await self.repository.next_registro(provincia)
        saved = await self.repository.save(agencia)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_AGENCIA_VIAGENS', entity_id=saved.id, citizen_id=proprietario_id, numero_processo=saved.registro, metadata={'nome_fantasia': saved.nome_fantasia, 'cnpj': saved.cnpj, 'municipio': saved.municipio})
        return saved

    async def obter(self, agencia_id: UUID) -> AgenciaViagens:
        agencia = await self.repository.get_by_id(agencia_id)
        if not agencia:
            raise ValueError('Agencia de viagens nao encontrada')
        return agencia

    async def listar(self, *, municipio: str | None=None, ativa: bool | None=None) -> list[AgenciaViagens]:
        return await self.repository.list(municipio=municipio, ativa=ativa)

    async def atualizar(self, agencia_id: UUID, *, nome_fantasia: str | None=None, razao_social: str | None=None, email: str | None=None, telefone: str | None=None, endereco: str | None=None, numero: str | None=None, bairro: str | None=None, municipio: str | None=None, provincia: str | None=None, cep: str | None=None, especialidades: list[str] | None=None, site: str | None=None, observacoes: str | None=None, ativa: bool | None=None) -> AgenciaViagens:
        agencia = await self.obter(agencia_id)
        agencia.atualizar(nome_fantasia=nome_fantasia, razao_social=razao_social, email=email, telefone=telefone, endereco=endereco, numero=numero, bairro=bairro, municipio=municipio, provincia=provincia, cep=cep, especialidades=especialidades, site=site, observacoes=observacoes)
        if ativa is True:
            agencia.ativar()
        if ativa is False:
            agencia.desativar()
        return await self.repository.save(agencia)

    async def remover(self, agencia_id: UUID) -> None:
        deleted = await self.repository.delete(agencia_id)
        if not deleted:
            raise ValueError('Agencia de viagens nao encontrada')
