from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.desporto.domain.enums import EstadoRelvado, TipoEstadio


@dataclass
class Estadio:
    id: UUID
    codigo_estadio: str
    nome: str
    tipo: TipoEstadio
    municipio: str
    provincia: str
    capacidade: int
    estado_relvado: EstadoRelvado
    data_cadastro: date
    codigo_obra_instalacao: str | None = None
    clube_mandante_id: UUID | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        codigo_estadio: str,
        nome: str,
        tipo: TipoEstadio,
        municipio: str,
        provincia: str,
        capacidade: int,
        estado_relvado: EstadoRelvado,
        codigo_obra_instalacao: str | None = None,
        clube_mandante_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Estadio:
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError("Nome do estadio deve ter pelo menos 3 caracteres")
        if capacidade <= 0:
            raise ValueError("Capacidade do estadio deve ser positiva")
        return cls(
            id=uuid4(),
            codigo_estadio=codigo_estadio.strip(),
            nome=nome_normalizado,
            tipo=tipo,
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            capacidade=capacidade,
            estado_relvado=estado_relvado,
            data_cadastro=date.today(),
            codigo_obra_instalacao=codigo_obra_instalacao.strip()
            if codigo_obra_instalacao
            else None,
            clube_mandante_id=clube_mandante_id,
            observacoes=observacoes.strip() if observacoes else None,
        )

    def atualizar(
        self,
        *,
        nome: str | None = None,
        tipo: TipoEstadio | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        capacidade: int | None = None,
        estado_relvado: EstadoRelvado | None = None,
        codigo_obra_instalacao: str | None = None,
        clube_mandante_id: UUID | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> None:
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError("Nome do estadio deve ter pelo menos 3 caracteres")
            self.nome = nome_normalizado
        if tipo is not None:
            self.tipo = tipo
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if capacidade is not None:
            if capacidade <= 0:
                raise ValueError("Capacidade do estadio deve ser positiva")
            self.capacidade = capacidade
        if estado_relvado is not None:
            self.estado_relvado = estado_relvado
        if codigo_obra_instalacao is not None:
            self.codigo_obra_instalacao = (
                codigo_obra_instalacao.strip() if codigo_obra_instalacao else None
            )
        if clube_mandante_id is not None:
            self.clube_mandante_id = clube_mandante_id
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None
