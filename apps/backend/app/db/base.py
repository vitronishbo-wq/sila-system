from app.core.db import Base
from app.core.bridges.identity_bridge import CitizenFUC
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.healthcare_model import HealthcareRequestModel, MaternalRecordModel, PostNatalRecordModel, ChronicMonitoringModel, NutritionRecordModel, PsychologySessionModel, HealthAlertModel
from apps.backend.app.modules.governance.service_requests.infrastructure.models.service_request_model import ServiceRequestModel
from apps.backend.app.modules.governance.service_requests.infrastructure.models.attachment_model import AttachmentModel
from apps.backend.app.modules.governance.service_requests.infrastructure.models.request_event_model import RequestEventModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.appointment_model import AppointmentModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.prescription_model import PrescriptionModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.medical_record_model import MedicalRecordModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.vaccine_model import VaccineModel, VaccineDoseModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.health_unit_model import HealthUnitModel, HealthProfessionalModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.exam_request_model import ExamRequestModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.exame_model import ExameImagemModel, ExameLaboratorialModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.internamento_model import InternamentoModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.urgencia_model import AmbulanciaModel, FilaHospitalarModel, UrgenciaModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.vigilancia_model import AlertaSaudeModel, ControleVetorModel, ControleZoonoseModel, MonitorizacaoHidricaModel, NotificacaoSurtoModel, VigilanciaEpidemiologicaModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.inspecao_model import ApreensaoProdutoModel, ControleAbatePublicoModel, ControleQualidadeAlimentoModel, FiscalizacaoAlimentoModel, FiscalizacaoCadeiaFrioModel, InspecaoSanitariaModel, InspecaoTransporteAlimentarModel, LicencaSanitariaModel, LicencaTemporariaModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.programa_model import ProgramaHIVModel, ProgramaMalariaModel, ProgramaPreventivoModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.rastreio_model import RastreioTuberculoseModel, TriagemDiabetesModel
# REMOVED (infrastructure not found): from apps.backend.app.modules.saude.core.infrastructure.models.relatorio_model import AvaliacaoRiscoSanitarioModel, EducacaoSanitariaModel, EmergenciaSanitariaModel, RelatorioSegurancaAlimentarModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_definition_model import WorkflowDefinitionModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_state_model import WorkflowStateModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_transition_model import WorkflowTransitionModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_instance_model import WorkflowInstanceModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_task_model import WorkflowTaskModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_history_model import WorkflowHistoryModel
from apps.backend.app.modules.intelligence.operations.infrastructure.models.order_model import OperationalOrderModel, OperationalOrderDocumentModel
from apps.backend.app.modules.intelligence.operations.infrastructure.models.payment_model import OperationalPaymentModel
from apps.backend.app.modules.intelligence.defesa_consumidor.infrastructure.models.reclamacao_model import ReclamacaoModel as DefesaConsumidorReclamacaoModel
from apps.backend.app.modules.educacao.infrastructure.models.matricula_model import MatriculaModel
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.modules.educacao.infrastructure.models.turma_model import TurmaModel
from apps.backend.app.modules.educacao.infrastructure.models.ano_letivo_model import AnoLetivoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.agente_carga_model import AgenteCargaModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.cancelamento_radar_model import CancelamentoRadarModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.despachante_model import DespachanteModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_externo_model import DrawbackExternoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_interno_model import DrawbackInternoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_model import DrawbackModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_isencao_model import DrawbackIsencaoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_integrado_model import DrawbackIntegradoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_restituicao_model import DrawbackRestituicaoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_substituicao_model import DrawbackSubstituicaoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_suspensao_model import DrawbackSuspensaoModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.drawback_verde_amarelo_model import DrawbackVerdeAmareloModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.exportador_model import ExportadorModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.habilitacao_exportador_model import HabilitacaoExportadorModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.habilitacao_importador_model import HabilitacaoImportadorModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.habilitacao_radar_model import HabilitacaoRadarModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.importador_model import ImportadorModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.radar_model import RadarModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.suspensao_radar_model import SuspensaoRadarModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.transportador_internacional_model import TransportadorInternacionalModel
from apps.backend.app.modules.economy.trade.external.infrastructure.models.siscomex_drawback_model import SiscomexDrawbackModel
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.animal_model import AnimalModel
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.pecuarista_model import PecuaristaModel
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.producao_leite_model import ProducaoLeiteModel
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.propriedade_pecuaria_model import PropriedadePecuariaModel
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.rebanho_model import RebanhoModel
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.vacina_model import VacinaModel
from apps.backend.app.modules.resources.pescas.infrastructure.models.armador_model import ArmadorModel
from apps.backend.app.modules.resources.pescas.infrastructure.models.captura_model import CapturaModel
from apps.backend.app.modules.resources.pescas.infrastructure.models.desembarque_model import DesembarqueModel
from apps.backend.app.modules.resources.pescas.infrastructure.models.embarcacao_model import EmbarcacaoModel
from apps.backend.app.modules.resources.pescas.infrastructure.models.especie_model import EspecieModel
from apps.backend.app.modules.resources.pescas.infrastructure.models.licenca_pesca_model import LicencaPescaModel
from apps.backend.app.modules.resources.pescas.infrastructure.models.pescador_model import PescadorModel
from apps.backend.app.modules.resources.florestas.infrastructure.models.operador_florestal_model import OperadorFlorestalModel
from apps.backend.app.modules.resources.florestas.infrastructure.models.unidade_manejo_model import UnidadeManejoModel
from apps.backend.app.modules.resources.florestas.infrastructure.models.plano_manejo_florestal_model import PlanoManejoFlorestalModel
from apps.backend.app.modules.resources.florestas.infrastructure.models.inventario_florestal_model import InventarioFlorestalModel
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.inspecao_model import InspecaoModel
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.lote_producao_model import LoteProducaoModel
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.produto_processado_model import ProdutoProcessadoModel
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.unidade_processamento_model import UnidadeProcessamentoModel
from apps.backend.app.modules.society.cultura.infrastructure.models.artista_model import ArtistaModel
from apps.backend.app.modules.society.cultura.infrastructure.models.bem_cultural_model import BemCulturalModel
from apps.backend.app.modules.society.cultura.infrastructure.models.evento_cultural_model import EventoCulturalModel
from apps.backend.app.modules.society.cultura.infrastructure.models.grupo_artistico_model import GrupoArtisticoModel
from apps.backend.app.modules.society.cultura.infrastructure.models.patrimonio_imaterial_model import PatrimonioImaterialModel
from apps.backend.app.modules.society.patrimonio_cultural.infrastructure.models.cultural_asset_model import CulturalAssetModel as PatrimonioCulturalAssetModel
from apps.backend.app.modules.society.desporto.infrastructure.models.atleta_model import AtletaModel
from apps.backend.app.modules.society.desporto.infrastructure.models.clube_model import ClubeModel
from apps.backend.app.modules.society.desporto.infrastructure.models.competicao_model import CompeticaoModel
from apps.backend.app.modules.society.desporto.infrastructure.models.jogo_model import JogoModel
from apps.backend.app.modules.society.juventude.infrastructure.models.acompanhamento_juvenil_model import AcompanhamentoJuvenilModel as JuventudeAcompanhamentoJuvenilModel
from apps.backend.app.modules.society.juventude.infrastructure.models.auxilio_model import AuxilioModel
from apps.backend.app.modules.society.juventude.infrastructure.models.bolsa_estudo_model import BolsaEstudoModel as JuventudeBolsaEstudoModel
from apps.backend.app.modules.society.juventude.infrastructure.models.empreendedorismo_juvenil_model import EmpreendedorismoJuvenilModel as JuventudeEmpreendedorismoJuvenilModel
from apps.backend.app.modules.society.juventude.infrastructure.models.estagio_juvenil_model import EstagioJuvenilModel as JuventudeEstagioJuvenilModel
from apps.backend.app.modules.society.juventude.infrastructure.models.evento_juvenil_model import EventoJuvenilModel as JuventudeEventoJuvenilModel
from apps.backend.app.modules.society.juventude.infrastructure.models.formacao_juvenil_model import FormacaoJuvenilModel
from apps.backend.app.modules.society.juventude.infrastructure.models.inscricao_programa_model import InscricaoProgramaModel as JuventudeInscricaoProgramaModel
from apps.backend.app.modules.society.juventude.infrastructure.models.intercambio_juvenil_model import IntercambioJuvenilModel as JuventudeIntercambioJuvenilModel
from apps.backend.app.modules.society.juventude.infrastructure.models.jovem_model import JovemModel
from apps.backend.app.modules.society.juventude.infrastructure.models.mentor_model import MentorModel as JuventudeMentorModel
from apps.backend.app.modules.society.juventude.infrastructure.models.politica_juventude_model import PoliticaJuventudeModel as JuventudePoliticaJuventudeModel
from apps.backend.app.modules.society.juventude.infrastructure.models.programa_juvenil_model import ProgramaJuvenilModel
from apps.backend.app.modules.society.juventude.infrastructure.models.risco_evasao_model import RiscoEvasaoModel as JuventudeRiscoEvasaoModel
from apps.backend.app.modules.society.juventude.infrastructure.models.saude_juvenil_model import SaudeJuvenilModel as JuventudeSaudeJuvenilModel
from apps.backend.app.modules.society.juventude.infrastructure.models.voluntariado_model import VoluntariadoModel as JuventudeVoluntariadoModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.atendimento_model import AtendimentoModel as AssistenciaAtendimentoModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.beneficiario_model import BeneficiarioModel as AssistenciaBeneficiarioModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.beneficio_model import BeneficioModel as AssistenciaBeneficioModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.cadastro_unico_model import CadastroUnicoModel as AssistenciaCadastroUnicoModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.crianca_risco_model import CriancaRiscoModel as AssistenciaCriancaRiscoModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.idoso_vulneravel_model import IdosoVulneravelModel as AssistenciaIdosoVulneravelModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.pcd_model import PCDModel as AssistenciaPCDModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.programa_social_model import ProgramaSocialModel as AssistenciaProgramaSocialModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.situacao_rua_model import SituacaoRuaModel as AssistenciaSituacaoRuaModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.visita_domiciliar_model import VisitaDomiciliarModel as AssistenciaVisitaDomiciliarModel
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.assinante_model import AssinanteModel as TelecomAssinanteModel
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.espectro_model import EspectroModel as TelecomEspectroModel
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.indicador_qualidade_model import IndicadorQualidadeModel as TelecomIndicadorQualidadeModel
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.infraestrutura_telco_model import InfraestruturaTelcoModel as TelecomInfraestruturaTelcoModel
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.operadora_model import OperadoraModel as TelecomOperadoraModel
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.outorga_espectro_model import OutorgaEspectroModel as TelecomOutorgaEspectroModel
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.qualidade_servico_model import QualidadeServicoModel as TelecomQualidadeServicoModel
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.sla_model import SLAModel as TelecomSLAModel
from apps.backend.app.modules.public_security.infrastructure.models.unidade_policial_model import UnidadePolicialModel as SegurancaUnidadePolicialModel
from apps.backend.app.modules.public_security.infrastructure.models.policial_model import PolicialModel as SegurancaPolicialModel
from apps.backend.app.modules.public_security.infrastructure.models.ocorrencia_model import OcorrenciaModel as SegurancaOcorrenciaModel
from apps.backend.app.modules.public_security.infrastructure.models.mandado_model import MandadoModel as SegurancaMandadoModel
from apps.backend.app.modules.public_security.infrastructure.models.investigacao_model import InvestigacaoModel as SegurancaInvestigacaoModel
from apps.backend.app.modules.public_security.infrastructure.models.prova_pericial_model import ProvaPericialModel as SegurancaProvaPericialModel
from apps.backend.app.modules.public_security.infrastructure.models.cadeia_custodia_model import CadeiaCustodiaModel as SegurancaCadeiaCustodiaModel
from apps.backend.app.modules.public_security.infrastructure.models.laudo_pericial_model import LaudoPericialModel as SegurancaLaudoPericialModel
from apps.backend.app.modules.public_security.infrastructure.models.vestigio_model import VestigioModel as SegurancaVestigioModel
from apps.backend.app.modules.public_security.infrastructure.models.evidencia_model import EvidenciaModel as SegurancaEvidenciaModel
from apps.backend.app.modules.civil_protection.infrastructure.models.corporacao_model import CorporacaoModel as ProtecaoCivilCorporacaoModel
from apps.backend.app.modules.civil_protection.infrastructure.models.bombeiro_model import BombeiroModel as ProtecaoCivilBombeiroModel
from apps.backend.app.modules.civil_protection.infrastructure.models.ocorrencia_emergencial_model import OcorrenciaEmergencialModel as ProtecaoCivilOcorrenciaEmergencialModel
from apps.backend.app.modules.civil_protection.infrastructure.models.despacho_model import DespachoModel as ProtecaoCivilDespachoModel
from apps.backend.app.modules.civil_protection.infrastructure.models.atendimento_model import AtendimentoModel as ProtecaoCivilAtendimentoModel
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.alvara_model import AlvaraModel as UrbanismoAlvaraModel
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.habite_se_model import HabiteSeModel as UrbanismoHabiteSeModel
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.licenca_urbanistica_model import LicencaUrbanisticaModel as UrbanismoLicencaUrbanisticaModel
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.loteamento_model import LoteamentoModel as UrbanismoLoteamentoModel
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.operacao_urbana_model import OperacaoUrbanaModel as UrbanismoOperacaoUrbanaModel
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.parcelamento_model import ParcelamentoModel as UrbanismoParcelamentoModel
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.plano_diretor_model import PlanoDiretorModel as UrbanismoPlanoDiretorModel
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.zoneamento_model import ZoneamentoModel as UrbanismoZoneamentoModel
from apps.backend.app.modules.infrastructure_sector.obras_publicas.infrastructure.models.edital_model import EditalModel as ObrasPublicasEditalModel
from apps.backend.app.modules.infrastructure_sector.obras_publicas.infrastructure.models.licitacao_model import LicitacaoModel as ObrasPublicasLicitacaoModel
from apps.backend.app.modules.infrastructure_sector.obras_publicas.infrastructure.models.obra_model import ObraModel as ObrasPublicasObraModel
from apps.backend.app.modules.infrastructure_sector.obras_publicas.infrastructure.models.projeto_model import ProjetoModel as ObrasPublicasProjetoModel
from apps.backend.app.modules.infrastructure_sector.logistica.transport.infrastructure.models.frota_model import FrotaModel as TransportesLogisticaFrotaModel
from apps.backend.app.modules.infrastructure_sector.logistica.transport.infrastructure.models.linha_model import LinhaModel as TransportesLogisticaLinhaModel
from apps.backend.app.modules.infrastructure_sector.logistica.transport.infrastructure.models.veiculo_model import VeiculoModel as TransportesLogisticaVeiculoModel
from apps.backend.app.modules.infrastructure_sector.logistica.transport.infrastructure.models.viagem_model import ViagemModel as TransportesLogisticaViagemModel
from apps.backend.app.modules.infrastructure_sector.logistica.transport.infrastructure.models.bilhetagem_evento_model import BilhetagemEventoModel as TransportesLogisticaBilhetagemEventoModel
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.models.outbox_event_model import OutboxEventModel as AguasSaneamentoOutboxEventModel
from apps.backend.app.modules.energy.infrastructure.models.energy_invoice_model import EnergyInvoiceModel
from apps.backend.app.modules.energy.infrastructure.models.energy_telemetry_model import EnergyTelemetryModel
from apps.backend.app.modules.energy.infrastructure.models.outbox_event_model import EnergiaOutboxEventModel
from apps.backend.app.modules.logistics.domain.infrastructure.models.toll_passage_model import (
    TollPassageModel,
)
from apps.backend.app.modules.justice.infrastructure.models.traffic_violation_model import TrafficViolationModel
from apps.backend.app.modules.society.familia.infrastructure.models.dependency_model import DependencyModel as FamiliaDependencyModel
from apps.backend.app.modules.society.familia.infrastructure.models.event_outbox_model import FamilyOutboxEventModel as FamiliaOutboxEventModel
from apps.backend.app.modules.society.familia.infrastructure.models.family_aggregate_model import FamilyAggregateModel as FamiliaAggregateModel
from apps.backend.app.modules.society.familia.infrastructure.models.family_member_model import FamilyMemberModel as FamiliaMemberModel
from apps.backend.app.modules.society.familia.infrastructure.models.projection_models import FamilyCompositionViewModel as FamiliaCompositionViewModel
from apps.backend.app.modules.society.familia.infrastructure.models.relationship_model import RelationshipModel as FamiliaRelationshipModel
from apps.backend.app.modules.infrastructure_sector.meteorologia.infrastructure.models.estacao_model import EstacaoMeteorologicaModel as MeteorologiaEstacaoModel
from apps.backend.app.modules.infrastructure_sector.meteorologia.infrastructure.models.observacao_model import ObservacaoMeteorologicaModel as MeteorologiaObservacaoModel
__all__ = ['Base', 'CitizenFUC', 'UserModel', 'UserRoleModel', 'RoleModel', 'RolePermissionModel', 'PermissionModel', 'UserPermissionModel', 'SessionModel', 'RefreshTokenModel', 'AuditLogModel', 'ServiceRequestModel', 'AttachmentModel', 'RequestEventModel', 'WorkflowDefinitionModel', 'WorkflowStateModel', 'WorkflowTransitionModel', 'WorkflowInstanceModel', 'WorkflowTaskModel', 'WorkflowHistoryModel', 'OperationalOrderModel', 'OperationalOrderDocumentModel', 'OperationalPaymentModel', 'DefesaConsumidorReclamacaoModel', 'MatriculaModel', 'EscolaModel', 'TurmaModel', 'AnoLetivoModel', 'ExportadorModel', 'ImportadorModel', 'DespachanteModel', 'AgenteCargaModel', 'TransportadorInternacionalModel', 'HabilitacaoExportadorModel', 'HabilitacaoImportadorModel', 'HabilitacaoRadarModel', 'RadarModel', 'CancelamentoRadarModel', 'SuspensaoRadarModel', 'DrawbackModel', 'DrawbackExternoModel', 'DrawbackInternoModel', 'DrawbackIsencaoModel', 'DrawbackIntegradoModel', 'DrawbackRestituicaoModel', 'DrawbackSubstituicaoModel', 'DrawbackSuspensaoModel', 'DrawbackVerdeAmareloModel', 'SiscomexDrawbackModel', 'PecuaristaModel', 'PropriedadePecuariaModel', 'RebanhoModel', 'AnimalModel', 'ProducaoLeiteModel', 'VacinaModel', 'PescadorModel', 'ArmadorModel', 'EmbarcacaoModel', 'LicencaPescaModel', 'CapturaModel', 'EspecieModel', 'DesembarqueModel', 'OperadorFlorestalModel', 'UnidadeManejoModel', 'PlanoManejoFlorestalModel', 'InventarioFlorestalModel', 'UnidadeProcessamentoModel', 'ProdutoProcessadoModel', 'LoteProducaoModel', 'InspecaoModel', 'ArtistaModel', 'BemCulturalModel', 'EventoCulturalModel', 'GrupoArtisticoModel', 'PatrimonioImaterialModel', 'AtletaModel', 'CompeticaoModel', 'ClubeModel', 'JogoModel', 'UrbanismoPlanoDiretorModel', 'UrbanismoZoneamentoModel', 'UrbanismoOperacaoUrbanaModel', 'UrbanismoParcelamentoModel', 'UrbanismoLoteamentoModel', 'UrbanismoLicencaUrbanisticaModel', 'UrbanismoAlvaraModel', 'UrbanismoHabiteSeModel', 'ObrasPublicasProjetoModel', 'ObrasPublicasObraModel', 'ObrasPublicasLicitacaoModel', 'ObrasPublicasEditalModel', 'TransportesLogisticaViagemModel', 'TransportesLogisticaFrotaModel', 'TransportesLogisticaLinhaModel', 'TransportesLogisticaVeiculoModel', 'TransportesLogisticaBilhetagemEventoModel', 'AguasSaneamentoOutboxEventModel', 'EnergiaOutboxEventModel', 'EnergyTelemetryModel', 'EnergyInvoiceModel', 'TollPassageModel', 'TrafficViolationModel', 'FamiliaAggregateModel', 'FamiliaMemberModel', 'FamiliaRelationshipModel', 'FamiliaDependencyModel', 'FamiliaOutboxEventModel', 'FamiliaCompositionViewModel', 'MeteorologiaEstacaoModel', 'MeteorologiaObservacaoModel']

def _register_statistics_models():
    """Lazy load statistics models to avoid circular import"""
    try:
        from apps.backend.app.modules.governance.statistics.infrastructure.models.statistic_model import StatisticModel
        from apps.backend.app.modules.governance.statistics.infrastructure.models.timeseries_model import TimeSeriesModel
        from apps.backend.app.modules.governance.statistics.infrastructure.models.aggregation_model import AggregationModel
        return (StatisticModel, TimeSeriesModel, AggregationModel)
    except ImportError:
        return (None, None, None)

def _register_taxpayer_models():
    """Lazy load taxpayer models to avoid circular import during runtime.
	Note: the direct import above ensures Alembic sees the model for autogenerate.
	"""
    try:
        from apps.backend.app.modules.economy.taxpayer.infrastructure.models.taxpayer_model import TaxpayerModel
        return TaxpayerModel
    except ImportError:
        return None
from apps.backend.app.modules.governance.statistics.infrastructure import models as estatistica_models
