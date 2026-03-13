from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.resources.ambiente.application.ports import CARRepositoryPort, LicencaRepositoryPort
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusCAR, StatusLicenca, TipoLicenca
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_ambiental import LicencaAmbiental
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_instalacao import LicencaInstalacao
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_operacao import LicencaOperacao
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_previa import LicencaPrevia
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_unica import LicencaUnica
from apps.backend.app.modules.resources.ambiente.exceptions import CARNotFoundError, LicencaAlreadyExistsError, LicencaNotFoundError

class LicenciamentoService:

    def __init__(self, *, car_repo: CARRepositoryPort, licenca_repo: LicencaRepositoryPort) -> None:
        self._car_repo = car_repo
        self._licenca_repo = licenca_repo

    async def requerer_licenca(self, *, numero_car: str, tipo: TipoLicenca, atividade: str) -> LicencaAmbiental:
        car = await self._car_repo.get_by_numero(numero_car)
        if not car:
            raise CARNotFoundError('CAR nao encontrado')
        if car.status != StatusCAR.CADASTRADO:
            raise ValueError('CAR precisa estar cadastrado para requerer licenca')
        existentes = await self._licenca_repo.list(numero_car=numero_car, tipo=tipo)
        ativos = {StatusLicenca.REQUERIDA, StatusLicenca.EM_ANALISE, StatusLicenca.DEFERIDA, StatusLicenca.SUSPENSA}
        if any((item.status in ativos for item in existentes)):
            raise LicencaAlreadyExistsError('Ja existe licenca ativa para este CAR e tipo')
        item = self._criar_licenca(numero_car=numero_car, tipo=tipo, atividade=atividade)
        item.numero_licenca = await self._licenca_repo.next_numero()
        return await self._licenca_repo.save(item)

    async def iniciar_analise(self, numero_licenca: str) -> LicencaAmbiental:
        item = await self._licenca_repo.get_by_numero(numero_licenca)
        if not item:
            raise LicencaNotFoundError('Licenca ambiental nao encontrada')
        item.iniciar_analise()
        return await self._licenca_repo.save(item)

    async def deferir(self, numero_licenca: str, *, analista_id: UUID, data_validade: date, condicionantes: list[str] | None=None) -> LicencaAmbiental:
        item = await self._licenca_repo.get_by_numero(numero_licenca)
        if not item:
            raise LicencaNotFoundError('Licenca ambiental nao encontrada')
        item.deferir(analista_id=analista_id, data_validade=data_validade, condicionantes=condicionantes)
        return await self._licenca_repo.save(item)

    async def indeferir(self, numero_licenca: str, *, analista_id: UUID, motivo: str) -> LicencaAmbiental:
        item = await self._licenca_repo.get_by_numero(numero_licenca)
        if not item:
            raise LicencaNotFoundError('Licenca ambiental nao encontrada')
        item.indeferir(analista_id=analista_id, motivo=motivo)
        return await self._licenca_repo.save(item)

    async def suspender(self, numero_licenca: str, *, motivo: str) -> LicencaAmbiental:
        item = await self._licenca_repo.get_by_numero(numero_licenca)
        if not item:
            raise LicencaNotFoundError('Licenca ambiental nao encontrada')
        item.suspender(motivo=motivo)
        return await self._licenca_repo.save(item)

    async def cancelar(self, numero_licenca: str, *, motivo: str) -> LicencaAmbiental:
        item = await self._licenca_repo.get_by_numero(numero_licenca)
        if not item:
            raise LicencaNotFoundError('Licenca ambiental nao encontrada')
        item.cancelar(motivo=motivo)
        return await self._licenca_repo.save(item)

    async def obter_por_numero(self, numero_licenca: str) -> LicencaAmbiental:
        item = await self._licenca_repo.get_by_numero(numero_licenca)
        if not item:
            raise LicencaNotFoundError('Licenca ambiental nao encontrada')
        return item

    async def listar(self, *, numero_car: str | None=None, tipo: TipoLicenca | None=None, status: StatusLicenca | None=None) -> list[LicencaAmbiental]:
        return await self._licenca_repo.list(numero_car=numero_car, tipo=tipo, status=status)

    def _criar_licenca(self, *, numero_car: str, tipo: TipoLicenca, atividade: str) -> LicencaAmbiental:
        if tipo == TipoLicenca.PREVIA:
            return LicencaPrevia.requerer(numero_car=numero_car, atividade=atividade)
        if tipo == TipoLicenca.INSTALACAO:
            return LicencaInstalacao.requerer(numero_car=numero_car, atividade=atividade)
        if tipo == TipoLicenca.OPERACAO:
            return LicencaOperacao.requerer(numero_car=numero_car, atividade=atividade)
        if tipo == TipoLicenca.UNICA:
            return LicencaUnica.requerer(numero_car=numero_car, atividade=atividade)
        return LicencaAmbiental.criar(numero_car=numero_car, tipo=tipo, atividade=atividade)