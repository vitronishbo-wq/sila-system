#!/usr/bin/env python3
"""Remove phantom saude references from base.py __all__"""

import re

# Read the file
with open('apps/backend/app/db/base.py', 'r') as f:
    content = f.read()

# Remove from __all__ all the saude health models
saude_models = [
    'HealthcareRequestModel', 'MaternalRecordModel', 'PostNatalRecordModel',
    'ChronicMonitoringModel', 'NutritionRecordModel', 'PsychologySessionModel',
    'HealthAlertModel', 'AppointmentModel', 'PrescriptionModel',
    'MedicalRecordModel', 'VaccineModel', 'VaccineDoseModel', 'HealthUnitModel',
    'HealthProfessionalModel', 'ExamRequestModel', 'ExameImagemModel',
    'ExameLaboratorialModel', 'InternamentoModel', 'UrgenciaModel',
    'AmbulanciaModel', 'FilaHospitalarModel', 'VigilanciaEpidemiologicaModel',
    'NotificacaoSurtoModel', 'ControleVetorModel', 'ControleZoonoseModel',
    'MonitorizacaoHidricaModel', 'AlertaSaudeModel', 'InspecaoSanitariaModel',
    'LicencaSanitariaModel', 'LicencaTemporariaModel', 'FiscalizacaoAlimentoModel',
    'ControleQualidadeAlimentoModel', 'FiscalizacaoCadeiaFrioModel',
    'ControleAbatePublicoModel', 'InspecaoTransporteAlimentarModel',
    'ApreensaoProdutoModel', 'ProgramaMalariaModel', 'ProgramaHIVModel',
    'ProgramaPreventivoModel', 'RastreioTuberculoseModel', 'TriagemDiabetesModel',
    'RelatorioSegurancaAlimentarModel', 'AvaliacaoRiscoSanitarioModel',
    'EmergenciaSanitariaModel', 'EducacaoSanitariaModel'
]

# Remove from __all__ string
for model in saude_models:
    content = re.sub(r", '" + model + r"'", '', content)
    content = re.sub(r"'" + model + r"', ", '', content)

# Write back
with open('apps/backend/app/db/base.py', 'w') as f:
    f.write(content)
    
print('✅ Removed saude models from __all__')
