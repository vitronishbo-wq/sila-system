from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.governance.cooperacao_internacional.application.events import AcordoAssinadoEvent, AcordoRatificadoEvent, AcordoVigorEvent, event_bus
from apps.backend.app.modules.governance.cooperacao_internacional.application.ports.acordo_repository_port import AcordoRepositoryPort
from apps.backend.app.modules.governance.cooperacao_internacional.domain.enums import NaturezaJuridica, TipoAcordo
from apps.backend.app.modules.governance.cooperacao_internacional.domain.models.acordo import Acordo
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.adapters.mre_adapter import MREAdapter
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.adapters.onu_adapter import ONUAdapter
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.persistence.outbox import InMemoryOutbox

class AcordoService:

    def __init__(self, *, acordo_repo: AcordoRepositoryPort, outbox: InMemoryOutbox, mre_adapter: MREAdapter | None=None, onu_adapter: ONUAdapter | None=None) -> None:
        self.acordo_repo = acordo_repo
        self.outbox = outbox
        self.mre = mre_adapter
        self.onu = onu_adapter

    async def criar_acordo(self, *, titulo: str, tipo: TipoAcordo, natureza: NaturezaJuridica, data_assinatura: date, data_vigor: date | None, prazo_anos: int | None, objeto: str, fundamento_legal: str | None=None, texto_integral: str | None=None) -> Acordo:
        acordo = Acordo(titulo=titulo, tipo=tipo, natureza=natureza, data_assinatura=data_assinatura, data_vigor=data_vigor, prazo_anos=prazo_anos, objeto=objeto, fundamento_legal=fundamento_legal, texto_integral=texto_integral)
        await self.acordo_repo.save(acordo)
        if self.mre is not None:
            await self.mre.registrar_acordo({'numero': acordo.numero_registro, 'titulo': acordo.titulo, 'tipo': acordo.tipo.value, 'data_assinatura': acordo.data_assinatura.isoformat()})
        return acordo

    async def assinar_acordo(self, *, acordo_id: UUID, partes: list[dict], local_assinatura: str) -> Acordo:
        acordo = await self.acordo_repo.get_by_id(acordo_id)
        if acordo is None:
            raise ValueError('Acordo nao encontrado')
        for parte in partes:
            acordo.adicionar_parte(entidade_id=parte['entidade_id'], tipo_entidade=parte['tipo_entidade'], data_adesao=parte['data_adesao'], assinante=parte['assinante'], titulo_assinante=parte['titulo_assinante'])
        acordo.assinar()
        await self.acordo_repo.save(acordo)
        evento = AcordoAssinadoEvent(acordo_id=acordo.id, numero_registro=acordo.numero_registro, titulo=acordo.titulo, tipo=acordo.tipo.value, partes=[str(item['entidade_id']) for item in partes])
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        if self.mre is not None:
            await self.mre.registrar_assinatura(numero_acordo=acordo.numero_registro, data_assinatura=acordo.data_assinatura, local=local_assinatura, partes=len(partes))
        return acordo

    async def ratificar_acordo(self, *, acordo_id: UUID, data_ratificacao: date, instrumento: str, parte_id: UUID) -> Acordo:
        acordo = await self.acordo_repo.get_by_id(acordo_id)
        if acordo is None:
            raise ValueError('Acordo nao encontrado')
        acordo.ratificar(parte_id=parte_id, data_ratificacao=data_ratificacao, instrumento=instrumento)
        await self.acordo_repo.save(acordo)
        evento = AcordoRatificadoEvent(acordo_id=acordo.id, numero_registro=acordo.numero_registro, instrumento_ratificacao=instrumento)
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        return acordo

    async def iniciar_vigor(self, *, acordo_id: UUID, data_vigor: date) -> Acordo:
        acordo = await self.acordo_repo.get_by_id(acordo_id)
        if acordo is None:
            raise ValueError('Acordo nao encontrado')
        acordo.iniciar_vigor(data_vigor)
        await self.acordo_repo.save(acordo)
        evento = AcordoVigorEvent(acordo_id=acordo.id, numero_registro=acordo.numero_registro, prazo_anos=acordo.prazo_anos)
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        if self.onu is not None and acordo.tipo == TipoAcordo.TRATADO:
            await self.onu.registrar_tratado({'numero': acordo.numero_registro, 'titulo': acordo.titulo, 'data_vigor': data_vigor.isoformat(), 'partes': len(acordo.partes)})
        return acordo

    async def listar_acordos(self) -> list[Acordo]:
        return await self.acordo_repo.list_all()

    async def get_acordos_vencimento_proximo(self, dias: int=90) -> list[dict]:
        acordos = await self.acordo_repo.find_em_vigor()
        resultado: list[dict] = []
        for acordo in acordos:
            restante = acordo.vigencia_restante_dias()
            if restante is not None and restante <= dias:
                resultado.append({'acordo_id': str(acordo.id), 'numero_registro': acordo.numero_registro, 'dias_restantes': restante, 'acao_recomendada': 'RENOVAR' if restante < 30 else 'MONITORAR'})
        return resultado