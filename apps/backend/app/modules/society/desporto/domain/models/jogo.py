from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.desporto.domain.enums import StatusJogo


@dataclass
class Jogo:
    id: UUID
    codigo_jogo: str
    competicao_id: UUID
    clube_casa_id: UUID
    clube_fora_id: UUID
    data_jogo: date
    local: str
    municipio: str
    provincia: str
    data_cadastro: date
    status: StatusJogo = StatusJogo.AGENDADO
    placar_casa: int | None = None
    placar_fora: int | None = None
    codigo_obra_instalacao: str | None = None
    atracao_turistica_id: UUID | None = None
    publico_estimado: int | None = None
    publico_presente: int | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def agendar(
        cls,
        *,
        codigo_jogo: str,
        competicao_id: UUID,
        clube_casa_id: UUID,
        clube_fora_id: UUID,
        data_jogo: date,
        local: str,
        municipio: str,
        provincia: str,
        codigo_obra_instalacao: str | None = None,
        atracao_turistica_id: UUID | None = None,
        publico_estimado: int | None = None,
        observacoes: str | None = None,
    ) -> Jogo:
        if clube_casa_id == clube_fora_id:
            raise ValueError("Clubes de casa e fora devem ser diferentes")
        if publico_estimado is not None and publico_estimado < 0:
            raise ValueError("Publico estimado nao pode ser negativo")
        local_normalizado = local.strip()
        if len(local_normalizado) < 3:
            raise ValueError("Local do jogo deve ter pelo menos 3 caracteres")
        return cls(
            id=uuid4(),
            codigo_jogo=codigo_jogo.strip(),
            competicao_id=competicao_id,
            clube_casa_id=clube_casa_id,
            clube_fora_id=clube_fora_id,
            data_jogo=data_jogo,
            local=local_normalizado,
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            data_cadastro=date.today(),
            codigo_obra_instalacao=codigo_obra_instalacao.strip()
            if codigo_obra_instalacao
            else None,
            atracao_turistica_id=atracao_turistica_id,
            publico_estimado=publico_estimado,
            observacoes=observacoes.strip() if observacoes else None,
        )

    def atualizar(
        self,
        *,
        data_jogo: date | None = None,
        local: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        status: StatusJogo | None = None,
        codigo_obra_instalacao: str | None = None,
        atracao_turistica_id: UUID | None = None,
        publico_estimado: int | None = None,
        publico_presente: int | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> None:
        if data_jogo is not None:
            self.data_jogo = data_jogo
        if local is not None:
            local_normalizado = local.strip()
            if len(local_normalizado) < 3:
                raise ValueError("Local do jogo deve ter pelo menos 3 caracteres")
            self.local = local_normalizado
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if status is not None:
            self.status = status
        if codigo_obra_instalacao is not None:
            self.codigo_obra_instalacao = (
                codigo_obra_instalacao.strip() if codigo_obra_instalacao else None
            )
        if atracao_turistica_id is not None:
            self.atracao_turistica_id = atracao_turistica_id
        if publico_estimado is not None:
            if publico_estimado < 0:
                raise ValueError("Publico estimado nao pode ser negativo")
            self.publico_estimado = publico_estimado
        if publico_presente is not None:
            if publico_presente < 0:
                raise ValueError("Publico presente nao pode ser negativo")
            self.publico_presente = publico_presente
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def registrar_resultado(self, *, placar_casa: int, placar_fora: int) -> None:
        if placar_casa < 0 or placar_fora < 0:
            raise ValueError("Placar nao pode ter valor negativo")
        self.placar_casa = placar_casa
        self.placar_fora = placar_fora
        self.status = StatusJogo.ENCERRADO
