# EVENT CLASSIFICATION REPORT

> Gerado em: 2026-06-08
> Proposito: Classificar todos os eventos do sistema SILA em GOVERNANCE_ONLY, RUNTIME_ONLY, SHOULD_BE_RUNTIME, DEPRECATED

---

## Resumo

| Categoria | Quantidade |
|---|---|
| VALID (ja reconciliados) | 9 |
| SHOULD_BE_RUNTIME | 15 |
| GOVERNANCE_ONLY | 21 |
| DEPRECATED | 0 |
| RUNTIME_ONLY (ja existem em runtime) | 66 |
| **Total** | **111** |

---

## SHOULD_BE_RUNTIME

Eventos nacionais centrais que DEVEM ganhar implementacao runtime (classe de evento + handler).

| # | Evento | Registry Refs | Modulo | Prioridade |
|---|---|---|---|---|
| 1 | nif_issued | 4 refs | integracao-nacional-nif, payment, apoio-empresarial, financas-impostos | P1 |
| 2 | company_incorporated | 3 refs | seguranca-social, justica, financas-impostos | P1 |
| 3 | employer_registered | 3 refs | emprego, trabalho-inspecao, seguranca-social | P1 |
| 4 | company_registered | 2 refs | apoio-empresarial, comercio | P2 |
| 5 | employment_contract_registered | 2 refs | emprego, trabalho-inspecao | P2 |
| 6 | benefit_granted | 1 refs | seguranca-social | P3 |
| 7 | certificate_issued | 1 refs | educacao | P3 |
| 8 | invoice_status_changed | 1 refs | payment | P3 |
| 9 | license_issued | 1 refs | administracao-local | P3 |
| 10 | payment_failed | 1 refs | payment | P3 |
| 11 | tax_declaration_submitted | 1 refs | financas-impostos | P3 |
| 12 | tax_payment_received | 1 refs | financas-impostos | P3 |
| 13 | **enrollment_completed** (MISSING) | 0 refs - CRIAR | educacao | P1 - NOVO |
| 14 | **pension_granted** (MISSING) | 0 refs - CRIAR | seguranca-social | P1 - NOVO |
| 15 | **procurement_awarded** (MISSING) | 0 refs - CRIAR | procurement | P1 - NOVO |

## GOVERNANCE_ONLY

Eventos exclusivos do RegistryCatalog - contratos validos entre modulos, sem necessidade imediata de classe runtime.

| # | Evento | Registry Refs | Modulo Publisher |
|---|---|---|---|
| 1 | appointment_scheduled | 1 refs | saude |
| 2 | bi_consulted | 1 refs | integracao-nacional |
| 3 | bi_verified | 1 refs | integracao-nacional |
| 4 | business_support_granted | 1 refs | apoio-empresarial |
| 5 | civil_registration_issued | 1 refs | justica |
| 6 | commercial_license_issued | 1 refs | apoio-empresarial |
| 7 | fine_issued | 1 refs | trabalho-inspecao |
| 8 | inspection_completed | 2 refs | comercio |
| 9 | inspection_scheduled | 1 refs | trabalho-inspecao |
| 10 | job_vacancy_created | 1 refs | emprego |
| 11 | license_permit_issued | 1 refs | comercio |
| 12 | municipal_certificate_issued | 1 refs | administracao-local |
| 13 | nif_verified | 1 refs | integracao-nacional-nif |
| 14 | notarial_act_signed | 1 refs | justica |
| 15 | placement_completed | 1 refs | emprego |
| 16 | prescription_issued | 1 refs | saude |
| 17 | referral_made | 1 refs | saude |
| 18 | residence_confirmed | 1 refs | administracao-local |
| 19 | social_contribution_received | 1 refs | seguranca-social |
| 20 | student_transferred | 1 refs | educacao |
| 21 | trade_registered | 1 refs | comercio |

## RUNTIME_ONLY

Eventos que ja existem em runtime mas nao estao registados no RegistryCatalog. Precisam de ser adicionados ao bootstrap.py.

| # | Evento | Runtime Refs |
|---|---|---|
| 1 | APIAccessTokenIssued | api(defines), api(class) |
| 2 | APIEndpointRegistered | api(defines), api(class) |
| 3 | APIEndpointStatusChanged | api(defines), api(class) |
| 4 | APIRequestProcessed | api(defines), api(class) |
| 5 | APISecurityPolicyEnforced | api(defines), api(class) |
| 6 | AcademicDegreeAwarded | educacao(defines), educacao(class), educacao(handles) |
| 7 | AdminOfficeStatusChanged | governance(defines), governance(class), governance(handles) |
| 8 | AuditExecutionStarted | audit(defines), audit(class), audit(handles) |
| 9 | AuditFindingReported | audit(defines), audit(class), audit(handles) |
| 10 | AuditProgramCreated | audit(defines), audit(class), audit(handles) |
| 11 | AuditReportSubmitted | audit(defines), audit(class), audit(handles) |
| 12 | BirthRecordCertificateIssued | justice(class), justice(handles) |
| 13 | CitizenCreated | justice(class), justice(handles) |
| 14 | CitizenIdentityDocumentIssued | justice(class), justice(handles) |
| 15 | CitizenStatusChanged | justice(class) |
| 16 | CivilProtectionResourceStatusChanged | civil_protection(defines), civil_protection(class), civil_protection(handles) |
| 17 | ComplianceCertificateIssued | compliance(defines), compliance(class), compliance(handles) |
| 18 | ComplianceInspectionConducted | compliance(defines), compliance(class), compliance(handles) |
| 19 | ComplianceObligationCreated | compliance(defines), compliance(class), compliance(handles) |
| 20 | ComplianceObligationStatusChanged | compliance(defines), compliance(class), compliance(handles) |
| 21 | ComplianceViolationReported | compliance(defines), compliance(class), compliance(handles) |
| 22 | ControllerRecommendationIssued | audit(defines), audit(class), audit(handles) |
| 23 | DeathCertificateIssued | justice(class), justice(handles) |
| 24 | DisasterEventOccurred | civil_protection(defines), civil_protection(class), civil_protection(handles) |
| 25 | DisasterRecoveryInitiated | civil_protection(defines), civil_protection(class), civil_protection(handles) |
| 26 | DocumentArchived | documents(defines), documents(class), documents(handles) |
| 27 | DocumentAuthenticated | documents(defines), documents(class), documents(handles) |
| 28 | DocumentRegistered | documents(defines), documents(class), documents(handles) |
| 29 | DocumentStatusChanged | documents(defines), documents(class), documents(handles) |
| 30 | EconomicActivityStarted | economy(defines), economy(class), economy(handles) |
| 31 | EconomicAgentRegistered | economy(defines), economy(class), economy(handles) |
| 32 | EconomicAgentStatusChanged | economy(defines), economy(class), economy(handles) |
| 33 | EconomicLicenseObtained | economy(defines), economy(class), economy(handles) |
| 34 | EducationInstitutionRegistered | educacao(defines), educacao(class), educacao(handles) |
| 35 | EducationInstitutionStatusChanged | educacao(defines), educacao(class), educacao(handles) |
| 36 | EmergencyAlertIssued | civil_protection(defines), civil_protection(class), civil_protection(handles) |
| 37 | EnvironmentalImpactAssessmentApproved | resources(defines), resources(class), resources(handles) |
| 38 | EnvironmentalPermitIssued | industry(defines), industry(class), industry(handles) |
| 39 | EvacuationInitiated | civil_protection(defines), civil_protection(class), civil_protection(handles) |
| 40 | ExploitationLicenseIssued | resources(defines), resources(class), resources(handles) |
| 41 | GovernmentDecisionMade | governance(defines), governance(class), governance(handles) |
| 42 | HealthProviderRegistered | saude(defines), saude(class), saude(handles) |
| 43 | HealthProviderStatusChanged | saude(defines), saude(class), saude(handles) |
| 44 | HealthVaccinationCompleted | saude(defines), saude(class), saude(handles) |
| 45 | IdentityDocumentRequested | identity(defines), identity(class), identity(handles) |
| 46 | IdentityDocumentStatusChanged | identity(defines), identity(class), identity(handles) |
| 47 | IndustrialFacilityRegistered | industry(defines), industry(class), industry(handles) |
| 48 | IndustrialFacilityStatusChanged | industry(defines), industry(class), industry(handles) |
| 49 | InvoiceIssued | payment(defines), payment(class), payment(handles) |
| 50 | MarriageCertificateIssued | justice(class), justice(handles) |
| 51 | MedicalLicenseIssued | saude(defines), saude(class), saude(handles) |
| 52 | MedicalVisitRecorded | saude(defines), saude(class), saude(handles) |
| 53 | OfficialDocumentIssued | documents(defines), documents(class), documents(handles) |
| 54 | OfficialRequiredActionIssued | governance(defines), governance(class), governance(handles) |
| 55 | PaymentConfirmed | administracao-local(handles) |
| 56 | PaymentStatusChanged | payment(defines), payment(class), payment(handles) |
| 57 | PaymentTransactionInitiated | payment(defines), payment(class), payment(handles) |
| 58 | PolicyPublished | governance(defines), governance(class), governance(handles) |
| 59 | PublicServiceApproved | governance(defines), governance(class), governance(handles) |
| 60 | ResourceExplorationLicenseApplied | resources(defines), resources(class), resources(handles) |
| 61 | ResourceLicenseStatusChanged | resources(defines), resources(class), resources(handles) |
| 62 | ResourceMonitoringReportFiled | resources(defines), resources(class), resources(handles) |
| 63 | SafetyCertificationIssued | industry(defines), industry(class), industry(handles) |
| 64 | SafetyInspectionConducted | industry(defines), industry(class), industry(handles) |
| 65 | TaxRegistrationIssued | economy(defines), economy(class), economy(handles) |
| 66 | TeacherCertificationIssued | educacao(defines), educacao(class), educacao(handles) |

## DEPRECATED

Nenhum evento classificado como DEPRECATED. Todos os 33 REGISTRY_ONLY tem pelo menos um publisher registado.

*Nota:* Eventos sem publisher nem consumer real serao marcados como DEPRECATED numa auditoria futura.

## VALID

Eventos totalmente reconciliados (Registry + Runtime).

| # | Evento | Registry Refs | Runtime Refs |
|---|---|---|---|
| 1 | BiometricDataEnrolled | identity(exposes) | identity(defines), identity(class), identity(handles) |
| 2 | BirthRecordCreated | identity(consumes), registo-civil(exposes) | justice(class), justice(handles) |
| 3 | DeathRecorded | identity(consumes), registo-civil(exposes) | justice(class), justice(handles) |
| 4 | IdentityCredentialIssued | educacao(consumes), identity(exposes) | identity(defines), identity(class), identity(handles) |
| 5 | IdentityDocumentVerified | educacao(consumes), saude(consumes), justica(consumes), identity(exposes), payment(consumes), registo-civil(consumes), financas-impostos(consumes), administracao-local(consumes), seguranca-social(consumes), integracao-nacional(consumes), integracao-nacional-nif(consumes), apoio-empresarial(consumes), comercio(consumes), emprego(consumes), trabalho-inspecao(consumes) | identity(defines), identity(class), identity(handles) |
| 6 | MarriageRecorded | registo-civil(exposes) | justice(class), justice(handles) |
| 7 | PaymentProcessed | justica(consumes), identity(consumes), payment(exposes), financas-impostos(consumes), administracao-local(consumes), seguranca-social(consumes), apoio-empresarial(consumes), comercio(consumes) | payment(defines), payment(class), payment(handles) |
| 8 | PaymentReconciled | payment(exposes) | payment(defines), payment(class), payment(handles) |
| 9 | StudentEnrolled | educacao(exposes), saude(consumes), payment(consumes) | educacao(defines), educacao(class), administracao-local(handles), educacao(handles), identity(handles) |

---

## Criterios de Classificacao

| Categoria | Criterio |
|---|---|
| **SHOULD_BE_RUNTIME** | Eventos nacionais centrais com alta relevancia transversal (nif, empresa, certificado, beneficio, licenca). Inclui eventos com multiplas referecias cross-module e eventos nacionais especificados como prioritarios pelo dominio. |
| **GOVERNANCE_ONLY** | Eventos de dominio especifico que validam contratos entre modulos mas nao necessitam de classe runtime dedicada. A semantica do evento e totalmente capturada pelos eventos runtime existentes nesse modulo. |
| **RUNTIME_ONLY** | Eventos com implementacao runtime completa (classe + class + handler) mas ausentes do RegistryCatalog. Acao necessaria: adicionar ao bootstrap.py. |
| **DEPRECATED** | Eventos sem publisher nem consumer real. Nenhum identificado nesta auditoria. |
