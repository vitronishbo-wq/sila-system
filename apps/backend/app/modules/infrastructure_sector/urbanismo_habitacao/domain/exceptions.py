from __future__ import annotations


class UrbanismoHabitacaoError(Exception):
    pass


class AlvaraAlreadyExistsError(UrbanismoHabitacaoError):
    pass

class AlvaraNotFoundError(UrbanismoHabitacaoError):
    pass

class HabiteSeAlreadyExistsError(UrbanismoHabitacaoError):
    pass

class HabiteSeNotFoundError(UrbanismoHabitacaoError):
    pass

class LicencaUrbanisticaAlreadyExistsError(UrbanismoHabitacaoError):
    pass

class LicencaUrbanisticaNotFoundError(UrbanismoHabitacaoError):
    pass

class LoteamentoAlreadyExistsError(UrbanismoHabitacaoError):
    pass

class LoteamentoNotFoundError(UrbanismoHabitacaoError):
    pass

class OperacaoUrbanaAlreadyExistsError(UrbanismoHabitacaoError):
    pass

class OperacaoUrbanaNotFoundError(UrbanismoHabitacaoError):
    pass

class ParcelamentoAlreadyExistsError(UrbanismoHabitacaoError):
    pass

class ParcelamentoNotFoundError(UrbanismoHabitacaoError):
    pass

class PlanoDiretorAlreadyExistsError(UrbanismoHabitacaoError):
    pass

class PlanoDiretorNotFoundError(UrbanismoHabitacaoError):
    pass

class ZoneamentoAlreadyExistsError(UrbanismoHabitacaoError):
    pass

class ZoneamentoNotFoundError(UrbanismoHabitacaoError):
    pass
