from __future__ import annotations


class TradeExternalError(Exception):
    pass


class AgenteCargaAlreadyExistsError(TradeExternalError):
    pass

class AgenteCargaNotFoundError(TradeExternalError):
    pass

class CancelamentoRadarAlreadyExistsError(TradeExternalError):
    pass

class CancelamentoRadarNotFoundError(TradeExternalError):
    pass

class DespachanteAlreadyExistsError(TradeExternalError):
    pass

class DespachanteNotFoundError(TradeExternalError):
    pass

class DrawbackAlreadyExistsError(TradeExternalError):
    pass

class DrawbackExternoAlreadyExistsError(TradeExternalError):
    pass

class DrawbackExternoNotFoundError(TradeExternalError):
    pass

class DrawbackIntegradoAlreadyExistsError(TradeExternalError):
    pass

class DrawbackIntegradoNotFoundError(TradeExternalError):
    pass

class DrawbackInternoAlreadyExistsError(TradeExternalError):
    pass

class DrawbackInternoNotFoundError(TradeExternalError):
    pass

class DrawbackIsencaoAlreadyExistsError(TradeExternalError):
    pass

class DrawbackIsencaoNotFoundError(TradeExternalError):
    pass

class DrawbackNotFoundError(TradeExternalError):
    pass

class DrawbackRestituicaoAlreadyExistsError(TradeExternalError):
    pass

class DrawbackRestituicaoNotFoundError(TradeExternalError):
    pass

class DrawbackSubstituicaoAlreadyExistsError(TradeExternalError):
    pass

class DrawbackSubstituicaoNotFoundError(TradeExternalError):
    pass

class DrawbackSuspensaoAlreadyExistsError(TradeExternalError):
    pass

class DrawbackSuspensaoNotFoundError(TradeExternalError):
    pass

class DrawbackVerdeAmareloAlreadyExistsError(TradeExternalError):
    pass

class DrawbackVerdeAmareloNotFoundError(TradeExternalError):
    pass

class ExportadorAlreadyExistsError(TradeExternalError):
    pass

class ExportadorNotFoundError(TradeExternalError):
    pass

class HabilitacaoExportadorAlreadyExistsError(TradeExternalError):
    pass

class HabilitacaoExportadorNotFoundError(TradeExternalError):
    pass

class HabilitacaoImportadorAlreadyExistsError(TradeExternalError):
    pass

class HabilitacaoImportadorNotFoundError(TradeExternalError):
    pass

class HabilitacaoRadarAlreadyExistsError(TradeExternalError):
    pass

class HabilitacaoRadarNotFoundError(TradeExternalError):
    pass

class ImportadorAlreadyExistsError(TradeExternalError):
    pass

class ImportadorNotFoundError(TradeExternalError):
    pass

class InvalidAgenteCargaStateError(TradeExternalError):
    pass

class InvalidCancelamentoRadarStateError(TradeExternalError):
    pass

class InvalidDespachanteStateError(TradeExternalError):
    pass

class InvalidDrawbackExternoStateError(TradeExternalError):
    pass

class InvalidDrawbackIntegradoStateError(TradeExternalError):
    pass

class InvalidDrawbackInternoStateError(TradeExternalError):
    pass

class InvalidDrawbackIsencaoStateError(TradeExternalError):
    pass

class InvalidDrawbackRestituicaoStateError(TradeExternalError):
    pass

class InvalidDrawbackStateError(TradeExternalError):
    pass

class InvalidDrawbackSubstituicaoStateError(TradeExternalError):
    pass

class InvalidDrawbackSuspensaoStateError(TradeExternalError):
    pass

class InvalidDrawbackVerdeAmareloStateError(TradeExternalError):
    pass

class InvalidExportadorStateError(TradeExternalError):
    pass

class InvalidHabilitacaoExportadorStateError(TradeExternalError):
    pass

class InvalidHabilitacaoImportadorStateError(TradeExternalError):
    pass

class InvalidHabilitacaoRadarStateError(TradeExternalError):
    pass

class InvalidImportadorStateError(TradeExternalError):
    pass

class InvalidRadarStateError(TradeExternalError):
    pass

class InvalidSiscomexDrawbackStateError(TradeExternalError):
    pass

class InvalidSuspensaoRadarStateError(TradeExternalError):
    pass

class InvalidTransportadorInternacionalStateError(TradeExternalError):
    pass

class RadarAlreadyExistsError(TradeExternalError):
    pass

class RadarNotFoundError(TradeExternalError):
    pass

class SiscomexDrawbackAlreadyExistsError(TradeExternalError):
    pass

class SiscomexDrawbackNotFoundError(TradeExternalError):
    pass

class SuspensaoRadarAlreadyExistsError(TradeExternalError):
    pass

class SuspensaoRadarNotFoundError(TradeExternalError):
    pass

class TransportadorInternacionalAlreadyExistsError(TradeExternalError):
    pass

class TransportadorInternacionalNotFoundError(TradeExternalError):
    pass
