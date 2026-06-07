from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento


@dataclass
class PessoaComDeficiencia:
    id: UUID
    codigo: str
    beneficiario_id: UUID
    citizen_id_pcd: UUID
    tipo_deficiencia: str
    cid: str
    grau_deficiencia: str
    laudo_id: UUID
    bpc_ativo: bool
    data_registro: datetime
    status: StatusAcompanhamento

    @classmethod
    def registrar(
        cls,
        *,
        codigo: str,
        beneficiario_id: UUID,
        citizen_id_pcd: UUID,
        tipo_deficiencia: str,
        cid: str,
        grau_deficiencia: str,
        laudo_id: UUID,
    ) -> PessoaComDeficiencia:
        return cls(
            id=uuid4(),
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            citizen_id_pcd=citizen_id_pcd,
            tipo_deficiencia=tipo_deficiencia,
            cid=cid,
            grau_deficiencia=grau_deficiencia,
            laudo_id=laudo_id,
            bpc_ativo=False,
            data_registro=datetime.utcnow(),
            status=StatusAcompanhamento.ATIVO,
        )

    def ativar_bpc(self) -> None:
        self.bpc_ativo = True

    def encerrar_acompanhamento(self) -> None:
        self.status = StatusAcompanhamento.ENCERRADO
