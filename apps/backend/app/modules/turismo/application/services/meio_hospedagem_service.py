from __future__ import annotations

from uuid import UUID

from app.modules.turismo.application.ports.citizen_service_port import CitizenServicePort
from app.modules.turismo.application.ports.hotel_repository_port import HotelRepositoryPort
from app.modules.turismo.application.ports.pousada_repository_port import PousadaRepositoryPort
from app.modules.turismo.application.ports.request_service_port import RequestServicePort
from app.modules.turismo.domain.enums import ClassificacaoHoteleira, TipoMeioHospedagem
from app.modules.turismo.domain.models.hotel import Hotel
from app.modules.turismo.domain.models.pousada import Pousada


class MeioHospedagemService:
    def __init__(
        self,
        *,
        hotel_repo: HotelRepositoryPort,
        pousada_repo: PousadaRepositoryPort | None = None,
        citizen_service: CitizenServicePort,
        request_service: RequestServicePort | None = None,
        estabelecimento_repo: object | None = None,
    ) -> None:
        self.hotel_repo = hotel_repo
        self.pousada_repo = pousada_repo
        self.citizen_service = citizen_service
        self.request_service = request_service
        self.estabelecimento_repo = estabelecimento_repo

    async def cadastrar_hotel(
        self,
        *,
        nome: str,
        tipo: TipoMeioHospedagem,
        classificacao: ClassificacaoHoteleira,
        cnpj: str,
        endereco: str,
        numero: str,
        bairro: str,
        municipio: str,
        provincia: str,
        cep: str,
        telefone: str,
        email: str,
        quartos: int,
        capacidade_maxima: int,
        proprietario_id: UUID,
    ) -> Hotel:
        proprietario_ativo = await self.citizen_service.is_citizen_active(proprietario_id)
        if not proprietario_ativo:
            raise ValueError("Proprietario nao encontrado ou inativo")

        existente = await self.hotel_repo.get_by_cnpj(cnpj)
        if existente:
            raise ValueError("Hotel ja cadastrado com este CNPJ")

        cadastur = await self.hotel_repo.next_cadastur(provincia.strip().upper())
        hotel = Hotel.cadastrar(
            nome=nome,
            tipo=tipo,
            classificacao=classificacao,
            cnpj=cnpj,
            endereco=endereco,
            numero=numero,
            bairro=bairro,
            municipio=municipio,
            provincia=provincia,
            cep=cep,
            telefone=telefone,
            email=email,
            quartos=quartos,
            capacidade_maxima=capacidade_maxima,
            proprietario_id=proprietario_id,
        )
        hotel.cadastur = cadastur
        saved = await self.hotel_repo.save(hotel)

        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_HOTEL",
                entity_id=saved.id,
                citizen_id=proprietario_id,
                numero_processo=saved.cadastur,
                metadata={
                    "nome": saved.nome,
                    "cadastur": saved.cadastur,
                    "tipo": saved.tipo.value,
                    "classificacao": saved.classificacao.value,
                    "municipio": saved.municipio,
                },
            )

        return saved

    async def buscar_hotel(self, hotel_id: UUID) -> Hotel:
        hotel = await self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            raise ValueError("Hotel nao encontrado")
        return hotel

    async def listar_hoteis(self, municipio: str | None = None) -> list[Hotel]:
        if municipio:
            return await self.hotel_repo.list_by_municipio(municipio)
        return await self.hotel_repo.list_all()

    async def listar_hoteis_por_classificacao(
        self, classificacao: ClassificacaoHoteleira
    ) -> list[Hotel]:
        return await self.hotel_repo.list_by_classificacao(classificacao)

    async def cadastrar_pousada(
        self,
        *,
        nome: str,
        classificacao: ClassificacaoHoteleira,
        cnpj: str,
        endereco: str,
        numero: str,
        bairro: str,
        municipio: str,
        provincia: str,
        cep: str,
        telefone: str,
        email: str,
        quartos: int,
        capacidade_maxima: int,
        proprietario_id: UUID,
    ) -> Pousada:
        if self.pousada_repo is None:
            raise ValueError("Repositorio de pousada nao configurado")

        proprietario_ativo = await self.citizen_service.is_citizen_active(proprietario_id)
        if not proprietario_ativo:
            raise ValueError("Proprietario nao encontrado ou inativo")

        existente = await self.pousada_repo.get_by_cnpj(cnpj)
        if existente:
            raise ValueError("Pousada ja cadastrada com este CNPJ")

        cadastur = await self.pousada_repo.next_cadastur(provincia.strip().upper())
        pousada = Pousada.cadastrar(
            nome=nome,
            classificacao=classificacao,
            cnpj=cnpj,
            endereco=endereco,
            numero=numero,
            bairro=bairro,
            municipio=municipio,
            provincia=provincia,
            cep=cep,
            telefone=telefone,
            email=email,
            quartos=quartos,
            capacidade_maxima=capacidade_maxima,
            proprietario_id=proprietario_id,
        )
        pousada.cadastur = cadastur
        return await self.pousada_repo.save(pousada)

    async def buscar_pousada(self, pousada_id: UUID) -> Pousada:
        if self.pousada_repo is None:
            raise ValueError("Repositorio de pousada nao configurado")
        pousada = await self.pousada_repo.get_by_id(pousada_id)
        if not pousada:
            raise ValueError("Pousada nao encontrada")
        return pousada

    async def listar_pousadas(
        self,
        *,
        municipio: str | None = None,
        classificacao: ClassificacaoHoteleira | None = None,
        ativa: bool | None = None,
    ) -> list[Pousada]:
        if self.pousada_repo is None:
            raise ValueError("Repositorio de pousada nao configurado")
        return await self.pousada_repo.list(
            municipio=municipio,
            classificacao=classificacao,
            ativa=ativa,
        )

    async def atualizar_pousada(
        self,
        pousada_id: UUID,
        *,
        nome: str | None = None,
        endereco: str | None = None,
        numero: str | None = None,
        bairro: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        cep: str | None = None,
        telefone: str | None = None,
        email: str | None = None,
        site: str | None = None,
        observacoes: str | None = None,
        classificacao: ClassificacaoHoteleira | None = None,
        ativa: bool | None = None,
    ) -> Pousada:
        pousada = await self.buscar_pousada(pousada_id)
        pousada.atualizar_dados(
            nome=nome,
            endereco=endereco,
            numero=numero,
            bairro=bairro,
            municipio=municipio,
            provincia=provincia,
            cep=cep,
            telefone=telefone,
            email=email,
            site=site,
            observacoes=observacoes,
            classificacao=classificacao,
        )
        if ativa is True:
            pousada.ativar()
        if ativa is False:
            pousada.desativar()
        return await self.pousada_repo.save(pousada)

    async def remover_pousada(self, pousada_id: UUID) -> None:
        if self.pousada_repo is None:
            raise ValueError("Repositorio de pousada nao configurado")
        deleted = await self.pousada_repo.delete(pousada_id)
        if not deleted:
            raise ValueError("Pousada nao encontrada")


HotelService = MeioHospedagemService
