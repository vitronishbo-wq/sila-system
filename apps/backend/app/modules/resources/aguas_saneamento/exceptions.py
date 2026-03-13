"""Excecoes do modulo aguas e saneamento."""

class AguasSaneamentoError(Exception):
    """Erro base do modulo."""

class OutorgaNotFoundError(AguasSaneamentoError):
    """Outorga nao encontrada."""

class OutorgaAlreadyExistsError(AguasSaneamentoError):
    """Ja existe outorga ativa para os mesmos dados base."""

class InfraestruturaNotFoundError(AguasSaneamentoError):
    """Infraestrutura nao encontrada."""

class InfraestruturaAlreadyExistsError(AguasSaneamentoError):
    """Ja existe infraestrutura equivalente registrada."""

class AbastecimentoNotFoundError(AguasSaneamentoError):
    """Abastecimento nao encontrado."""

class AbastecimentoAlreadyExistsError(AguasSaneamentoError):
    """Ja existe abastecimento equivalente registrado."""

class ConsumoNotFoundError(AguasSaneamentoError):
    """Consumo nao encontrado."""

class ConsumoAlreadyExistsError(AguasSaneamentoError):
    """Ja existe consumo registrado para os mesmos dados base."""

class FaturaNotFoundError(AguasSaneamentoError):
    """Fatura nao encontrada."""

class FaturaAlreadyExistsError(AguasSaneamentoError):
    """Ja existe fatura ativa para o mesmo consumo e referencia."""