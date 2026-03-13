from app.core.db import Base
from app.core.bridges.identity_bridge import CitizenFUC
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.healthcare_model import HealthcareRequestModel, MaternalRecordModel, PostNatalRecordModel, ChronicMonitoringModel, NutritionRecordModel, PsychologySessionModel, HealthAlertModel
from app.modules.governance.service_requests.infrastructure.models.service_request_model import ServiceRequestModel
from app.modules.governance.service_requests.infrastructure.models.attachment_model import AttachmentModel
from app.modules.governance.service_requests.infrastructure.models.request_event_model import RequestEventModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.appointment_model import AppointmentModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.prescription_model import PrescriptionModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.medical_record_model import MedicalRecordModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.vaccine_model import VaccineModel, VaccineDoseModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.health_unit_model import HealthUnitModel, HealthProfessionalModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.exam_request_model import ExamRequestModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.exame_model import ExameImagemModel, ExameLaboratorialModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.internamento_model import InternamentoModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.urgencia_model import AmbulanciaModel, FilaHospitalarModel, UrgenciaModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.vigilancia_model import AlertaSaudeModel, ControleVetorModel, ControleZoonoseModel, MonitorizacaoHidricaModel, NotificacaoSurtoModel, VigilanciaEpidemiologicaModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.inspecao_model import ApreensaoProdutoModel, ControleAbatePublicoModel, ControleQualidadeAlimentoModel, FiscalizacaoAlimentoModel, FiscalizacaoCadeiaFrioModel, InspecaoSanitariaModel, InspecaoTransporteAlimentarModel, LicencaSanitariaModel, LicencaTemporariaModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.programa_model import ProgramaHIVModel, ProgramaMalariaModel, ProgramaPreventivoModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.rastreio_model import RastreioTuberculoseModel, TriagemDiabetesModel
# REMOVED (infrastructure not found): from app.modules.saude.core.infrastructure.models.relatorio_model import AvaliacaoRiscoSanitarioModel, EducacaoSanitariaModel, EmergenciaSanitariaModel, RelatorioSegurancaAlimentarModel
from app.modules.governance.workflow.infrastructure.models.workflow_definition_model import WorkflowDefinitionModel
from app.modules.governance.workflow.infrastructure.models.workflow_state_model import WorkflowStateModel
from app.modules.governance.workflow.infrastructure.models.workflow_transition_model import WorkflowTransitionModel
from app.modules.governance.workflow.infrastructure.models.workflow_instance_model import WorkflowInstanceModel
from app.modules.governance.workflow.infrastructure.models.workflow_task_model import WorkflowTaskModel
from app.modules.governance.workflow.infrastructure.models.workflow_history_model import WorkflowHistoryModel
from app.modules.intelligence.operations.infrastructure.models.order_model import OperationalOrderModel, OperationalOrderDocumentModel
from app.modules.intelligence.operations.infrastructure.models.payment_model import OperationalPaymentModel
from app.modules.intelligence.defesa_consumidor.infrastructure.models.reclamacao_model import ReclamacaoModel as DefesaConsumidorReclamacaoModel
from app.modules.educacao.infrastructure.models.matricula_model import MatriculaModel
from app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from app.modules.educacao.infrastructure.models.turma_model import TurmaModel
from app.modules.educacao.infrastructure.models.ano_letivo_model import AnoLetivoModel
from app.modules.economy.trade.external.infrastructure.models.agente_carga_model import AgenteCargaModel
from app.modules.economy.trade.external.infrastructure.models.cancelamento_radar_model import CancelamentoRadarModel
from app.modules.economy.trade.external.infrastructure.models.despachante_model import DespachanteModel
from app.modules.economy.trade.external.infrastructure.models.drawback_externo_model import DrawbackExternoModel
from app.modules.economy.trade.external.infrastructure.models.drawback_interno_model import DrawbackInternoModel
from app.modules.economy.trade.external.infrastructure.models.drawback_model import DrawbackModel
from app.modules.economy.trade.external.infrastructure.models.drawback_isencao_model import DrawbackIsencaoModel
from app.modules.economy.trade.external.infrastructure.models.drawback_integrado_model import DrawbackIntegradoModel
from app.modules.economy.trade.external.infrastructure.models.drawback_restituicao_model import DrawbackRestituicaoModel
from app.modules.economy.trade.external.infrastructure.models.drawback_substituicao_model import DrawbackSubstituicaoModel
from app.modules.economy.trade.external.infrastructure.models.drawback_suspensao_model import DrawbackSuspensaoModel
from app.modules.economy.trade.external.infrastructure.models.drawback_verde_amarelo_model import DrawbackVerdeAmareloModel
from app.modules.economy.trade.external.infrastructure.models.exportador_model import ExportadorModel
from app.modules.economy.trade.external.infrastructure.models.habilitacao_exportador_model import HabilitacaoExportadorModel
from app.modules.economy.trade.external.infrastructure.models.habilitacao_importador_model import HabilitacaoImportadorModel
from app.modules.economy.trade.external.infrastructure.models.habilitacao_radar_model import HabilitacaoRadarModel
from app.modules.economy.trade.external.infrastructure.models.importador_model import ImportadorModel
from app.modules.economy.trade.external.infrastructure.models.radar_model import RadarModel
from app.modules.economy.trade.external.infrastructure.models.suspensao_radar_model import SuspensaoRadarModel
from app.modules.economy.trade.external.infrastructure.models.transportador_internacional_model import TransportadorInternacionalModel
from app.modules.economy.trade.external.infrastructure.models.siscomex_drawback_model import SiscomexDrawbackModel
from app.modules.resources.pecuaria.infrastructure.models.animal_model import AnimalModel
from app.modules.resources.pecuaria.infrastructure.models.pecuarista_model import PecuaristaModel
from app.modules.resources.pecuaria.infrastructure.models.producao_leite_model import ProducaoLeiteModel
from app.modules.resources.pecuaria.infrastructure.models.propriedade_pecuaria_model import PropriedadePecuariaModel
from app.modules.resources.pecuaria.infrastructure.models.rebanho_model import RebanhoModel
from app.modules.resources.pecuaria.infrastructure.models.vacina_model import VacinaModel
from app.modules.resources.pescas.infrastructure.models.armador_model import ArmadorModel
from app.modules.resources.pescas.infrastructure.models.captura_model import CapturaModel
from app.modules.resources.pescas.infrastructure.models.desembarque_model import DesembarqueModel
from app.modules.resources.pescas.infrastructure.models.embarcacao_model import EmbarcacaoModel
from app.modules.resources.pescas.infrastructure.models.especie_model import EspecieModel
from app.modules.resources.pescas.infrastructure.models.licenca_pesca_model import LicencaPescaModel
from app.modules.resources.pescas.infrastructure.models.pescador_model import PescadorModel
from app.modules.resources.florestas.infrastructure.models.operador_florestal_model import OperadorFlorestalModel
from app.modules.resources.florestas.infrastructure.models.unidade_manejo_model import UnidadeManejoModel
from app.modules.resources.florestas.infrastructure.models.plano_manejo_florestal_model import PlanoManejoFlorestalModel
from app.modules.resources.florestas.infrastructure.models.inventario_florestal_model import InventarioFlorestalModel
from app.modules.resources.pescas.industrial.infrastructure.models.inspecao_model import InspecaoModel
from app.modules.resources.pescas.industrial.infrastructure.models.lote_producao_model import LoteProducaoModel
from app.modules.resources.pescas.industrial.infrastructure.models.produto_processado_model import ProdutoProcessadoModel
from app.modules.resources.pescas.industrial.infrastructure.models.unidade_processamento_model import UnidadeProcessamentoModel
from app.modules.society.cultura.infrastructure.models.artista_model import ArtistaModel
from app.modules.society.cultura.infrastructure.models.bem_cultural_model import BemCulturalModel
from app.modules.society.cultura.infrastructure.models.evento_cultural_model import EventoCulturalModel
from app.modules.society.cultura.infrastructure.models.grupo_artistico_model import GrupoArtisticoModel
from app.modules.society.cultura.infrastructure.models.patrimonio_imaterial_model import PatrimonioImaterialModel
from app.modules.society.patrimonio_cultural.infrastructure.models.cultural_asset_model import CulturalAssetModel as PatrimonioCulturalAssetModel
from app.modules.society.desporto.infrastructure.models.atleta_model import AtletaModel
from app.modules.society.desporto.infrastructure.models.clube_model import ClubeModel
from app.modules.society.desporto.infrastructure.models.competicao_model import CompeticaoModel
from app.modules.society.desporto.infrastructure.models.jogo_model import JogoModel
from app.modules.society.juventude.infrastructure.models.acompanhamento_juvenil_model import AcompanhamentoJuvenilModel as JuventudeAcompanhamentoJuvenilModel
from app.modules.society.juventude.infrastructure.models.auxilio_model import AuxilioModel
from app.modules.society.juventude.infrastructure.models.bolsa_estudo_model import BolsaEstudoModel as JuventudeBolsaEstudoModel
from app.modules.society.juventude.infrastructure.models.empreendedorismo_juvenil_model import EmpreendedorismoJuvenilModel as JuventudeEmpreendedorismoJuvenilModel
from app.modules.society.juventude.infrastructure.models.estagio_juvenil_model import EstagioJuvenilModel as JuventudeEstagioJuvenilModel
from app.modules.society.juventude.infrastructure.models.evento_juvenil_model import EventoJuvenilModel as JuventudeEventoJuvenilModel
from app.modules.society.juventude.infrastructure.models.formacao_juvenil_model import FormacaoJuvenilModel
from app.modules.society.juventude.infrastructure.models.inscricao_programa_model import InscricaoProgramaModel as JuventudeInscricaoProgramaModel
from app.modules.society.juventude.infrastructure.models.intercambio_juvenil_model import IntercambioJuvenilModel as JuventudeIntercambioJuvenilModel
from app.modules.society.juventude.infrastructure.models.jovem_model import JovemModel
from app.modules.society.juventude.infrastructure.models.mentor_model import MentorModel as JuventudeMentorModel
from app.modules.society.juventude.infrastructure.models.politica_juventude_model import PoliticaJuventudeModel as JuventudePoliticaJuventudeModel
from app.modules.society.juventude.infrastructure.models.programa_juvenil_model import ProgramaJuvenilModel
from app.modules.society.juventude.infrastructure.models.risco_evasao_model import RiscoEvasaoModel as JuventudeRiscoEvasaoModel
from app.modules.society.juventude.infrastructure.models.saude_juvenil_model import SaudeJuvenilModel as JuventudeSaudeJuvenilModel
from app.modules.society.juventude.infrastructure.models.voluntariado_model import VoluntariadoModel as JuventudeVoluntariadoModel
from app.modules.society.assistencia_social.infrastructure.models.atendimento_model import AtendimentoModel as AssistenciaAtendimentoModel
from app.modules.society.assistencia_social.infrastructure.models.beneficiario_model import BeneficiarioModel as AssistenciaBeneficiarioModel
from app.modules.society.assistencia_social.infrastructure.models.beneficio_model import BeneficioModel as AssistenciaBeneficioModel
from app.modules.society.assistencia_social.infrastructure.models.cadastro_unico_model import CadastroUnicoModel as AssistenciaCadastroUnicoModel
from app.modules.society.assistencia_social.infrastructure.models.crianca_risco_model import CriancaRiscoModel as AssistenciaCriancaRiscoModel
from app.modules.society.assistencia_social.infrastructure.models.idoso_vulneravel_model import IdosoVulneravelModel as AssistenciaIdosoVulneravelModel
from app.modules.society.assistencia_social.infrastructure.models.pcd_model import PCDModel as AssistenciaPCDModel
from app.modules.society.assistencia_social.infrastructure.models.programa_social_model import ProgramaSocialModel as AssistenciaProgramaSocialModel
from app.modules.society.assistencia_social.infrastructure.models.situacao_rua_model import SituacaoRuaModel as AssistenciaSituacaoRuaModel
from app.modules.society.assistencia_social.infrastructure.models.visita_domiciliar_model import VisitaDomiciliarModel as AssistenciaVisitaDomiciliarModel
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.assinante_model import AssinanteModel as TelecomAssinanteModel
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.espectro_model import EspectroModel as TelecomEspectroModel
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.indicador_qualidade_model import IndicadorQualidadeModel as TelecomIndicadorQualidadeModel
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.infraestrutura_telco_model import InfraestruturaTelcoModel as TelecomInfraestruturaTelcoModel
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.operadora_model import OperadoraModel as TelecomOperadoraModel
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.outorga_espectro_model import OutorgaEspectroModel as TelecomOutorgaEspectroModel
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.qualidade_servico_model import QualidadeServicoModel as TelecomQualidadeServicoModel
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.sla_model import SLAModel as TelecomSLAModel
from app.modules.public_security.infrastructure.models.unidade_policial_model import UnidadePolicialModel as SegurancaUnidadePolicialModel
from app.modules.public_security.infrastructure.models.policial_model import PolicialModel as SegurancaPolicialModel
from app.modules.public_security.infrastructure.models.ocorrencia_model import OcorrenciaModel as SegurancaOcorrenciaModel
from app.modules.public_security.infrastructure.models.mandado_model import MandadoModel as SegurancaMandadoModel
from app.modules.public_security.infrastructure.models.investigacao_model import InvestigacaoModel as SegurancaInvestigacaoModel
from app.modules.public_security.infrastructure.models.prova_pericial_model import ProvaPericialModel as SegurancaProvaPericialModel
from app.modules.public_security.infrastructure.models.cadeia_custodia_model import CadeiaCustodiaModel as SegurancaCadeiaCustodiaModel
from app.modules.public_security.infrastructure.models.laudo_pericial_model import LaudoPericialModel as SegurancaLaudoPericialModel
from app.modules.public_security.infrastructure.models.vestigio_model import VestigioModel as SegurancaVestigioModel
from app.modules.public_security.infrastructure.models.evidencia_model import EvidenciaModel as SegurancaEvidenciaModel
from app.modules.civil_protection.infrastructure.models.corporacao_model import CorporacaoModel as ProtecaoCivilCorporacaoModel
from app.modules.civil_protection.infrastructure.models.bombeiro_model import BombeiroModel as ProtecaoCivilBombeiroModel
from app.modules.civil_protection.infrastructure.models.ocorrencia_emergencial_model import OcorrenciaEmergencialModel as ProtecaoCivilOcorrenciaEmergencialModel
from app.modules.civil_protection.infrastructure.models.despacho_model import DespachoModel as ProtecaoCivilDespachoModel
from app.modules.civil_protection.infrastructure.models.atendimento_model import AtendimentoModel as ProtecaoCivilAtendimentoModel
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.alvara_model import AlvaraModel as UrbanismoAlvaraModel
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.habite_se_model import HabiteSeModel as UrbanismoHabiteSeModel
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.licenca_urbanistica_model import LicencaUrbanisticaModel as UrbanismoLicencaUrbanisticaModel
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.loteamento_model import LoteamentoModel as UrbanismoLoteamentoModel
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.operacao_urbana_model import OperacaoUrbanaModel as UrbanismoOperacaoUrbanaModel
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.parcelamento_model import ParcelamentoModel as UrbanismoParcelamentoModel
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.plano_diretor_model import PlanoDiretorModel as UrbanismoPlanoDiretorModel
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.zoneamento_model import ZoneamentoModel as UrbanismoZoneamentoModel
from app.modules.infrastructure_sector.obras_publicas.infrastructure.models.edital_model import EditalModel as ObrasPublicasEditalModel
from app.modules.infrastructure_sector.obras_publicas.infrastructure.models.licitacao_model import LicitacaoModel as ObrasPublicasLicitacaoModel
from app.modules.infrastructure_sector.obras_publicas.infrastructure.models.obra_model import ObraModel as ObrasPublicasObraModel
from app.modules.infrastructure_sector.obras_publicas.infrastructure.models.projeto_model import ProjetoModel as ObrasPublicasProjetoModel
from app.modules.infrastructure_sector.logistica.transport.infrastructure.models.frota_model import FrotaModel as TransportesLogisticaFrotaModel
from app.modules.infrastructure_sector.logistica.transport.infrastructure.models.linha_model import LinhaModel as TransportesLogisticaLinhaModel
from app.modules.infrastructure_sector.logistica.transport.infrastructure.models.veiculo_model import VeiculoModel as TransportesLogisticaVeiculoModel
from app.modules.infrastructure_sector.logistica.transport.infrastructure.models.viagem_model import ViagemModel as TransportesLogisticaViagemModel
from app.modules.infrastructure_sector.logistica.transport.infrastructure.models.bilhetagem_evento_model import BilhetagemEventoModel as TransportesLogisticaBilhetagemEventoModel
from app.modules.resources.aguas_saneamento.infrastructure.models.outbox_event_model import OutboxEventModel as AguasSaneamentoOutboxEventModel
from app.modules.energy.infrastructure.models.energy_invoice_model import EnergyInvoiceModel
from app.modules.energy.infrastructure.models.energy_telemetry_model import EnergyTelemetryModel
from app.modules.energy.infrastructure.models.outbox_event_model import EnergiaOutboxEventModel
from app.modules.logistics.domain.infrastructure.models.toll_passage_model import (
    TollPassageModel,
)
from app.modules.justice.infrastructure.models.traffic_violation_model import TrafficViolationModel
from app.modules.society.familia.infrastructure.models.dependency_model import DependencyModel as FamiliaDependencyModel
from app.modules.society.familia.infrastructure.models.event_outbox_model import FamilyOutboxEventModel as FamiliaOutboxEventModel
from app.modules.society.familia.infrastructure.models.family_aggregate_model import FamilyAggregateModel as FamiliaAggregateModel
from app.modules.society.familia.infrastructure.models.family_member_model import FamilyMemberModel as FamiliaMemberModel
from app.modules.society.familia.infrastructure.models.projection_models import FamilyCompositionViewModel as FamiliaCompositionViewModel
from app.modules.society.familia.infrastructure.models.relationship_model import RelationshipModel as FamiliaRelationshipModel
from app.modules.infrastructure_sector.meteorologia.infrastructure.models.estacao_model import EstacaoMeteorologicaModel as MeteorologiaEstacaoModel
from app.modules.infrastructure_sector.meteorologia.infrastructure.models.observacao_model import ObservacaoMeteorologicaModel as MeteorologiaObservacaoModel
__all__ = ['Base', 'CitizenFUC', 'UserModel', 'UserRoleModel', 'RoleModel', 'RolePermissionModel', 'PermissionModel', 'UserPermissionModel', 'SessionModel', 'RefreshTokenModel', 'AuditLogModel', 'ServiceRequestModel', 'AttachmentModel', 'RequestEventModel', 'WorkflowDefinitionModel', 'WorkflowStateModel', 'WorkflowTransitionModel', 'WorkflowInstanceModel', 'WorkflowTaskModel', 'WorkflowHistoryModel', 'OperationalOrderModel', 'OperationalOrderDocumentModel', 'OperationalPaymentModel', 'DefesaConsumidorReclamacaoModel', 'MatriculaModel', 'EscolaModel', 'TurmaModel', 'AnoLetivoModel', 'ExportadorModel', 'ImportadorModel', 'DespachanteModel', 'AgenteCargaModel', 'TransportadorInternacionalModel', 'HabilitacaoExportadorModel', 'HabilitacaoImportadorModel', 'HabilitacaoRadarModel', 'RadarModel', 'CancelamentoRadarModel', 'SuspensaoRadarModel', 'DrawbackModel', 'DrawbackExternoModel', 'DrawbackInternoModel', 'DrawbackIsencaoModel', 'DrawbackIntegradoModel', 'DrawbackRestituicaoModel', 'DrawbackSubstituicaoModel', 'DrawbackSuspensaoModel', 'DrawbackVerdeAmareloModel', 'SiscomexDrawbackModel', 'PecuaristaModel', 'PropriedadePecuariaModel', 'RebanhoModel', 'AnimalModel', 'ProducaoLeiteModel', 'VacinaModel', 'PescadorModel', 'ArmadorModel', 'EmbarcacaoModel', 'LicencaPescaModel', 'CapturaModel', 'EspecieModel', 'DesembarqueModel', 'OperadorFlorestalModel', 'UnidadeManejoModel', 'PlanoManejoFlorestalModel', 'InventarioFlorestalModel', 'UnidadeProcessamentoModel', 'ProdutoProcessadoModel', 'LoteProducaoModel', 'InspecaoModel', 'ArtistaModel', 'BemCulturalModel', 'EventoCulturalModel', 'GrupoArtisticoModel', 'PatrimonioImaterialModel', 'AtletaModel', 'CompeticaoModel', 'ClubeModel', 'JogoModel', 'UrbanismoPlanoDiretorModel', 'UrbanismoZoneamentoModel', 'UrbanismoOperacaoUrbanaModel', 'UrbanismoParcelamentoModel', 'UrbanismoLoteamentoModel', 'UrbanismoLicencaUrbanisticaModel', 'UrbanismoAlvaraModel', 'UrbanismoHabiteSeModel', 'ObrasPublicasProjetoModel', 'ObrasPublicasObraModel', 'ObrasPublicasLicitacaoModel', 'ObrasPublicasEditalModel', 'TransportesLogisticaViagemModel', 'TransportesLogisticaFrotaModel', 'TransportesLogisticaLinhaModel', 'TransportesLogisticaVeiculoModel', 'TransportesLogisticaBilhetagemEventoModel', 'AguasSaneamentoOutboxEventModel', 'EnergiaOutboxEventModel', 'EnergyTelemetryModel', 'EnergyInvoiceModel', 'TollPassageModel', 'TrafficViolationModel', 'FamiliaAggregateModel', 'FamiliaMemberModel', 'FamiliaRelationshipModel', 'FamiliaDependencyModel', 'FamiliaOutboxEventModel', 'FamiliaCompositionViewModel', 'MeteorologiaEstacaoModel', 'MeteorologiaObservacaoModel']

def _register_statistics_models():
    """Lazy load statistics models to avoid circular import"""
    try:
        from app.modules.governance.statistics.infrastructure.models.statistic_model import StatisticModel
        from app.modules.governance.statistics.infrastructure.models.timeseries_model import TimeSeriesModel
        from app.modules.governance.statistics.infrastructure.models.aggregation_model import AggregationModel
        return (StatisticModel, TimeSeriesModel, AggregationModel)
    except ImportError:
        return (None, None, None)

def _register_taxpayer_models():
    """Lazy load taxpayer models to avoid circular import during runtime.
	Note: the direct import above ensures Alembic sees the model for autogenerate.
	"""
    try:
        from app.modules.economy.taxpayer.infrastructure.models.taxpayer_model import TaxpayerModel
        return TaxpayerModel
    except ImportError:
        return None
from app.modules.governance.statistics.infrastructure import models as estatistica_models
