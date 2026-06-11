from enum import Enum

class CanonicalStatus(str, Enum):
    """
    Enum canónico e unificado para o estado do ciclo de vida de todas as
    entidades de domínio no módulo de Educação.

    Esta é a fonte única de verdade para estados, eliminando 'magic strings'
    e Enums duplicados nos modelos de Enrollment, Boletim, Certificado, etc.
    """
    PENDENTE = "PENDENTE"       # O processo foi iniciado, mas aguarda validação ou ação futura.
    ATIVO = "ATIVO"             # A entidade está em curso, válida e operacional.
    SUSPENSO = "SUSPENSO"       # A entidade foi temporariamente pausada, podendo ser retomada.
    CONCLUIDO = "CONCLUIDO"     # O ciclo de vida da entidade terminou com sucesso.
    CANCELADO = "CANCELADO"     # O ciclo de vida foi interrompido e não pode ser retomado.
    TRANSFERIDO = "TRANSFERIDO" # Estado especial indicando que a responsabilidade foi movida para outra entidade (e.g., uma nova matrícula).
