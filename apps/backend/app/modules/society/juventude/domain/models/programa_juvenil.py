from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.juventude.domain.enums import StatusPrograma, TipoPrograma


@dataclass
class ProgramaJuvenil:
    id: UUID
    codigo_programa: str
    nome: str
    tipo: TipoPrograma
    data_inicio: date
    data_cadastro: date
    data_fim: date | None = None
    vagas: int | None = None
    municipio: str | None = None
    provincia: str | None = None
    status: StatusPrograma = StatusPrograma.PLANEADO
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def criar(
        cls,
        *,
        codigo_programa: str,
        nome: str,
        tipo: TipoPrograma,
        data_inicio: date,
        data_fim: date | None = None,
        vagas: int | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        observacoes: str | None = None,
    ) -> ProgramaJuvenil:
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError("Nome do programa deve ter pelo menos 3 caracteres")
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError("Data fim do programa deve ser maior ou igual a data inicio")
        if vagas is not None and vagas <= 0:
            raise ValueError("Vagas deve ser maior que zero")
        return cls(
            id=uuid4(),
            codigo_programa=codigo_programa.strip(),
            nome=nome_normalizado,
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            vagas=vagas,
            municipio=municipio.strip() if municipio else None,
            provincia=provincia.strip() if provincia else None,
            data_cadastro=date.today(),
            status=StatusPrograma.PLANEADO,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusPrograma) -> None:
        self.status = status
        self.ativo = status not in {StatusPrograma.CANCELADO, StatusPrograma.CONCLUIDO}
