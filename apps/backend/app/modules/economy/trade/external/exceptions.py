"""Excecoes do modulo comercio_externo."""

class ComercioExternoError(Exception):
    """Erro base do modulo."""

class ExportadorNotFoundError(ComercioExternoError):
    """Exportador nao encontrado."""

class ExportadorAlreadyExistsError(ComercioExternoError):
    """Exportador ja cadastrado."""

class InvalidExportadorStateError(ComercioExternoError):
    """Transicao de estado invalida para exportador."""

class ImportadorNotFoundError(ComercioExternoError):
    """Importador nao encontrado."""

class ImportadorAlreadyExistsError(ComercioExternoError):
    """Importador ja cadastrado."""

class InvalidImportadorStateError(ComercioExternoError):
    """Transicao de estado invalida para importador."""

class DespachanteNotFoundError(ComercioExternoError):
    """Despachante nao encontrado."""

class DespachanteAlreadyExistsError(ComercioExternoError):
    """Despachante ja cadastrado."""

class InvalidDespachanteStateError(ComercioExternoError):
    """Transicao de estado invalida para despachante."""

class AgenteCargaNotFoundError(ComercioExternoError):
    """Agente de carga nao encontrado."""

class AgenteCargaAlreadyExistsError(ComercioExternoError):
    """Agente de carga ja cadastrado."""

class InvalidAgenteCargaStateError(ComercioExternoError):
    """Transicao de estado invalida para agente de carga."""

class TransportadorInternacionalNotFoundError(ComercioExternoError):
    """Transportador internacional nao encontrado."""

class TransportadorInternacionalAlreadyExistsError(ComercioExternoError):
    """Transportador internacional ja cadastrado."""

class InvalidTransportadorInternacionalStateError(ComercioExternoError):
    """Transicao de estado invalida para transportador internacional."""

class HabilitacaoExportadorNotFoundError(ComercioExternoError):
    """Habilitacao de exportador nao encontrada."""

class HabilitacaoExportadorAlreadyExistsError(ComercioExternoError):
    """Habilitacao de exportador ja cadastrada."""

class InvalidHabilitacaoExportadorStateError(ComercioExternoError):
    """Transicao de estado invalida para habilitacao de exportador."""

class HabilitacaoImportadorNotFoundError(ComercioExternoError):
    """Habilitacao de importador nao encontrada."""

class HabilitacaoImportadorAlreadyExistsError(ComercioExternoError):
    """Habilitacao de importador ja cadastrada."""

class InvalidHabilitacaoImportadorStateError(ComercioExternoError):
    """Transicao de estado invalida para habilitacao de importador."""

class RadarNotFoundError(ComercioExternoError):
    """Radar nao encontrado."""

class RadarAlreadyExistsError(ComercioExternoError):
    """Radar ja cadastrado."""

class InvalidRadarStateError(ComercioExternoError):
    """Transicao de estado invalida para radar."""

class HabilitacaoRadarNotFoundError(ComercioExternoError):
    """Habilitacao de radar nao encontrada."""

class HabilitacaoRadarAlreadyExistsError(ComercioExternoError):
    """Habilitacao de radar ja cadastrada."""

class InvalidHabilitacaoRadarStateError(ComercioExternoError):
    """Transicao de estado invalida para habilitacao de radar."""

class CancelamentoRadarNotFoundError(ComercioExternoError):
    """Cancelamento de radar nao encontrado."""

class CancelamentoRadarAlreadyExistsError(ComercioExternoError):
    """Cancelamento de radar ja cadastrado."""

class InvalidCancelamentoRadarStateError(ComercioExternoError):
    """Transicao de estado invalida para cancelamento de radar."""

class SuspensaoRadarNotFoundError(ComercioExternoError):
    """Suspensao de radar nao encontrada."""

class SuspensaoRadarAlreadyExistsError(ComercioExternoError):
    """Suspensao de radar ja cadastrada."""

class InvalidSuspensaoRadarStateError(ComercioExternoError):
    """Transicao de estado invalida para suspensao de radar."""

class DrawbackNotFoundError(ComercioExternoError):
    """Drawback nao encontrado."""

class DrawbackAlreadyExistsError(ComercioExternoError):
    """Drawback ja cadastrado."""

class InvalidDrawbackStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback."""

class DrawbackExternoNotFoundError(ComercioExternoError):
    """Drawback externo nao encontrado."""

class DrawbackExternoAlreadyExistsError(ComercioExternoError):
    """Drawback externo ja cadastrado."""

class InvalidDrawbackExternoStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback externo."""

class DrawbackInternoNotFoundError(ComercioExternoError):
    """Drawback interno nao encontrado."""

class DrawbackInternoAlreadyExistsError(ComercioExternoError):
    """Drawback interno ja cadastrado."""

class InvalidDrawbackInternoStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback interno."""

class DrawbackVerdeAmareloNotFoundError(ComercioExternoError):
    """Drawback verde amarelo nao encontrado."""

class DrawbackVerdeAmareloAlreadyExistsError(ComercioExternoError):
    """Drawback verde amarelo ja cadastrado."""

class InvalidDrawbackVerdeAmareloStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback verde amarelo."""

class SiscomexDrawbackNotFoundError(ComercioExternoError):
    """Siscomex drawback nao encontrado."""

class SiscomexDrawbackAlreadyExistsError(ComercioExternoError):
    """Siscomex drawback ja cadastrado."""

class InvalidSiscomexDrawbackStateError(ComercioExternoError):
    """Transicao de estado invalida para siscomex drawback."""

class DrawbackSuspensaoNotFoundError(ComercioExternoError):
    """Drawback suspensao nao encontrado."""

class DrawbackSuspensaoAlreadyExistsError(ComercioExternoError):
    """Drawback suspensao ja cadastrado."""

class InvalidDrawbackSuspensaoStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback suspensao."""

class DrawbackIsencaoNotFoundError(ComercioExternoError):
    """Drawback isencao nao encontrado."""

class DrawbackIsencaoAlreadyExistsError(ComercioExternoError):
    """Drawback isencao ja cadastrado."""

class InvalidDrawbackIsencaoStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback isencao."""

class DrawbackSubstituicaoNotFoundError(ComercioExternoError):
    """Drawback substituicao nao encontrado."""

class DrawbackSubstituicaoAlreadyExistsError(ComercioExternoError):
    """Drawback substituicao ja cadastrado."""

class InvalidDrawbackSubstituicaoStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback substituicao."""

class DrawbackRestituicaoNotFoundError(ComercioExternoError):
    """Drawback restituicao nao encontrado."""

class DrawbackRestituicaoAlreadyExistsError(ComercioExternoError):
    """Drawback restituicao ja cadastrado."""

class InvalidDrawbackRestituicaoStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback restituicao."""

class DrawbackIntegradoNotFoundError(ComercioExternoError):
    """Drawback integrado nao encontrado."""

class DrawbackIntegradoAlreadyExistsError(ComercioExternoError):
    """Drawback integrado ja cadastrado."""

class InvalidDrawbackIntegradoStateError(ComercioExternoError):
    """Transicao de estado invalida para drawback integrado."""