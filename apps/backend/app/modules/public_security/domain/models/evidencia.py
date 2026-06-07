from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.public_security.domain.enums import StatusEvidencia, TipoEvidencia


@dataclass
class Evidencia:
    id: UUID
    codigo_evidencia: str
    vestigio_id: UUID
    cadeia_custodia_id: UUID
    tipo: TipoEvidencia
    descricao: str
    fonte: str
    confiabilidade: int
    status: StatusEvidencia
    data_registro: date
    analisado_por_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(
        cls,
        *,
        codigo_evidencia: str,
        vestigio_id: UUID,
        cadeia_custodia_id: UUID,
        tipo: TipoEvidencia,
        descricao: str,
        fonte: str,
        confiabilidade: int = 3,
        analisado_por_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Evidencia:
        if len(descricao.strip()) < 5:
            raise ValueError("Descricao da evidencia deve ter pelo menos 5 caracteres")
        if len(fonte.strip()) < 3:
            raise ValueError("Fonte da evidencia deve ter pelo menos 3 caracteres")
        if confiabilidade < 1 or confiabilidade > 5:
            raise ValueError("Confiabilidade deve estar entre 1 e 5")
        return cls(
            id=uuid4(),
            codigo_evidencia=codigo_evidencia.strip(),
            vestigio_id=vestigio_id,
            cadeia_custodia_id=cadeia_custodia_id,
            tipo=tipo,
            descricao=descricao.strip(),
            fonte=fonte.strip(),
            confiabilidade=confiabilidade,
            status=StatusEvidencia.REGISTRADA,
            data_registro=date.today(),
            analisado_por_id=analisado_por_id,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusEvidencia, observacoes: str | None = None) -> None:
        self.status = status
        self.ativo = status is not StatusEvidencia.INUTILIZADA
        if observacoes:
            self.observacoes = observacoes.strip()
