from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.aviacao_civil.domain.enums import FaseVoo, GravidadeOcorrencia, TipoOcorrencia

@dataclass
class Ocorrencia:
    tipo: TipoOcorrencia
    aeronave_id: UUID
    data_ocorrencia: datetime
    local: dict
    fase_voo: FaseVoo
    descricao: str
    vitimas: dict[str, int]
    danos: str
    voo_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    numero_ocorrencia: str = ''
    gravidade: GravidadeOcorrencia = GravidadeOcorrencia.LEVE
    status: str = 'aberta'
    data_registro: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        self.numero_ocorrencia = self.numero_ocorrencia or self._gerar_numero()
        self.gravidade = self._classificar_gravidade()

    def _gerar_numero(self) -> str:
        return f'OC{datetime.utcnow().year}{uuid4().hex[:8].upper()}'

    def _classificar_gravidade(self) -> GravidadeOcorrencia:
        fatais = int(self.vitimas.get('fatais', 0))
        graves = int(self.vitimas.get('graves', 0))
        if fatais > 0:
            return GravidadeOcorrencia.FATAL
        if graves > 0:
            return GravidadeOcorrencia.GRAVE
        if self.danos.upper() in {'SUBSTANCIAL', 'DESTRUIDA'}:
            return GravidadeOcorrencia.MODERADA
        return GravidadeOcorrencia.LEVE

    def encerrar(self) -> None:
        self.status = 'encerrada'