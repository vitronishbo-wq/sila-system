from enum import Enum

class StatusMatricula(str, Enum):
    ATIVA = 'ativa'
    INATIVA = 'inativa'
    CANCELADA = 'cancelada'
    PENDENTE = 'pendente'

class StatusGeral(str, Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    DELETADO = 'deletado'
__all__ = ['StatusMatricula', 'StatusGeral']