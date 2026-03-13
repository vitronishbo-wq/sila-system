"""Excecoes do modulo agricultura."""

class AgriculturaError(Exception):
    """Erro base do modulo."""

class ProdutorNotFoundError(AgriculturaError):
    """Produtor nao encontrado."""

class ProdutorAlreadyExistsError(AgriculturaError):
    """Produtor com documento ja cadastrado."""

class PropriedadeNotFoundError(AgriculturaError):
    """Propriedade nao encontrada."""

class CulturaNotFoundError(AgriculturaError):
    """Cultura nao encontrada."""

class SafraNotFoundError(AgriculturaError):
    """Safra nao encontrada."""

class InsumoNotFoundError(AgriculturaError):
    """Insumo nao encontrado."""

class EstoqueNotFoundError(AgriculturaError):
    """Controle de estoque nao encontrado."""

class OperacaoNotFoundError(AgriculturaError):
    """Operacao nao encontrada."""

class OcorrenciaNotFoundError(AgriculturaError):
    """Ocorrencia fitossanitaria nao encontrada."""

class CertificacaoNotFoundError(AgriculturaError):
    """Certificacao nao encontrada."""

class ComercializacaoNotFoundError(AgriculturaError):
    """Comercializacao nao encontrada."""

class CreditoNotFoundError(AgriculturaError):
    """Credito rural nao encontrado."""

class AssistenciaNotFoundError(AgriculturaError):
    """Assistencia tecnica nao encontrada."""

class ZoneamentoNotFoundError(AgriculturaError):
    """Zoneamento nao encontrado."""

class CadastroAmbientalNotFoundError(AgriculturaError):
    """Cadastro ambiental nao encontrado."""

class TalhaoNotFoundError(AgriculturaError):
    """Talhao nao encontrado."""

class PlantioNotFoundError(AgriculturaError):
    """Plantio nao encontrado."""

class ColheitaNotFoundError(AgriculturaError):
    """Colheita nao encontrada."""

class EquipamentoNotFoundError(AgriculturaError):
    """Equipamento nao encontrado."""

class CitizenInactiveError(AgriculturaError):
    """Cidadao informado nao existe ou esta inativo."""