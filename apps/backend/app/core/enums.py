from enum import StrEnum


class StatusMatricula(StrEnum):
    ATIVA = "ativa"
    INATIVA = "inativa"
    CANCELADA = "cancelada"
    PENDENTE = "pendente"


class StatusGeral(StrEnum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    DELETADO = "deletado"


__all__ = ["StatusMatricula", "StatusGeral"]
