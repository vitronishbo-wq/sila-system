from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.logistics.domain.enums import StatusFrota
from apps.backend.app.modules.logistics.domain.models.fiscalizacao_transporte import FiscalizacaoTransporte
from apps.backend.app.modules.logistics.domain.models.manutencao import Manutencao
from apps.backend.app.modules.logistics.domain.models.tarifa import Tarifa

@dataclass
class Frota:
    id: UUID
    codigo_frota: str
    nome: str
    operadora_id: UUID
    municipio: str
    provincia: str
    status: StatusFrota
    data_cadastro: date
    data_atualizacao: date | None = None
    observacoes: str | None = None
    veiculos: list[dict] = field(default_factory=list)
    manutencoes: list[dict] = field(default_factory=list)
    fiscalizacoes: list[dict] = field(default_factory=list)
    tarifas: list[dict] = field(default_factory=list)
    trilha_auditoria: list[dict] = field(default_factory=list)

    @classmethod
    def criar(cls, *, codigo_frota: str, nome: str, operadora_id: UUID, municipio: str, provincia: str, observacoes: str | None=None) -> 'Frota':
        if not codigo_frota.strip():
            raise ValueError('Codigo da frota e obrigatorio')
        if not nome.strip():
            raise ValueError('Nome da frota e obrigatorio')
        if not municipio.strip() or not provincia.strip():
            raise ValueError('Municipio e provincia sao obrigatorios')
        return cls(id=uuid4(), codigo_frota=codigo_frota.strip(), nome=nome.strip(), operadora_id=operadora_id, municipio=municipio.strip(), provincia=provincia.strip(), status=StatusFrota.ATIVA, data_cadastro=date.today(), observacoes=observacoes.strip() if observacoes else None)

    def adicionar_veiculo(self, *, veiculo_id: UUID, placa: str, tipo: str, capacidade: int | None=None) -> None:
        if self.status != StatusFrota.ATIVA:
            raise ValueError('Frota precisa estar ativa para adicionar veiculo')
        if not placa.strip():
            raise ValueError('Placa do veiculo e obrigatoria')
        if any((item.get('placa') == placa.strip().upper() for item in self.veiculos)):
            raise ValueError('Veiculo ja cadastrado na frota')
        self.veiculos.append({'veiculo_id': str(veiculo_id), 'placa': placa.strip().upper(), 'tipo': tipo.strip().lower(), 'capacidade': capacidade, 'data_vinculo': date.today().isoformat()})
        self.data_atualizacao = date.today()

    def registrar_manutencao(self, manutencao: Manutencao) -> None:
        self.manutencoes.append(manutencao.to_dict())
        self.data_atualizacao = date.today()

    def atualizar_tarifa(self, tarifa: Tarifa) -> None:
        self.tarifas.append(tarifa.to_dict())
        self.data_atualizacao = date.today()

    def registrar_fiscalizacao(self, fiscalizacao: FiscalizacaoTransporte) -> None:
        self.fiscalizacoes.append(fiscalizacao.to_dict())
        if not fiscalizacao.conformidade:
            self.status = StatusFrota.SUSPENSA
        self.data_atualizacao = date.today()

    def custo_total_manutencao(self) -> Decimal:
        total = Decimal('0')
        for item in self.manutencoes:
            total += Decimal(item['custo'])
        return total.quantize(Decimal('0.01'))

    def registrar_evento_auditoria(self, *, evento: str, payload: dict | None=None) -> None:
        self.trilha_auditoria.append({'data': date.today().isoformat(), 'evento': evento, 'payload': payload or {}})
        self.data_atualizacao = date.today()