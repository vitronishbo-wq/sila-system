from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.tourism.application.ports.atracao_turistica_repository_port import (
    AtracaoTuristicaRepositoryPort,
)
from apps.backend.app.modules.tourism.domain.enums import TipoAtracao
from apps.backend.app.modules.tourism.domain.models.atracao_turistica import AtracaoTuristica


class AtracaoService:
    def __init__(self, *, repository: AtracaoTuristicaRepositoryPort):
        self.repository = repository

    async def cadastrar(
        self,
        *,
        nome: str,
        tipo: TipoAtracao,
        descricao: str,
        endereco: str,
        municipio: str,
        provincia: str,
        horario_funcionamento: str,
        acessivel: bool,
        gratuita: bool = False,
        capacidade_visitantes_dia: int | None = None,
        valor_entrada: Decimal | None = None,
        latitude: Decimal | None = None,
        longitude: Decimal | None = None,
        observacoes: str | None = None,
    ) -> AtracaoTuristica:
        atracao = AtracaoTuristica.cadastrar(
            nome=nome,
            tipo=tipo,
            descricao=descricao,
            endereco=endereco,
            municipio=municipio,
            provincia=provincia,
            horario_funcionamento=horario_funcionamento,
            acessivel=acessivel,
            gratuita=gratuita,
            capacidade_visitantes_dia=capacidade_visitantes_dia,
            valor_entrada=valor_entrada,
            latitude=latitude,
            longitude=longitude,
            observacoes=observacoes,
        )
        atracao.codigo = await self.repository.next_codigo(provincia.strip().upper())
        return await self.repository.save(atracao)

    async def obter(self, atracao_id: UUID) -> AtracaoTuristica:
        atracao = await self.repository.get_by_id(atracao_id)
        if not atracao:
            raise ValueError("Atracao turistica nao encontrada")
        return atracao

    async def listar(
        self,
        *,
        tipo: TipoAtracao | None = None,
        municipio: str | None = None,
        ativa: bool | None = None,
    ) -> list[AtracaoTuristica]:
        return await self.repository.list(tipo=tipo, municipio=municipio, ativa=ativa)

    async def atualizar(
        self,
        atracao_id: UUID,
        *,
        nome: str | None = None,
        tipo: TipoAtracao | None = None,
        descricao: str | None = None,
        endereco: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        horario_funcionamento: str | None = None,
        acessivel: bool | None = None,
        gratuita: bool | None = None,
        capacidade_visitantes_dia: int | None = None,
        valor_entrada: Decimal | None = None,
        latitude: Decimal | None = None,
        longitude: Decimal | None = None,
        observacoes: str | None = None,
        ativa: bool | None = None,
    ) -> AtracaoTuristica:
        atracao = await self.obter(atracao_id)
        atracao.atualizar(
            nome=nome,
            tipo=tipo,
            descricao=descricao,
            endereco=endereco,
            municipio=municipio,
            provincia=provincia,
            horario_funcionamento=horario_funcionamento,
            acessivel=acessivel,
            gratuita=gratuita,
            capacidade_visitantes_dia=capacidade_visitantes_dia,
            valor_entrada=valor_entrada,
            latitude=latitude,
            longitude=longitude,
            observacoes=observacoes,
        )
        if ativa is True:
            atracao.ativar()
        if ativa is False:
            atracao.desativar()
        return await self.repository.save(atracao)

    async def remover(self, atracao_id: UUID) -> None:
        deleted = await self.repository.delete(atracao_id)
        if not deleted:
            raise ValueError("Atracao turistica nao encontrada")
