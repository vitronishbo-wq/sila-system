from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4
from app.modules.governance.cooperacao_internacional.domain.enums import NaturezaJuridica, StatusAcordo, TipoAcordo

@dataclass
class Acordo:
    titulo: str
    tipo: TipoAcordo
    natureza: NaturezaJuridica
    data_assinatura: date
    objeto: str
    data_vigor: date | None = None
    prazo_anos: int | None = None
    fundamento_legal: str | None = None
    texto_integral: str | None = None
    id: UUID = field(default_factory=uuid4)
    numero_registro: str = ''
    status: StatusAcordo = StatusAcordo.NEGOCIACAO
    partes: list[dict] = field(default_factory=list)
    ratificacoes: list[dict] = field(default_factory=list)
    emendas: list[dict] = field(default_factory=list)
    denuncias: list[dict] = field(default_factory=list)
    data_registro: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        self.numero_registro = self.numero_registro or self._gerar_numero_registro()
        self.titulo = self.titulo.strip()
        if not self.titulo:
            raise ValueError('Titulo do acordo obrigatorio')

    def _gerar_numero_registro(self) -> str:
        return f'INT{datetime.utcnow().year}{uuid4().hex[:8].upper()}'

    def adicionar_parte(self, *, entidade_id: UUID, tipo_entidade: str, data_adesao: date, assinante: str, titulo_assinante: str) -> None:
        self.partes.append({'id': str(uuid4()), 'entidade_id': str(entidade_id), 'tipo_entidade': tipo_entidade, 'data_adesao': data_adesao.isoformat(), 'assinante': assinante, 'titulo_assinante': titulo_assinante})

    def assinar(self) -> None:
        if not self.partes:
            raise ValueError('Nao e possivel assinar acordo sem partes')
        self.status = StatusAcordo.ASSINADO

    def ratificar(self, *, parte_id: UUID, data_ratificacao: date, instrumento: str) -> None:
        self.ratificacoes.append({'parte_id': str(parte_id), 'data_ratificacao': data_ratificacao.isoformat(), 'instrumento': instrumento})
        if self.partes and len(self.ratificacoes) >= len(self.partes):
            self.status = StatusAcordo.RATIFICADO

    def iniciar_vigor(self, data_vigor: date) -> None:
        self.data_vigor = data_vigor
        self.status = StatusAcordo.EM_VIGOR

    def denunciar(self, *, parte_id: UUID, data_denuncia: date, motivo: str) -> None:
        self.denuncias.append({'parte_id': str(parte_id), 'data_denuncia': data_denuncia.isoformat(), 'motivo': motivo})
        if self.partes and len(self.denuncias) >= len(self.partes):
            self.status = StatusAcordo.EXTINTO

    def vigencia_restante_dias(self) -> int | None:
        if self.data_vigor is None or self.prazo_anos is None:
            return None
        fim = date(self.data_vigor.year + self.prazo_anos, self.data_vigor.month, self.data_vigor.day)
        if date.today() >= fim:
            return 0
        return (fim - date.today()).days