"""Aggregate Root: Taxpayer (Contribuinte Fiscal)"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from ..aggregate_entities import TaxCertificate, TaxDebt, TaxDeclaration, TaxPayment
from ..enums.tax_regime import TaxRegime
from ..enums.taxpayer_status import TaxpayerStatus
from ..value_objects.nif import NIF


@dataclass
class Taxpayer:
    """
    AGGREGATE ROOT: Taxpayer

    Representa um contribuinte (pessoa física ou jurídica) no sistema SILA.

    This is the boundary for transactional consistency:
    - Todas operações de contribuinte passam por aqui
    - Todas entidades relacionadas (declarations, debts, etc) devem estar aqui
    - Repositório NÃO tem operações diretas em declarações, débitos, etc

    Invariantes de Domínio:
    - Um NIF é único no sistema
    - Um contribuinte não pode ter 2 declarations no mesmo período
    - Débitos não podem ser negativos
    - Status deve seguir transições válidas

    Ver: AGGREGATE_ROOT.md para documentação completa
    """

    id: UUID = field(default_factory=uuid4)
    nif: str = ""
    name: str = ""
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    tax_regime: str = TaxRegime.GERAL.value
    tenant_id: UUID = field(default_factory=uuid4)
    citizen_id: UUID | None = None
    status: TaxpayerStatus = TaxpayerStatus.DRAFT
    addresses: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    emails: list[str] = field(default_factory=list)
    declarations: list[TaxDeclaration] = field(default_factory=list)
    debts: list[TaxDebt] = field(default_factory=list)
    payments: list[TaxPayment] = field(default_factory=list)
    certificates: list[TaxCertificate] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: UUID | None = None
    updated_at: datetime | None = None
    updated_by: UUID | None = None
    version: int = 1
    metadata: dict = field(default_factory=dict)
    domain_events: list[Any] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        """Valida o agregado na criação."""
        self.validate()

    def validate(self) -> None:
        """
        Valida as invariantes do Aggregate Root.

        Raises:
            ValueError: Se alguma invariante é violada
        """
        try:
            NIF(self.nif)
        except ValueError as e:
            raise ValueError(f"NIF inválido para contribuinte: {e}") from e
        if not self.name or len(self.name.strip()) < 3:
            raise ValueError("Nome do contribuinte deve ter pelo menos 3 caracteres")
        periods_seen = set()
        for declaration in self.declarations:
            period_key = f"{declaration.tax_type}:{declaration.tax_period}"
            if period_key in periods_seen:
                raise ValueError(f"Não pode haver 2 declarações para o mesmo período: {period_key}")
            periods_seen.add(period_key)
            declaration.validate()
        for debt in self.debts:
            debt.validate()
        for payment in self.payments:
            payment.validate()
        for certificate in self.certificates:
            certificate.validate()

    def activate(self) -> None:
        """Ativa o contribuinte."""
        if self.status == TaxpayerStatus.ACTIVE:
            raise ValueError("Contribuinte já está ativo")
        self.status = TaxpayerStatus.ACTIVE
        self._mark_modified()

    def suspend(self) -> None:
        """Suspende o contribuinte."""
        if self.status == TaxpayerStatus.SUSPENDED:
            raise ValueError("Contribuinte já está suspenso")
        self.status = TaxpayerStatus.SUSPENDED
        self._mark_modified()

    def deactivate(self) -> None:
        """Desativa o contribuinte."""
        if self.status not in [TaxpayerStatus.ACTIVE, TaxpayerStatus.SUSPENDED]:
            raise ValueError("Contribuinte não pode ser desativado neste estado")
        self.status = TaxpayerStatus.DRAFT
        self._mark_modified()

    def update_personal_data(
        self,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        updated_by: UUID | None = None,
    ) -> None:
        """Atualiza dados pessoais do contribuinte."""
        if name and name.strip():
            self.name = name.strip()
        if email:
            self.email = email
        if phone:
            self.phone = phone
        if address:
            self.address = address
        self._mark_modified(updated_by)

    def set_tax_regime(self, regime: str, updated_by: UUID | None = None) -> None:
        """Define o regime fiscal."""
        valid_regimes = [r.value for r in TaxRegime]
        if regime not in valid_regimes:
            raise ValueError(f"Regime fiscal inválido: {regime}")
        self.tax_regime = regime
        self._mark_modified(updated_by)

    def add_declaration(self, declaration: TaxDeclaration) -> None:
        """
        Adiciona declaração fiscal ao contribuinte.

        Valida as invariantes antes de adicionar.
        """
        declaration.validate()
        period_key = f"{declaration.tax_type}:{declaration.tax_period}"
        for existing in self.declarations:
            if f"{existing.tax_type}:{existing.tax_period}" == period_key:
                raise ValueError(f"Declaração já existe para o período: {period_key}")
        self.declarations.append(declaration)
        self._mark_modified()

    def get_declaration_by_number(self, number: str) -> TaxDeclaration | None:
        """Busca declaração por número."""
        for declaration in self.declarations:
            if declaration.declaration_number == number:
                return declaration
        return None

    def get_declarations_by_period(self, tax_period: str) -> list[TaxDeclaration]:
        """Retorna todas as declarações para um período fiscalspecífico."""
        return [d for d in self.declarations if d.tax_period == tax_period]

    def update_declaration_status(
        self, declaration_number: str, new_status: str, updated_by: UUID | None = None
    ) -> TaxDeclaration:
        """Atualiza o status de uma declaração."""
        declaration = self.get_declaration_by_number(declaration_number)
        if not declaration:
            raise ValueError(f"Declaração não encontrada: {declaration_number}")
        declaration.status = new_status
        declaration.mark_updated(updated_by)
        self._mark_modified(updated_by)
        return declaration

    def add_debt(self, debt: TaxDebt) -> None:
        """
        Adiciona débito fiscal ao contribuinte.

        Valida as invariantes antes de adicionar.
        """
        debt.validate()
        self.debts.append(debt)
        self._mark_modified()

    def get_debt_by_number(self, number: str) -> TaxDebt | None:
        """Busca débito por número."""
        for debt in self.debts:
            if debt.debt_number == number:
                return debt
        return None

    def get_open_debts(self) -> list[TaxDebt]:
        """Retorna todos os débitos em aberto."""
        return [d for d in self.debts if d.status == "OPEN"]

    def get_total_debt_amount(self) -> float:
        """Retorna o valor total de todos os débitos em aberto."""
        return sum(d.total_amount for d in self.get_open_debts())

    def resolve_debt(self, debt_number: str, updated_by: UUID | None = None) -> TaxDebt:
        """Marca um débito como resolvido."""
        debt = self.get_debt_by_number(debt_number)
        if not debt:
            raise ValueError(f"Débito não encontrado: {debt_number}")
        debt.status = "RESOLVED"
        debt.mark_updated(updated_by)
        self._mark_modified(updated_by)
        return debt

    def add_payment(self, payment: TaxPayment) -> None:
        """
        Adiciona pagamento ao contribuinte.

        Valida as invariantes antes de adicionar.
        """
        payment.validate()
        self.payments.append(payment)
        self._mark_modified()

    def get_payment_by_number(self, number: str) -> TaxPayment | None:
        """Busca pagamento por número."""
        for payment in self.payments:
            if payment.payment_number == number:
                return payment
        return None

    def get_confirmed_payments(self) -> list[TaxPayment]:
        """Retorna todos os pagamentos confirmados."""
        return [p for p in self.payments if p.status == "CONFIRMED"]

    def get_total_paid_amount(self) -> float:
        """Retorna o valor total de pagamentos confirmados."""
        return sum(p.amount for p in self.get_confirmed_payments())

    def update_payment_status(
        self, payment_number: str, new_status: str, updated_by: UUID | None = None
    ) -> TaxPayment:
        """Atualiza o status de um pagamento."""
        payment = self.get_payment_by_number(payment_number)
        if not payment:
            raise ValueError(f"Pagamento não encontrado: {payment_number}")
        payment.status = new_status
        payment.mark_updated(updated_by)
        self._mark_modified(updated_by)
        return payment

    def add_certificate(self, certificate: TaxCertificate) -> None:
        """
        Adiciona certidão ao contribuinte.

        Valida as invariantes antes de adicionar.
        """
        certificate.validate()
        self.certificates.append(certificate)
        self._mark_modified()

    def get_certificate_by_number(self, number: str) -> TaxCertificate | None:
        """Busca certidão por número."""
        for cert in self.certificates:
            if cert.certificate_number == number:
                return cert
        return None

    def get_valid_certificates(self) -> list[TaxCertificate]:
        """Retorna todas as certidões válidas."""
        now = datetime.utcnow()
        return [c for c in self.certificates if c.is_valid_at(now)]

    def add_event(self, event: Any) -> None:
        """Adiciona um domain evento ao agregado."""
        self.domain_events.append(event)

    def get_events(self) -> list[Any]:
        """Retorna todos os eventos não publicados."""
        return self.domain_events.copy()

    def clear_events(self) -> None:
        """Limpa os eventos após publicação."""
        self.domain_events.clear()

    def _mark_modified(self, by: UUID | None = None) -> None:
        """Marca o agregado como modificado."""
        self.updated_at = datetime.utcnow()
        self.updated_by = by
        self.version += 1

    def to_dict(self) -> dict[str, Any]:
        """Serializa o agregado completo."""
        return {
            "id": str(self.id),
            "nif": self.nif,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "tax_regime": self.tax_regime,
            "tenant_id": str(self.tenant_id),
            "citizen_id": str(self.citizen_id) if self.citizen_id else None,
            "status": self.status.value,
            "addresses": self.addresses,
            "phones": self.phones,
            "emails": self.emails,
            "declarations": [d.to_dict() for d in self.declarations],
            "debts": [d.to_dict() for d in self.debts],
            "payments": [p.to_dict() for p in self.payments],
            "certificates": [c.to_dict() for c in self.certificates],
            "created_at": self.created_at.isoformat(),
            "created_by": str(self.created_by) if self.created_by else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": str(self.updated_by) if self.updated_by else None,
            "version": self.version,
            "metadata": self.metadata,
        }
