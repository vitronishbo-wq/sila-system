from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.public_security.domain.enums import StatusLaudo, TipoLaudo


@dataclass
class LaudoPericial:
    id: UUID
    numero_laudo: str
    prova_id: UUID
    tipo_laudo: TipoLaudo
    perito_id: UUID
    data_emissao: date
    conclusao: str
    status: StatusLaudo
    resumo: str | None = None
    arquivo_url: str | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def emitir(
        cls,
        *,
        numero_laudo: str,
        prova_id: UUID,
        tipo_laudo: TipoLaudo,
        perito_id: UUID,
        conclusao: str,
        resumo: str | None = None,
        arquivo_url: str | None = None,
        observacoes: str | None = None,
    ) -> LaudoPericial:
        if len(conclusao.strip()) < 10:
            raise ValueError("Conclusao do laudo deve ter pelo menos 10 caracteres")
        return cls(
            id=uuid4(),
            numero_laudo=numero_laudo.strip(),
            prova_id=prova_id,
            tipo_laudo=tipo_laudo,
            perito_id=perito_id,
            data_emissao=date.today(),
            conclusao=conclusao.strip(),
            status=StatusLaudo.EMITIDO,
            resumo=resumo.strip() if resumo else None,
            arquivo_url=arquivo_url.strip() if arquivo_url else None,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusLaudo, observacoes: str | None = None) -> None:
        self.status = status
        self.ativo = status not in {StatusLaudo.CANCELADO}
        if observacoes:
            self.observacoes = observacoes.strip()
