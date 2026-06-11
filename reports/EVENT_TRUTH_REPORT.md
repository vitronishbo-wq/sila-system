# EVENT TRUTH RECONCILIATION REPORT

> Gerado em: 2026-06-08
> Proposito: Reconciliar eventos entre RegistryCatalog e Runtime real

---

## Resumo

| Metrica | Valor |
|---|---|
| Total eventos Registry | 42 |
| Total eventos Runtime | 75 |
| Total eventos reconciliados | 108 |
| VALID | 9 |
| REGISTRY_ONLY (Ghost) | 33 |
| RUNTIME_ONLY | 66 |
| NAME_MISMATCH | 0 |

## Tabela de Reconciliacao

| Evento | Registry Name | Runtime Name | Registry | Runtime | Status |
|---|---|---|---|---|---|
| APIAccessTokenIssued | APIAccessTokenIssued | Apiaccesstokenissued | - | api(defines), api(class) | RUNTIME_ONLY |
| APIEndpointRegistered | APIEndpointRegistered | Apiendpointregistered | - | api(defines), api(class) | RUNTIME_ONLY |
| APIEndpointStatusChanged | APIEndpointStatusChanged | Apiendpointstatuschanged | - | api(defines), api(class) | RUNTIME_ONLY |
| APIRequestProcessed | APIRequestProcessed | Apirequestprocessed | - | api(defines), api(class) | RUNTIME_ONLY |
| APISecurityPolicyEnforced | APISecurityPolicyEnforced | Apisecuritypolicyenforced | - | api(defines), api(class) | RUNTIME_ONLY |
| AcademicDegreeAwarded | AcademicDegreeAwarded | Academicdegreeawarded | - | educacao(defines), educacao(class), educacao(handles) | RUNTIME_ONLY |
| AdminOfficeStatusChanged | AdminOfficeStatusChanged | Adminofficestatuschanged | - | governance(defines), governance(class), governance(handles) | RUNTIME_ONLY |
| AuditExecutionStarted | AuditExecutionStarted | Auditexecutionstarted | - | audit(defines), audit(class), audit(handles) | RUNTIME_ONLY |
| AuditFindingReported | AuditFindingReported | Auditfindingreported | - | audit(defines), audit(class), audit(handles) | RUNTIME_ONLY |
| AuditProgramCreated | AuditProgramCreated | Auditprogramcreated | - | audit(defines), audit(class), audit(handles) | RUNTIME_ONLY |
| AuditReportSubmitted | AuditReportSubmitted | Auditreportsubmitted | - | audit(defines), audit(class), audit(handles) | RUNTIME_ONLY |
| BiometricDataEnrolled | BiometricDataEnrolled | Biometricdataenrolled | identity(exposes) | identity(defines), identity(class), identity(handles) | VALID |
| BirthRecordCertificateIssued | BirthRecordCertificateIssued | Birthrecordcertificateissued | - | justice(class), justice(handles) | RUNTIME_ONLY |
| BirthRecordCreated | BirthRecordCreated | Birthrecordcreated | identity(consumes), registo-civil(exposes) | justice(class), justice(handles) | VALID |
| CitizenCreated | CitizenCreated | Citizencreated | - | justice(class), justice(handles) | RUNTIME_ONLY |
| CitizenIdentityDocumentIssued | CitizenIdentityDocumentIssued | Citizenidentitydocumentissued | - | justice(class), justice(handles) | RUNTIME_ONLY |
| CitizenStatusChanged | CitizenStatusChanged | Citizenstatuschanged | - | justice(class) | RUNTIME_ONLY |
| CivilProtectionResourceStatusChanged | CivilProtectionResourceStatusChanged | Civilprotectionresourcestatuschanged | - | civil_protection(defines), civil_protection(class), civil_protection(handles) | RUNTIME_ONLY |
| ComplianceCertificateIssued | ComplianceCertificateIssued | Compliancecertificateissued | - | compliance(defines), compliance(class), compliance(handles) | RUNTIME_ONLY |
| ComplianceInspectionConducted | ComplianceInspectionConducted | Complianceinspectionconducted | - | compliance(defines), compliance(class), compliance(handles) | RUNTIME_ONLY |
| ComplianceObligationCreated | ComplianceObligationCreated | Complianceobligationcreated | - | compliance(defines), compliance(class), compliance(handles) | RUNTIME_ONLY |
| ComplianceObligationStatusChanged | ComplianceObligationStatusChanged | Complianceobligationstatuschanged | - | compliance(defines), compliance(class), compliance(handles) | RUNTIME_ONLY |
| ComplianceViolationReported | ComplianceViolationReported | Complianceviolationreported | - | compliance(defines), compliance(class), compliance(handles) | RUNTIME_ONLY |
| ControllerRecommendationIssued | ControllerRecommendationIssued | Controllerrecommendationissued | - | audit(defines), audit(class), audit(handles) | RUNTIME_ONLY |
| DeathCertificateIssued | DeathCertificateIssued | Deathcertificateissued | - | justice(class), justice(handles) | RUNTIME_ONLY |
| DeathRecorded | DeathRecorded | Deathrecorded | identity(consumes), registo-civil(exposes) | justice(class), justice(handles) | VALID |
| DisasterEventOccurred | DisasterEventOccurred | Disastereventoccurred | - | civil_protection(defines), civil_protection(class), civil_protection(handles) | RUNTIME_ONLY |
| DisasterRecoveryInitiated | DisasterRecoveryInitiated | Disasterrecoveryinitiated | - | civil_protection(defines), civil_protection(class), civil_protection(handles) | RUNTIME_ONLY |
| DocumentArchived | DocumentArchived | Documentarchived | - | documents(defines), documents(class), documents(handles) | RUNTIME_ONLY |
| DocumentAuthenticated | DocumentAuthenticated | Documentauthenticated | - | documents(defines), documents(class), documents(handles) | RUNTIME_ONLY |
| DocumentRegistered | DocumentRegistered | Documentregistered | - | documents(defines), documents(class), documents(handles) | RUNTIME_ONLY |
| DocumentStatusChanged | DocumentStatusChanged | Documentstatuschanged | - | documents(defines), documents(class), documents(handles) | RUNTIME_ONLY |
| EconomicActivityStarted | EconomicActivityStarted | Economicactivitystarted | - | economy(defines), economy(class), economy(handles) | RUNTIME_ONLY |
| EconomicAgentRegistered | EconomicAgentRegistered | Economicagentregistered | - | economy(defines), economy(class), economy(handles) | RUNTIME_ONLY |
| EconomicAgentStatusChanged | EconomicAgentStatusChanged | Economicagentstatuschanged | - | economy(defines), economy(class), economy(handles) | RUNTIME_ONLY |
| EconomicLicenseObtained | EconomicLicenseObtained | Economiclicenseobtained | - | economy(defines), economy(class), economy(handles) | RUNTIME_ONLY |
| EducationInstitutionRegistered | EducationInstitutionRegistered | Educationinstitutionregistered | - | educacao(defines), educacao(class), educacao(handles) | RUNTIME_ONLY |
| EducationInstitutionStatusChanged | EducationInstitutionStatusChanged | Educationinstitutionstatuschanged | - | educacao(defines), educacao(class), educacao(handles) | RUNTIME_ONLY |
| EmergencyAlertIssued | EmergencyAlertIssued | Emergencyalertissued | - | civil_protection(defines), civil_protection(class), civil_protection(handles) | RUNTIME_ONLY |
| EnvironmentalImpactAssessmentApproved | EnvironmentalImpactAssessmentApproved | Environmentalimpactassessmentapproved | - | resources(defines), resources(class), resources(handles) | RUNTIME_ONLY |
| EnvironmentalPermitIssued | EnvironmentalPermitIssued | Environmentalpermitissued | - | industry(defines), industry(class), industry(handles) | RUNTIME_ONLY |
| EvacuationInitiated | EvacuationInitiated | Evacuationinitiated | - | civil_protection(defines), civil_protection(class), civil_protection(handles) | RUNTIME_ONLY |
| ExploitationLicenseIssued | ExploitationLicenseIssued | Exploitationlicenseissued | - | resources(defines), resources(class), resources(handles) | RUNTIME_ONLY |
| GovernmentDecisionMade | GovernmentDecisionMade | Governmentdecisionmade | - | governance(defines), governance(class), governance(handles) | RUNTIME_ONLY |
| HealthProviderRegistered | HealthProviderRegistered | Healthproviderregistered | - | saude(defines), saude(class), saude(handles) | RUNTIME_ONLY |
| HealthProviderStatusChanged | HealthProviderStatusChanged | Healthproviderstatuschanged | - | saude(defines), saude(class), saude(handles) | RUNTIME_ONLY |
| HealthVaccinationCompleted | HealthVaccinationCompleted | Healthvaccinationcompleted | - | saude(defines), saude(class), saude(handles) | RUNTIME_ONLY |
| IdentityCredentialIssued | IdentityCredentialIssued | Identitycredentialissued | educacao(consumes), identity(exposes) | identity(defines), identity(class), identity(handles) | VALID |
| IdentityDocumentRequested | IdentityDocumentRequested | Identitydocumentrequested | - | identity(defines), identity(class), identity(handles) | RUNTIME_ONLY |
| IdentityDocumentStatusChanged | IdentityDocumentStatusChanged | Identitydocumentstatuschanged | - | identity(defines), identity(class), identity(handles) | RUNTIME_ONLY |
| IdentityDocumentVerified | IdentityDocumentVerified | Identitydocumentverified | educacao(consumes), saude(consumes), justica(consumes), identity(exposes), payment(consumes), registo-civil(consumes), financas-impostos(consumes), administracao-local(consumes), seguranca-social(consumes), integracao-nacional(consumes), integracao-nacional-nif(consumes), apoio-empresarial(consumes), comercio(consumes), emprego(consumes), trabalho-inspecao(consumes) | identity(defines), identity(class), identity(handles) | VALID |
| IndustrialFacilityRegistered | IndustrialFacilityRegistered | Industrialfacilityregistered | - | industry(defines), industry(class), industry(handles) | RUNTIME_ONLY |
| IndustrialFacilityStatusChanged | IndustrialFacilityStatusChanged | Industrialfacilitystatuschanged | - | industry(defines), industry(class), industry(handles) | RUNTIME_ONLY |
| InvoiceIssued | InvoiceIssued | Invoiceissued | - | payment(defines), payment(class), payment(handles) | RUNTIME_ONLY |
| MarriageCertificateIssued | MarriageCertificateIssued | Marriagecertificateissued | - | justice(class), justice(handles) | RUNTIME_ONLY |
| MarriageRecorded | MarriageRecorded | Marriagerecorded | registo-civil(exposes) | justice(class), justice(handles) | VALID |
| MedicalLicenseIssued | MedicalLicenseIssued | Medicallicenseissued | - | saude(defines), saude(class), saude(handles) | RUNTIME_ONLY |
| MedicalVisitRecorded | MedicalVisitRecorded | Medicalvisitrecorded | - | saude(defines), saude(class), saude(handles) | RUNTIME_ONLY |
| OfficialDocumentIssued | OfficialDocumentIssued | Officialdocumentissued | - | documents(defines), documents(class), documents(handles) | RUNTIME_ONLY |
| OfficialRequiredActionIssued | OfficialRequiredActionIssued | Officialrequiredactionissued | - | governance(defines), governance(class), governance(handles) | RUNTIME_ONLY |
| PaymentConfirmed | PaymentConfirmed | Paymentconfirmed | - | administracao-local(handles) | RUNTIME_ONLY |
| PaymentProcessed | PaymentProcessed | Paymentprocessed | justica(consumes), identity(consumes), payment(exposes), financas-impostos(consumes), administracao-local(consumes), seguranca-social(consumes), apoio-empresarial(consumes), comercio(consumes) | payment(defines), payment(class), payment(handles) | VALID |
| PaymentReconciled | PaymentReconciled | Paymentreconciled | payment(exposes) | payment(defines), payment(class), payment(handles) | VALID |
| PaymentStatusChanged | PaymentStatusChanged | Paymentstatuschanged | - | payment(defines), payment(class), payment(handles) | RUNTIME_ONLY |
| PaymentTransactionInitiated | PaymentTransactionInitiated | Paymenttransactioninitiated | - | payment(defines), payment(class), payment(handles) | RUNTIME_ONLY |
| PolicyPublished | PolicyPublished | Policypublished | - | governance(defines), governance(class), governance(handles) | RUNTIME_ONLY |
| PublicServiceApproved | PublicServiceApproved | Publicserviceapproved | - | governance(defines), governance(class), governance(handles) | RUNTIME_ONLY |
| ResourceExplorationLicenseApplied | ResourceExplorationLicenseApplied | Resourceexplorationlicenseapplied | - | resources(defines), resources(class), resources(handles) | RUNTIME_ONLY |
| ResourceLicenseStatusChanged | ResourceLicenseStatusChanged | Resourcelicensestatuschanged | - | resources(defines), resources(class), resources(handles) | RUNTIME_ONLY |
| ResourceMonitoringReportFiled | ResourceMonitoringReportFiled | Resourcemonitoringreportfiled | - | resources(defines), resources(class), resources(handles) | RUNTIME_ONLY |
| SafetyCertificationIssued | SafetyCertificationIssued | Safetycertificationissued | - | industry(defines), industry(class), industry(handles) | RUNTIME_ONLY |
| SafetyInspectionConducted | SafetyInspectionConducted | Safetyinspectionconducted | - | industry(defines), industry(class), industry(handles) | RUNTIME_ONLY |
| StudentEnrolled | StudentEnrolled | Studentenrolled | educacao(exposes), saude(consumes), payment(consumes) | educacao(defines), educacao(class), administracao-local(handles), educacao(handles), identity(handles) | VALID |
| TaxRegistrationIssued | TaxRegistrationIssued | Taxregistrationissued | - | economy(defines), economy(class), economy(handles) | RUNTIME_ONLY |
| TeacherCertificationIssued | TeacherCertificationIssued | Teachercertificationissued | - | educacao(defines), educacao(class), educacao(handles) | RUNTIME_ONLY |
| appointment_scheduled | appointment_scheduled | N/A | saude(exposes) | - | REGISTRY_ONLY |
| benefit_granted | benefit_granted | N/A | seguranca-social(exposes) | - | REGISTRY_ONLY |
| bi_consulted | bi_consulted | N/A | integracao-nacional(exposes) | - | REGISTRY_ONLY |
| bi_verified | bi_verified | N/A | integracao-nacional(exposes) | - | REGISTRY_ONLY |
| business_support_granted | business_support_granted | N/A | apoio-empresarial(exposes) | - | REGISTRY_ONLY |
| certificate_issued | certificate_issued | N/A | educacao(exposes) | - | REGISTRY_ONLY |
| civil_registration_issued | civil_registration_issued | N/A | justica(exposes) | - | REGISTRY_ONLY |
| commercial_license_issued | commercial_license_issued | N/A | apoio-empresarial(exposes) | - | REGISTRY_ONLY |
| company_incorporated | company_incorporated | N/A | justica(exposes), financas-impostos(consumes), seguranca-social(consumes) | - | REGISTRY_ONLY |
| company_registered | company_registered | N/A | apoio-empresarial(exposes), comercio(consumes) | - | REGISTRY_ONLY |
| employer_registered | employer_registered | N/A | seguranca-social(exposes), emprego(consumes), trabalho-inspecao(consumes) | - | REGISTRY_ONLY |
| employment_contract_registered | employment_contract_registered | N/A | emprego(exposes), trabalho-inspecao(consumes) | - | REGISTRY_ONLY |
| fine_issued | fine_issued | N/A | trabalho-inspecao(exposes) | - | REGISTRY_ONLY |
| inspection_completed | inspection_completed | N/A | comercio(exposes), trabalho-inspecao(exposes) | - | REGISTRY_ONLY |
| inspection_scheduled | inspection_scheduled | N/A | trabalho-inspecao(exposes) | - | REGISTRY_ONLY |
| invoice_status_changed | invoice_status_changed | N/A | payment(exposes) | - | REGISTRY_ONLY |
| job_vacancy_created | job_vacancy_created | N/A | emprego(exposes) | - | REGISTRY_ONLY |
| license_issued | license_issued | N/A | administracao-local(exposes) | - | REGISTRY_ONLY |
| license_permit_issued | license_permit_issued | N/A | comercio(exposes) | - | REGISTRY_ONLY |
| municipal_certificate_issued | municipal_certificate_issued | N/A | administracao-local(exposes) | - | REGISTRY_ONLY |
| nif_issued | nif_issued | N/A | payment(consumes), financas-impostos(exposes), integracao-nacional-nif(consumes), apoio-empresarial(consumes) | - | REGISTRY_ONLY |
| nif_verified | nif_verified | N/A | integracao-nacional-nif(exposes) | - | REGISTRY_ONLY |
| notarial_act_signed | notarial_act_signed | N/A | justica(exposes) | - | REGISTRY_ONLY |
| payment_failed | payment_failed | N/A | payment(exposes) | - | REGISTRY_ONLY |
| placement_completed | placement_completed | N/A | emprego(exposes) | - | REGISTRY_ONLY |
| prescription_issued | prescription_issued | N/A | saude(exposes) | - | REGISTRY_ONLY |
| referral_made | referral_made | N/A | saude(exposes) | - | REGISTRY_ONLY |
| residence_confirmed | residence_confirmed | N/A | administracao-local(exposes) | - | REGISTRY_ONLY |
| social_contribution_received | social_contribution_received | N/A | seguranca-social(exposes) | - | REGISTRY_ONLY |
| student_transferred | student_transferred | N/A | educacao(exposes) | - | REGISTRY_ONLY |
| tax_declaration_submitted | tax_declaration_submitted | N/A | financas-impostos(exposes) | - | REGISTRY_ONLY |
| tax_payment_received | tax_payment_received | N/A | financas-impostos(exposes) | - | REGISTRY_ONLY |
| trade_registered | trade_registered | N/A | comercio(exposes) | - | REGISTRY_ONLY |

## Eventos REGISTRY_ONLY (Ghost Events)

Estes eventos existem no RegistryCatalog mas NAO existem no codigo runtime:

| Evento | Publisher (Registry) | Subscribers (Registry) | Acao |
|---|---|---|---|
| appointment_scheduled | saude(exposes) | - | CORRIGIR alias ou REMOVER |
| benefit_granted | seguranca-social(exposes) | - | CORRIGIR alias ou REMOVER |
| bi_consulted | integracao-nacional(exposes) | - | CORRIGIR alias ou REMOVER |
| bi_verified | integracao-nacional(exposes) | - | CORRIGIR alias ou REMOVER |
| business_support_granted | apoio-empresarial(exposes) | - | CORRIGIR alias ou REMOVER |
| certificate_issued | educacao(exposes) | - | CORRIGIR alias ou REMOVER |
| civil_registration_issued | justica(exposes) | - | CORRIGIR alias ou REMOVER |
| commercial_license_issued | apoio-empresarial(exposes) | - | CORRIGIR alias ou REMOVER |
| company_incorporated | justica(exposes) | financas-impostos(consumes), seguranca-social(consumes) | CORRIGIR alias ou REMOVER |
| company_registered | apoio-empresarial(exposes) | comercio(consumes) | CORRIGIR alias ou REMOVER |
| employer_registered | seguranca-social(exposes) | emprego(consumes), trabalho-inspecao(consumes) | CORRIGIR alias ou REMOVER |
| employment_contract_registered | emprego(exposes) | trabalho-inspecao(consumes) | CORRIGIR alias ou REMOVER |
| fine_issued | trabalho-inspecao(exposes) | - | CORRIGIR alias ou REMOVER |
| inspection_completed | comercio(exposes), trabalho-inspecao(exposes) | - | CORRIGIR alias ou REMOVER |
| inspection_scheduled | trabalho-inspecao(exposes) | - | CORRIGIR alias ou REMOVER |
| invoice_status_changed | payment(exposes) | - | CORRIGIR alias ou REMOVER |
| job_vacancy_created | emprego(exposes) | - | CORRIGIR alias ou REMOVER |
| license_issued | administracao-local(exposes) | - | CORRIGIR alias ou REMOVER |
| license_permit_issued | comercio(exposes) | - | CORRIGIR alias ou REMOVER |
| municipal_certificate_issued | administracao-local(exposes) | - | CORRIGIR alias ou REMOVER |
| nif_issued | financas-impostos(exposes) | payment(consumes), integracao-nacional-nif(consumes), apoio-empresarial(consumes) | CORRIGIR alias ou REMOVER |
| nif_verified | integracao-nacional-nif(exposes) | - | CORRIGIR alias ou REMOVER |
| notarial_act_signed | justica(exposes) | - | CORRIGIR alias ou REMOVER |
| payment_failed | payment(exposes) | - | CORRIGIR alias ou REMOVER |
| placement_completed | emprego(exposes) | - | CORRIGIR alias ou REMOVER |
| prescription_issued | saude(exposes) | - | CORRIGIR alias ou REMOVER |
| referral_made | saude(exposes) | - | CORRIGIR alias ou REMOVER |
| residence_confirmed | administracao-local(exposes) | - | CORRIGIR alias ou REMOVER |
| social_contribution_received | seguranca-social(exposes) | - | CORRIGIR alias ou REMOVER |
| student_transferred | educacao(exposes) | - | CORRIGIR alias ou REMOVER |
| tax_declaration_submitted | financas-impostos(exposes) | - | CORRIGIR alias ou REMOVER |
| tax_payment_received | financas-impostos(exposes) | - | CORRIGIR alias ou REMOVER |
| trade_registered | comercio(exposes) | - | CORRIGIR alias ou REMOVER |

## Eventos NAME_MISMATCH

Estes eventos tem nomes diferentes entre Registry (snake_case) e Runtime (PascalCase):

| Registry Name | Runtime Name | Modulos Afetados | Acao |
|---|---|---|---|

## Eventos RUNTIME_ONLY

Estes eventos existem no codigo runtime mas NAO estao no RegistryCatalog:

| Evento | Modulo | Acao |
|---|---|---|
| APIAccessTokenIssued | api(defines), api(class) | Adicionar ao RegistryCatalog |
| APIEndpointRegistered | api(defines), api(class) | Adicionar ao RegistryCatalog |
| APIEndpointStatusChanged | api(defines), api(class) | Adicionar ao RegistryCatalog |
| APIRequestProcessed | api(defines), api(class) | Adicionar ao RegistryCatalog |
| APISecurityPolicyEnforced | api(defines), api(class) | Adicionar ao RegistryCatalog |
| AcademicDegreeAwarded | educacao(defines), educacao(class), educacao(handles) | Adicionar ao RegistryCatalog |
| AdminOfficeStatusChanged | governance(defines), governance(class), governance(handles) | Adicionar ao RegistryCatalog |
| AuditExecutionStarted | audit(defines), audit(class), audit(handles) | Adicionar ao RegistryCatalog |
| AuditFindingReported | audit(defines), audit(class), audit(handles) | Adicionar ao RegistryCatalog |
| AuditProgramCreated | audit(defines), audit(class), audit(handles) | Adicionar ao RegistryCatalog |
| AuditReportSubmitted | audit(defines), audit(class), audit(handles) | Adicionar ao RegistryCatalog |
| BirthRecordCertificateIssued | justice(class), justice(handles) | Adicionar ao RegistryCatalog |
| CitizenCreated | justice(class), justice(handles) | Adicionar ao RegistryCatalog |
| CitizenIdentityDocumentIssued | justice(class), justice(handles) | Adicionar ao RegistryCatalog |
| CitizenStatusChanged | justice(class) | Adicionar ao RegistryCatalog |
| CivilProtectionResourceStatusChanged | civil_protection(defines), civil_protection(class), civil_protection(handles) | Adicionar ao RegistryCatalog |
| ComplianceCertificateIssued | compliance(defines), compliance(class), compliance(handles) | Adicionar ao RegistryCatalog |
| ComplianceInspectionConducted | compliance(defines), compliance(class), compliance(handles) | Adicionar ao RegistryCatalog |
| ComplianceObligationCreated | compliance(defines), compliance(class), compliance(handles) | Adicionar ao RegistryCatalog |
| ComplianceObligationStatusChanged | compliance(defines), compliance(class), compliance(handles) | Adicionar ao RegistryCatalog |
| ComplianceViolationReported | compliance(defines), compliance(class), compliance(handles) | Adicionar ao RegistryCatalog |
| ControllerRecommendationIssued | audit(defines), audit(class), audit(handles) | Adicionar ao RegistryCatalog |
| DeathCertificateIssued | justice(class), justice(handles) | Adicionar ao RegistryCatalog |
| DisasterEventOccurred | civil_protection(defines), civil_protection(class), civil_protection(handles) | Adicionar ao RegistryCatalog |
| DisasterRecoveryInitiated | civil_protection(defines), civil_protection(class), civil_protection(handles) | Adicionar ao RegistryCatalog |
| DocumentArchived | documents(defines), documents(class), documents(handles) | Adicionar ao RegistryCatalog |
| DocumentAuthenticated | documents(defines), documents(class), documents(handles) | Adicionar ao RegistryCatalog |
| DocumentRegistered | documents(defines), documents(class), documents(handles) | Adicionar ao RegistryCatalog |
| DocumentStatusChanged | documents(defines), documents(class), documents(handles) | Adicionar ao RegistryCatalog |
| EconomicActivityStarted | economy(defines), economy(class), economy(handles) | Adicionar ao RegistryCatalog |
| EconomicAgentRegistered | economy(defines), economy(class), economy(handles) | Adicionar ao RegistryCatalog |
| EconomicAgentStatusChanged | economy(defines), economy(class), economy(handles) | Adicionar ao RegistryCatalog |
| EconomicLicenseObtained | economy(defines), economy(class), economy(handles) | Adicionar ao RegistryCatalog |
| EducationInstitutionRegistered | educacao(defines), educacao(class), educacao(handles) | Adicionar ao RegistryCatalog |
| EducationInstitutionStatusChanged | educacao(defines), educacao(class), educacao(handles) | Adicionar ao RegistryCatalog |
| EmergencyAlertIssued | civil_protection(defines), civil_protection(class), civil_protection(handles) | Adicionar ao RegistryCatalog |
| EnvironmentalImpactAssessmentApproved | resources(defines), resources(class), resources(handles) | Adicionar ao RegistryCatalog |
| EnvironmentalPermitIssued | industry(defines), industry(class), industry(handles) | Adicionar ao RegistryCatalog |
| EvacuationInitiated | civil_protection(defines), civil_protection(class), civil_protection(handles) | Adicionar ao RegistryCatalog |
| ExploitationLicenseIssued | resources(defines), resources(class), resources(handles) | Adicionar ao RegistryCatalog |
| GovernmentDecisionMade | governance(defines), governance(class), governance(handles) | Adicionar ao RegistryCatalog |
| HealthProviderRegistered | saude(defines), saude(class), saude(handles) | Adicionar ao RegistryCatalog |
| HealthProviderStatusChanged | saude(defines), saude(class), saude(handles) | Adicionar ao RegistryCatalog |
| HealthVaccinationCompleted | saude(defines), saude(class), saude(handles) | Adicionar ao RegistryCatalog |
| IdentityDocumentRequested | identity(defines), identity(class), identity(handles) | Adicionar ao RegistryCatalog |
| IdentityDocumentStatusChanged | identity(defines), identity(class), identity(handles) | Adicionar ao RegistryCatalog |
| IndustrialFacilityRegistered | industry(defines), industry(class), industry(handles) | Adicionar ao RegistryCatalog |
| IndustrialFacilityStatusChanged | industry(defines), industry(class), industry(handles) | Adicionar ao RegistryCatalog |
| InvoiceIssued | payment(defines), payment(class), payment(handles) | Adicionar ao RegistryCatalog |
| MarriageCertificateIssued | justice(class), justice(handles) | Adicionar ao RegistryCatalog |
| MedicalLicenseIssued | saude(defines), saude(class), saude(handles) | Adicionar ao RegistryCatalog |
| MedicalVisitRecorded | saude(defines), saude(class), saude(handles) | Adicionar ao RegistryCatalog |
| OfficialDocumentIssued | documents(defines), documents(class), documents(handles) | Adicionar ao RegistryCatalog |
| OfficialRequiredActionIssued | governance(defines), governance(class), governance(handles) | Adicionar ao RegistryCatalog |
| PaymentConfirmed | administracao-local(handles) | Adicionar ao RegistryCatalog |
| PaymentStatusChanged | payment(defines), payment(class), payment(handles) | Adicionar ao RegistryCatalog |
| PaymentTransactionInitiated | payment(defines), payment(class), payment(handles) | Adicionar ao RegistryCatalog |
| PolicyPublished | governance(defines), governance(class), governance(handles) | Adicionar ao RegistryCatalog |
| PublicServiceApproved | governance(defines), governance(class), governance(handles) | Adicionar ao RegistryCatalog |
| ResourceExplorationLicenseApplied | resources(defines), resources(class), resources(handles) | Adicionar ao RegistryCatalog |
| ResourceLicenseStatusChanged | resources(defines), resources(class), resources(handles) | Adicionar ao RegistryCatalog |
| ResourceMonitoringReportFiled | resources(defines), resources(class), resources(handles) | Adicionar ao RegistryCatalog |
| SafetyCertificationIssued | industry(defines), industry(class), industry(handles) | Adicionar ao RegistryCatalog |
| SafetyInspectionConducted | industry(defines), industry(class), industry(handles) | Adicionar ao RegistryCatalog |
| TaxRegistrationIssued | economy(defines), economy(class), economy(handles) | Adicionar ao RegistryCatalog |
| TeacherCertificationIssued | educacao(defines), educacao(class), educacao(handles) | Adicionar ao RegistryCatalog |

## Plano de Correcacao

### Acao 1: Corrigir `citizen_updated`
- Registry: `identity` expoe `citizen_updated` (consumido por 11 modulos)
- Runtime: NAO EXISTE. Identity module define `IdentityDocumentVerified`, `IdentityDocumentStatusChanged`, etc.
- Solucao: 
  - Renomear no RegistryCatalog: `citizen_updated` -> `IdentityDocumentVerified`
  - Ou adicionar alias: registry guarda ambos os nomes

### Acao 2: Corrigir `identity_verified`
- Registry: `identity` expoe `identity_verified` (consumido por 11 modulos)
- Runtime: NAO EXISTE como string. A classe `IdentityDocumentVerified` existe.
- Solucao:
  - Renomear: `identity_verified` -> `IdentityDocumentVerified`

### Acao 3: RegistryCatalog sync
- Adicionar todos os eventos RUNTIME_ONLY ao RegistryCatalog
- Remover ou criar alias para eventos REGISTRY_ONLY

### Acao 4: Automacao
- Criar script `scripts/sync_events.py` que valida registry vs runtime
- Integrar no `make daily-audit`
