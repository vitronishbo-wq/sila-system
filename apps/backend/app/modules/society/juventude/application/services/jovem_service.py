from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.society.juventude.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.society.juventude.application.ports.educacao_service_port import (
    EducacaoServicePort,
)
from apps.backend.app.modules.society.juventude.application.ports.emprego_service_port import (
    EmpregoServicePort,
)
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import (
    JovemRepositoryPort,
)
from apps.backend.app.modules.society.juventude.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.juventude.domain.enums import (
    Escolaridade,
    FaixaEtaria,
    SituacaoOcupacional,
    TipoVulnerabilidade,
)
from apps.backend.app.modules.society.juventude.domain.models.jovem import Jovem


class JovemService:
    def __init__(
        self,
        *,
        jovem_repo: JovemRepositoryPort,
        citizen_service: CitizenServicePort | None = None,
        educacao_service: EducacaoServicePort | None = None,
        emprego_service: EmpregoServicePort | None = None,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.jovem_repo = jovem_repo
        self.citizen_service = citizen_service
        self.educacao_service = educacao_service
        self.emprego_service = emprego_service
        self.request_service = request_service

    async def cadastrar_jovem(
        self,
        *,
        nome: str,
        data_nascimento: date,
        genero: str,
        naturalidade: str,
        escolaridade: Escolaridade,
        situacao_ocupacional: SituacaoOcupacional,
        endereco: str,
        municipio: str,
        provincia: str,
        nacionalidade: str = "Angolana",
        telefone: str | None = None,
        email: str | None = None,
        citizen_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Jovem:
        if citizen_id is not None and self.citizen_service is not None:
            if not await self.citizen_service.is_citizen_active(citizen_id):
                raise ValueError("Cidadao nao encontrado ou inativo")
        if (
            citizen_id is not None
            and self.educacao_service is not None
            and (
                situacao_ocupacional
                in {SituacaoOcupacional.ESTUDA, SituacaoOcupacional.ESTUDA_TRABALHA}
            )
        ):
            possui_matricula = await self.educacao_service.has_matricula_ativa(citizen_id)
            if not possui_matricula:
                raise ValueError("Jovem declarou estudo ativo sem matricula valida")
        if (
            citizen_id is not None
            and self.emprego_service is not None
            and (
                situacao_ocupacional
                in {
                    SituacaoOcupacional.TRABALHA,
                    SituacaoOcupacional.PROCURA_EMPREGO,
                    SituacaoOcupacional.ESTUDA_TRABALHA,
                }
            )
        ):
            await self.emprego_service.has_candidatura_ativa(citizen_id)
        registro = await self.jovem_repo.next_registro()
        jovem = Jovem.cadastrar(
            numero_registro=registro,
            nome=nome,
            data_nascimento=data_nascimento,
            genero=genero,
            naturalidade=naturalidade,
            escolaridade=escolaridade,
            situacao_ocupacional=situacao_ocupacional,
            endereco=endereco,
            municipio=municipio,
            provincia=provincia,
            nacionalidade=nacionalidade,
            telefone=telefone,
            email=email,
            citizen_id=citizen_id,
            observacoes=observacoes,
        )
        saved = await self.jovem_repo.save(jovem)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_JOVEM",
                entity_id=saved.id,
                citizen_id=citizen_id,
                numero_processo=saved.numero_registro,
                metadata={
                    "registro": saved.numero_registro,
                    "nome": saved.nome,
                    "faixa_etaria": saved.faixa_etaria.value,
                    "escolaridade": saved.escolaridade.value,
                    "situacao_ocupacional": saved.situacao_ocupacional.value,
                },
            )
        return saved

    async def buscar_jovem(self, jovem_id: UUID) -> Jovem:
        jovem = await self.jovem_repo.get_by_id(jovem_id)
        if jovem is None:
            raise ValueError("Jovem nao encontrado")
        return jovem

    async def listar_jovens(
        self,
        *,
        faixa_etaria: FaixaEtaria | None = None,
        escolaridade: Escolaridade | None = None,
        situacao: SituacaoOcupacional | None = None,
        municipio: str | None = None,
        vulneravel: bool | None = None,
    ) -> list[Jovem]:
        if faixa_etaria is not None:
            return await self.jovem_repo.list_by_faixa_etaria(faixa_etaria)
        if escolaridade is not None:
            return await self.jovem_repo.list_by_escolaridade(escolaridade)
        if situacao is not None:
            return await self.jovem_repo.list_by_situacao(situacao)
        if municipio:
            return await self.jovem_repo.list_by_municipio(municipio)
        if vulneravel:
            return await self.jovem_repo.list_vulneraveis()
        return await self.jovem_repo.list_all()

    async def atualizar_jovem(
        self,
        *,
        jovem_id: UUID,
        escolaridade: Escolaridade | None = None,
        situacao_ocupacional: SituacaoOcupacional | None = None,
        telefone: str | None = None,
        email: str | None = None,
        endereco: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        observacoes: str | None = None,
        ativo: bool | None = None,
    ) -> Jovem:
        jovem = await self.buscar_jovem(jovem_id)
        if escolaridade is not None:
            jovem.atualizar_escolaridade(escolaridade)
        if situacao_ocupacional is not None:
            jovem.atualizar_situacao_ocupacional(situacao_ocupacional)
        if telefone is not None or email is not None:
            jovem.atualizar_contato(telefone=telefone, email=email)
        if endereco is not None:
            jovem.endereco = endereco.strip()
        if municipio is not None:
            jovem.municipio = municipio.strip()
        if provincia is not None:
            jovem.provincia = provincia.strip()
        if observacoes is not None:
            jovem.observacoes = observacoes.strip() or None
        if ativo is not None:
            jovem.ativo = ativo
        return await self.jovem_repo.save(jovem)

    async def adicionar_vulnerabilidade(
        self, *, jovem_id: UUID, vulnerabilidade: TipoVulnerabilidade
    ) -> Jovem:
        jovem = await self.buscar_jovem(jovem_id)
        jovem.adicionar_vulnerabilidade(vulnerabilidade)
        return await self.jovem_repo.save(jovem)

    async def remover_jovem(self, jovem_id: UUID) -> None:
        deleted = await self.jovem_repo.delete(jovem_id)
        if not deleted:
            raise ValueError("Jovem nao encontrado")
