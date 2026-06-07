from __future__ import annotations


class AgriculturaError(Exception):
    pass


class AssistenciaNotFoundError(AgriculturaError):
    pass

class CadastroAmbientalNotFoundError(AgriculturaError):
    pass

class CertificacaoNotFoundError(AgriculturaError):
    pass

class CitizenInactiveError(AgriculturaError):
    pass

class ColheitaNotFoundError(AgriculturaError):
    pass

class ComercializacaoNotFoundError(AgriculturaError):
    pass

class CreditoNotFoundError(AgriculturaError):
    pass

class CulturaNotFoundError(AgriculturaError):
    pass

class EquipamentoNotFoundError(AgriculturaError):
    pass

class EstoqueNotFoundError(AgriculturaError):
    pass

class InsumoNotFoundError(AgriculturaError):
    pass

class OcorrenciaNotFoundError(AgriculturaError):
    pass

class OperacaoNotFoundError(AgriculturaError):
    pass

class PlantioNotFoundError(AgriculturaError):
    pass

class ProdutorAlreadyExistsError(AgriculturaError):
    pass

class ProdutorNotFoundError(AgriculturaError):
    pass

class PropriedadeNotFoundError(AgriculturaError):
    pass

class SafraNotFoundError(AgriculturaError):
    pass

class TalhaoNotFoundError(AgriculturaError):
    pass

class ZoneamentoNotFoundError(AgriculturaError):
    pass
