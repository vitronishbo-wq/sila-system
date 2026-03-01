from __future__ import annotations

from uuid import UUID

from app.modules.turismo.application.ports.citizen_service_port import CitizenServicePort
from app.modules.turismo.application.ports.hotel_repository_port import HotelRepositoryPort
from app.modules.turismo.application.ports.request_service_port import RequestServicePort
from app.modules.turismo.domain.enums import ClassificacaoHoteleira, TipoMeioHospedagem
from app.modules.turismo.domain.models.hotel import Hotel


class MeioHospedagemService:
    def __init__(
        self,
        *,
        hotel_repo: HotelRepositoryPort,
        citizen_service: CitizenServicePort,
        request_service: RequestServicePort | None = None,
        estabelecimento_repo: object | None = None,
    ) -> None:
        self.hotel_repo = hotel_repo
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


HotelService = MeioHospedagemService
