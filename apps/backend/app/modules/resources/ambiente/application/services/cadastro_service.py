from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.ambiente.application.ports import CARRepositoryPort, ImovelRepositoryPort, ProprietarioRepositoryPort
from apps.backend.app.modules.resources.ambiente.domain.enums import Bioma, StatusCAR, TipoImovel
from apps.backend.app.modules.resources.ambiente.domain.models.car import CAR
from apps.backend.app.modules.resources.ambiente.domain.models.imovel_rural import ImovelRural
from apps.backend.app.modules.resources.ambiente.domain.models.proprietario import Proprietario
from apps.backend.app.modules.resources.ambiente.exceptions import CARAlreadyExistsError, CARNotFoundError, ImovelNotFoundError, ProprietarioAlreadyExistsError, ProprietarioNotFoundError

class CadastroService:

    def __init__(self, *, proprietario_repo: ProprietarioRepositoryPort, imovel_repo: ImovelRepositoryPort, car_repo: CARRepositoryPort) -> None:
        self._proprietario_repo = proprietario_repo
        self._imovel_repo = imovel_repo
        self._car_repo = car_repo

    async def cadastrar_proprietario(self, *, nome: str, documento: str, telefone: str | None=None, email: str | None=None) -> Proprietario:
        existente = await self._proprietario_repo.get_by_documento(documento)
        if existente:
            raise ProprietarioAlreadyExistsError('Ja existe proprietario para este documento')
        item = Proprietario.criar(nome=nome, documento=documento, telefone=telefone, email=email)
        item.codigo_proprietario = await self._proprietario_repo.next_codigo()
        return await self._proprietario_repo.save(item)

    async def cadastrar_imovel(self, *, proprietario_id: UUID, nome: str, provincia: str, municipio: str, area_total: Decimal, bioma: Bioma, tipo_imovel: TipoImovel, coordenadas: str | None=None) -> ImovelRural:
        proprietario = await self._proprietario_repo.get_by_id(proprietario_id)
        if not proprietario:
            raise ProprietarioNotFoundError('Proprietario nao encontrado')
        item = ImovelRural.criar(proprietario_id=proprietario_id, nome=nome, provincia=provincia, municipio=municipio, area_total=area_total, bioma=bioma, tipo_imovel=tipo_imovel, coordenadas=coordenadas)
        item.codigo_imovel = await self._imovel_repo.next_codigo()
        return await self._imovel_repo.save(item)

    async def criar_car(self, *, imovel_id: UUID, proprietario_id: UUID, area_total: Decimal, bioma: Bioma, tipo_imovel: TipoImovel) -> CAR:
        proprietario = await self._proprietario_repo.get_by_id(proprietario_id)
        if not proprietario:
            raise ProprietarioNotFoundError('Proprietario nao encontrado')
        imovel = await self._imovel_repo.get_by_id(imovel_id)
        if not imovel:
            raise ImovelNotFoundError('Imovel rural nao encontrado')
        if imovel.proprietario_id != proprietario_id:
            raise ValueError('Imovel nao pertence ao proprietario informado')
        existente = await self._car_repo.get_by_imovel(imovel_id)
        if existente:
            raise CARAlreadyExistsError('Ja existe CAR para este imovel')
        car = CAR.criar(imovel_id=imovel_id, proprietario_id=proprietario_id, area_total=area_total, bioma=bioma, tipo_imovel=tipo_imovel)
        car.numero_car = await self._car_repo.next_numero()
        return await self._car_repo.save(car)

    async def atualizar_areas(self, *, numero_car: str, area_preservacao_permanente: Decimal, area_reserva_legal: Decimal, area_uso_alternativo: Decimal, area_consolidada: Decimal) -> CAR:
        car = await self._car_repo.get_by_numero(numero_car)
        if not car:
            raise CARNotFoundError('CAR nao encontrado')
        car.definir_areas(area_preservacao_permanente=area_preservacao_permanente, area_reserva_legal=area_reserva_legal, area_uso_alternativo=area_uso_alternativo, area_consolidada=area_consolidada)
        return await self._car_repo.save(car)

    async def submeter_para_analise(self, numero_car: str) -> CAR:
        car = await self._car_repo.get_by_numero(numero_car)
        if not car:
            raise CARNotFoundError('CAR nao encontrado')
        car.submeter_para_analise()
        return await self._car_repo.save(car)

    async def aprovar(self, numero_car: str, analista_id: UUID) -> CAR:
        car = await self._car_repo.get_by_numero(numero_car)
        if not car:
            raise CARNotFoundError('CAR nao encontrado')
        car.aprovar(analista_id)
        return await self._car_repo.save(car)

    async def solicitar_pendencia(self, numero_car: str, motivo: str, analista_id: UUID) -> CAR:
        car = await self._car_repo.get_by_numero(numero_car)
        if not car:
            raise CARNotFoundError('CAR nao encontrado')
        car.solicitar_pendencia(motivo, analista_id)
        return await self._car_repo.save(car)

    async def obter_por_numero(self, numero_car: str) -> CAR:
        car = await self._car_repo.get_by_numero(numero_car)
        if not car:
            raise CARNotFoundError('CAR nao encontrado')
        return car

    async def listar(self, status: StatusCAR | None=None) -> list[CAR]:
        return await self._car_repo.list_by_status(status=status)