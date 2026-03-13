"""Excecoes do modulo urbanismo e habitacao."""

class UrbanismoHabitacaoError(Exception):
    """Erro base do modulo."""

class PlanoDiretorNotFoundError(UrbanismoHabitacaoError):
    """Plano diretor nao encontrado."""

class PlanoDiretorAlreadyExistsError(UrbanismoHabitacaoError):
    """Ja existe plano diretor com o mesmo codigo."""

class ZoneamentoNotFoundError(UrbanismoHabitacaoError):
    """Zoneamento nao encontrado."""

class ZoneamentoAlreadyExistsError(UrbanismoHabitacaoError):
    """Ja existe zoneamento com o mesmo codigo."""

class OperacaoUrbanaNotFoundError(UrbanismoHabitacaoError):
    """Operacao urbana nao encontrada."""

class OperacaoUrbanaAlreadyExistsError(UrbanismoHabitacaoError):
    """Ja existe operacao urbana com o mesmo codigo."""

class ParcelamentoNotFoundError(UrbanismoHabitacaoError):
    """Parcelamento nao encontrado."""

class ParcelamentoAlreadyExistsError(UrbanismoHabitacaoError):
    """Ja existe parcelamento com o mesmo codigo."""

class LoteamentoNotFoundError(UrbanismoHabitacaoError):
    """Loteamento nao encontrado."""

class LoteamentoAlreadyExistsError(UrbanismoHabitacaoError):
    """Ja existe loteamento com o mesmo codigo."""

class LicencaUrbanisticaNotFoundError(UrbanismoHabitacaoError):
    """Licenca urbanistica nao encontrada."""

class LicencaUrbanisticaAlreadyExistsError(UrbanismoHabitacaoError):
    """Ja existe licenca urbanistica com o mesmo codigo."""

class AlvaraNotFoundError(UrbanismoHabitacaoError):
    """Alvara nao encontrado."""

class AlvaraAlreadyExistsError(UrbanismoHabitacaoError):
    """Ja existe alvara com o mesmo codigo."""

class HabiteSeNotFoundError(UrbanismoHabitacaoError):
    """Habite-se nao encontrado."""

class HabiteSeAlreadyExistsError(UrbanismoHabitacaoError):
    """Ja existe habite-se com o mesmo codigo."""