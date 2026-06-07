# Validacao Ministerial — Nucleo do Estado Digital

_Gerado em: 2026-06-07 09:23:04.641475_

## Resumo

| Ministerio | Modulo | RBAC | Territorio | Aprovacao | Delegacao | Auditoria | Assinatura | Eventos | Organizacoes | Score |
|---|---|---|---|---|---|---|---|---|---|---|
| Ministerio da Educacao | educacao | [##########] 8/8| [##########] 5/5| [##########] 2/2| [##########] 6/6| [##########] 2/2| [##########] 2/2| [##########] 3/3| [##########] 3/3| **100%** |
| Ministerio da Saude | saude | [##########] 8/8| [##########] 4/4| [##########] 2/2| [##########] 6/6| [##########] 2/2| [##########] 2/2| [##########] 2/2| [##########] 3/3| **100%** |
| Ministerio da Justica e dos Direitos Humanos | justica | [##########] 8/8| [##########] 4/4| [##########] 2/2| [##########] 6/6| [##########] 2/2| [##########] 2/2| [##########] 3/3| [##########] 3/3| **100%** |
| Ministerio das Financas | financas-impostos | [##########] 6/6| [##########] 4/4| [##########] 2/2| [##########] 5/5| [##########] 2/2| [##########] 2/2| [##########] 3/3| [##########] 1/1| **100%** |
| Ministerio da Administracao Territorial | administracao-local | [##########] 4/4| [##########] 5/5| [##########] 2/2| [##########] 4/4| [##########] 2/2| [##########] 2/2| [##########] 2/2| [##########] 1/1| **100%** |
| Ministerio da Adm. Publica e Seguranca Social | seguranca-social | [##########] 8/8| [##########] 5/5| [##########] 2/2| [##########] 6/6| [##########] 2/2| [##########] 2/2| [##########] 3/3| [##########] 2/2| **100%** |

## Detalhe por Ministerio

### Ministerio da Educacao (`educacao`)
**Score: 100%** (31/31 checks)

| Check | Status | Descricao |
|---|---|---|
| role_role_ministerio | PASS | Role ROLE_MINISTERIO definida |
| role_role_provincia | PASS | Role ROLE_PROVINCIA definida |
| role_role_municipio | PASS | Role ROLE_MUNICIPIO definida |
| role_role_escola | PASS | Role ROLE_ESCOLA definida |
| rbac_hierarchy_ministerio | PASS | Role ROLE_MINISTERIO mapeavel para RoleGovernance |
| rbac_hierarchy_provincia | PASS | Role ROLE_PROVINCIA mapeavel para RoleGovernance |
| rbac_hierarchy_municipio | PASS | Role ROLE_MUNICIPIO mapeavel para RoleGovernance |
| rbac_hierarchy_escola | PASS | Role ROLE_ESCOLA mapeavel para RoleGovernance |
| territorial_model | PASS | Modelo territorial correto: nacional_provincial_municipal_unidade |
| nivel_nacional | PASS | Nivel territorial 'nacional' disponivel |
| nivel_provincial | PASS | Nivel territorial 'provincial' disponivel |
| nivel_municipal | PASS | Nivel territorial 'municipal' disponivel |
| nivel_unidade | PASS | Nivel territorial 'unidade' disponivel |
| approval_chain | PASS | Cadeia definida: escola -> municipio -> provincia |
| approval_chain_pending | PASS | Aprovacao inicial corretamente pendente |
| delegation_engine | PASS | DelegationEngine disponivel |
| delegation_role_role_ministerio | PASS | Role ROLE_MINISTERIO pode delegar/ receber delegacao |
| delegation_role_role_provincia | PASS | Role ROLE_PROVINCIA pode delegar/ receber delegacao |
| delegation_role_role_municipio | PASS | Role ROLE_MUNICIPIO pode delegar/ receber delegacao |
| delegation_role_role_escola | PASS | Role ROLE_ESCOLA pode delegar/ receber delegacao |
| delegation_hierarchy | PASS | Delegacao hierarquica funcional (nivel superior -> inferior) |
| audit_logger | PASS | AuditLogger operacional |
| audit_trail | PASS | Trilha de auditoria funcional |
| digital_signature | PASS | Assinatura digital funcional |
| signature_verification | PASS | Verificacao de assinatura funcional |
| exposed_events | PASS | Eventos expostos: 3 |
| consumed_events | PASS | Eventos consumidos: 3 |
| event_student_enrolled | PASS | Evento 'student_enrolled' tem consumidores |
| org_mined | PASS | Organizacao 'Ministério da Educação' registada |
| org_dpe-huambo | PASS | Organizacao 'Direção Provincial da Educação do Huambo' registada |
| org_dme-caala | PASS | Organizacao 'Direção Municipal da Educação da Caála' registada |

**Configuracao atual:**

- Dono: Ministério da Educação (MINED)
- Modelo territorial: nacional_provincial_municipal_unidade
- Cadeia de aprovacao: escola -> municipio -> provincia
- Servicos: matricula, transferencia, certificado, declaracao
- Expõe: student_enrolled, student_transferred, certificate_issued
- Consome: citizen_updated, identity_verified, bi_issued

### Ministerio da Saude (`saude`)
**Score: 100%** (29/29 checks)

| Check | Status | Descricao |
|---|---|---|
| role_role_ministerio | PASS | Role ROLE_MINISTERIO definida |
| role_role_provincia | PASS | Role ROLE_PROVINCIA definida |
| role_role_municipio | PASS | Role ROLE_MUNICIPIO definida |
| role_role_unidade | PASS | Role ROLE_UNIDADE definida |
| rbac_hierarchy_ministerio | PASS | Role ROLE_MINISTERIO mapeavel para RoleGovernance |
| rbac_hierarchy_provincia | PASS | Role ROLE_PROVINCIA mapeavel para RoleGovernance |
| rbac_hierarchy_municipio | PASS | Role ROLE_MUNICIPIO mapeavel para RoleGovernance |
| rbac_hierarchy_unidade | PASS | Role ROLE_UNIDADE mapeavel para RoleGovernance |
| territorial_model | PASS | Modelo territorial correto: nacional_provincial_unidade |
| nivel_nacional | PASS | Nivel territorial 'nacional' disponivel |
| nivel_provincial | PASS | Nivel territorial 'provincial' disponivel |
| nivel_unidade | PASS | Nivel territorial 'unidade' disponivel |
| approval_chain | PASS | Cadeia definida: unidade -> municipio -> provincia |
| approval_chain_pending | PASS | Aprovacao inicial corretamente pendente |
| delegation_engine | PASS | DelegationEngine disponivel |
| delegation_role_role_ministerio | PASS | Role ROLE_MINISTERIO pode delegar/ receber delegacao |
| delegation_role_role_provincia | PASS | Role ROLE_PROVINCIA pode delegar/ receber delegacao |
| delegation_role_role_municipio | PASS | Role ROLE_MUNICIPIO pode delegar/ receber delegacao |
| delegation_role_role_unidade | PASS | Role ROLE_UNIDADE pode delegar/ receber delegacao |
| delegation_hierarchy | PASS | Delegacao hierarquica funcional (nivel superior -> inferior) |
| audit_logger | PASS | AuditLogger operacional |
| audit_trail | PASS | Trilha de auditoria funcional |
| digital_signature | PASS | Assinatura digital funcional |
| signature_verification | PASS | Verificacao de assinatura funcional |
| exposed_events | PASS | Eventos expostos: 3 |
| consumed_events | PASS | Eventos consumidos: 3 |
| org_minsa | PASS | Organizacao 'Ministério da Saúde' registada |
| org_dps-huambo | PASS | Organizacao 'Direção Provincial da Saúde do Huambo' registada |
| org_hospital-huambo | PASS | Organizacao 'Hospital Geral do Huambo' registada |

**Configuracao atual:**

- Dono: Ministério da Saúde (MINSA)
- Modelo territorial: nacional_provincial_unidade
- Cadeia de aprovacao: unidade -> municipio -> provincia
- Servicos: marcacao_consulta, receituario, referenciacao, internamento
- Expõe: appointment_scheduled, prescription_issued, referral_made
- Consome: citizen_updated, identity_verified, student_enrolled

### Ministerio da Justica e dos Direitos Humanos (`justica`)
**Score: 100%** (30/30 checks)

| Check | Status | Descricao |
|---|---|---|
| role_role_ministerio | PASS | Role ROLE_MINISTERIO definida |
| role_role_provincia | PASS | Role ROLE_PROVINCIA definida |
| role_role_municipio | PASS | Role ROLE_MUNICIPIO definida |
| role_role_unidade | PASS | Role ROLE_UNIDADE definida |
| rbac_hierarchy_ministerio | PASS | Role ROLE_MINISTERIO mapeavel para RoleGovernance |
| rbac_hierarchy_provincia | PASS | Role ROLE_PROVINCIA mapeavel para RoleGovernance |
| rbac_hierarchy_municipio | PASS | Role ROLE_MUNICIPIO mapeavel para RoleGovernance |
| rbac_hierarchy_unidade | PASS | Role ROLE_UNIDADE mapeavel para RoleGovernance |
| territorial_model | PASS | Modelo territorial correto: nacional_provincial_unidade |
| nivel_nacional | PASS | Nivel territorial 'nacional' disponivel |
| nivel_provincial | PASS | Nivel territorial 'provincial' disponivel |
| nivel_unidade | PASS | Nivel territorial 'unidade' disponivel |
| approval_chain | PASS | Cadeia definida: unidade -> municipio -> provincia |
| approval_chain_pending | PASS | Aprovacao inicial corretamente pendente |
| delegation_engine | PASS | DelegationEngine disponivel |
| delegation_role_role_ministerio | PASS | Role ROLE_MINISTERIO pode delegar/ receber delegacao |
| delegation_role_role_provincia | PASS | Role ROLE_PROVINCIA pode delegar/ receber delegacao |
| delegation_role_role_municipio | PASS | Role ROLE_MUNICIPIO pode delegar/ receber delegacao |
| delegation_role_role_unidade | PASS | Role ROLE_UNIDADE pode delegar/ receber delegacao |
| delegation_hierarchy | PASS | Delegacao hierarquica funcional (nivel superior -> inferior) |
| audit_logger | PASS | AuditLogger operacional |
| audit_trail | PASS | Trilha de auditoria funcional |
| digital_signature | PASS | Assinatura digital funcional |
| signature_verification | PASS | Verificacao de assinatura funcional |
| exposed_events | PASS | Eventos expostos: 3 |
| consumed_events | PASS | Eventos consumidos: 3 |
| event_company_incorporated | PASS | Evento 'company_incorporated' tem consumidores |
| org_minjusdh | PASS | Organizacao 'Ministério da Justiça e dos Direitos Humanos' registada |
| org_drh-huambo | PASS | Organizacao 'Direção Regional da Justiça do Huambo' registada |
| org_conservatoria-huambo | PASS | Organizacao 'Conservatória do Registo Civil do Huambo' registada |

**Configuracao atual:**

- Dono: Ministério da Justiça e dos Direitos Humanos (MINJUSDH)
- Modelo territorial: nacional_provincial_unidade
- Cadeia de aprovacao: unidade -> municipio -> provincia
- Servicos: registo_civil, notariado, tribunal, criminal
- Expõe: civil_registration_issued, company_incorporated, notarial_act_signed
- Consome: citizen_updated, identity_verified, payment_confirmed

### Ministerio das Financas (`financas-impostos`)
**Score: 100%** (25/25 checks)

| Check | Status | Descricao |
|---|---|---|
| role_role_ministerio | PASS | Role ROLE_MINISTERIO definida |
| role_role_provincia | PASS | Role ROLE_PROVINCIA definida |
| role_role_unidade | PASS | Role ROLE_UNIDADE definida |
| rbac_hierarchy_ministerio | PASS | Role ROLE_MINISTERIO mapeavel para RoleGovernance |
| rbac_hierarchy_provincia | PASS | Role ROLE_PROVINCIA mapeavel para RoleGovernance |
| rbac_hierarchy_unidade | PASS | Role ROLE_UNIDADE mapeavel para RoleGovernance |
| territorial_model | PASS | Modelo territorial correto: nacional_provincial_unidade |
| nivel_nacional | PASS | Nivel territorial 'nacional' disponivel |
| nivel_provincial | PASS | Nivel territorial 'provincial' disponivel |
| nivel_unidade | PASS | Nivel territorial 'unidade' disponivel |
| approval_chain | PASS | Cadeia definida: unidade -> provincia |
| approval_chain_pending | PASS | Aprovacao inicial corretamente pendente |
| delegation_engine | PASS | DelegationEngine disponivel |
| delegation_role_role_ministerio | PASS | Role ROLE_MINISTERIO pode delegar/ receber delegacao |
| delegation_role_role_provincia | PASS | Role ROLE_PROVINCIA pode delegar/ receber delegacao |
| delegation_role_role_unidade | PASS | Role ROLE_UNIDADE pode delegar/ receber delegacao |
| delegation_hierarchy | PASS | Delegacao hierarquica funcional (nivel superior -> inferior) |
| audit_logger | PASS | AuditLogger operacional |
| audit_trail | PASS | Trilha de auditoria funcional |
| digital_signature | PASS | Assinatura digital funcional |
| signature_verification | PASS | Verificacao de assinatura funcional |
| exposed_events | PASS | Eventos expostos: 3 |
| consumed_events | PASS | Eventos consumidos: 4 |
| event_nif_issued | PASS | Evento 'nif_issued' tem consumidores |
| org_minfin | PASS | Organizacao 'Ministério das Finanças' registada |

**Configuracao atual:**

- Dono: Ministério das Finanças (MINFIN)
- Modelo territorial: nacional_provincial_unidade
- Cadeia de aprovacao: unidade -> provincia
- Servicos: emitir_nif, declarar_impostos, consultar_fiscal, regularizar
- Expõe: nif_issued, tax_declaration_submitted, tax_payment_received
- Consome: citizen_updated, identity_verified, company_incorporated, payment_confirmed

### Ministerio da Administracao Territorial (`administracao-local`)
**Score: 100%** (22/22 checks)

| Check | Status | Descricao |
|---|---|---|
| role_role_provincia | PASS | Role ROLE_PROVINCIA definida |
| role_role_municipio | PASS | Role ROLE_MUNICIPIO definida |
| rbac_hierarchy_provincia | PASS | Role ROLE_PROVINCIA mapeavel para RoleGovernance |
| rbac_hierarchy_municipio | PASS | Role ROLE_MUNICIPIO mapeavel para RoleGovernance |
| territorial_model | PASS | Modelo territorial correto: nacional_provincial_municipal_unidade |
| nivel_nacional | PASS | Nivel territorial 'nacional' disponivel |
| nivel_provincial | PASS | Nivel territorial 'provincial' disponivel |
| nivel_municipal | PASS | Nivel territorial 'municipal' disponivel |
| nivel_unidade | PASS | Nivel territorial 'unidade' disponivel |
| approval_chain | PASS | Cadeia definida: municipio -> provincia |
| approval_chain_pending | PASS | Aprovacao inicial corretamente pendente |
| delegation_engine | PASS | DelegationEngine disponivel |
| delegation_role_role_provincia | PASS | Role ROLE_PROVINCIA pode delegar/ receber delegacao |
| delegation_role_role_municipio | PASS | Role ROLE_MUNICIPIO pode delegar/ receber delegacao |
| delegation_hierarchy | PASS | Delegacao hierarquica funcional (nivel superior -> inferior) |
| audit_logger | PASS | AuditLogger operacional |
| audit_trail | PASS | Trilha de auditoria funcional |
| digital_signature | PASS | Assinatura digital funcional |
| signature_verification | PASS | Verificacao de assinatura funcional |
| exposed_events | PASS | Eventos expostos: 3 |
| consumed_events | PASS | Eventos consumidos: 3 |
| org_mat | PASS | Organizacao 'Ministério da Administração Territorial' registada |

**Configuracao atual:**

- Dono: Ministério da Administração Territorial (MAT)
- Modelo territorial: nacional_provincial_municipal_unidade
- Cadeia de aprovacao: municipio -> provincia
- Servicos: licenciamento, alvara, atestado_residencia, atendimento_municipal
- Expõe: license_issued, residence_confirmed, municipal_certificate_issued
- Consome: citizen_updated, identity_verified, payment_confirmed

### Ministerio da Adm. Publica e Seguranca Social (`seguranca-social`)
**Score: 100%** (30/30 checks)

| Check | Status | Descricao |
|---|---|---|
| role_role_ministerio | PASS | Role ROLE_MINISTERIO definida |
| role_role_provincia | PASS | Role ROLE_PROVINCIA definida |
| role_role_municipio | PASS | Role ROLE_MUNICIPIO definida |
| role_role_unidade | PASS | Role ROLE_UNIDADE definida |
| rbac_hierarchy_ministerio | PASS | Role ROLE_MINISTERIO mapeavel para RoleGovernance |
| rbac_hierarchy_provincia | PASS | Role ROLE_PROVINCIA mapeavel para RoleGovernance |
| rbac_hierarchy_municipio | PASS | Role ROLE_MUNICIPIO mapeavel para RoleGovernance |
| rbac_hierarchy_unidade | PASS | Role ROLE_UNIDADE mapeavel para RoleGovernance |
| territorial_model | PASS | Modelo territorial correto: nacional_provincial_municipal_unidade |
| nivel_nacional | PASS | Nivel territorial 'nacional' disponivel |
| nivel_provincial | PASS | Nivel territorial 'provincial' disponivel |
| nivel_municipal | PASS | Nivel territorial 'municipal' disponivel |
| nivel_unidade | PASS | Nivel territorial 'unidade' disponivel |
| approval_chain | PASS | Cadeia definida: unidade -> municipio -> provincia |
| approval_chain_pending | PASS | Aprovacao inicial corretamente pendente |
| delegation_engine | PASS | DelegationEngine disponivel |
| delegation_role_role_ministerio | PASS | Role ROLE_MINISTERIO pode delegar/ receber delegacao |
| delegation_role_role_provincia | PASS | Role ROLE_PROVINCIA pode delegar/ receber delegacao |
| delegation_role_role_municipio | PASS | Role ROLE_MUNICIPIO pode delegar/ receber delegacao |
| delegation_role_role_unidade | PASS | Role ROLE_UNIDADE pode delegar/ receber delegacao |
| delegation_hierarchy | PASS | Delegacao hierarquica funcional (nivel superior -> inferior) |
| audit_logger | PASS | AuditLogger operacional |
| audit_trail | PASS | Trilha de auditoria funcional |
| digital_signature | PASS | Assinatura digital funcional |
| signature_verification | PASS | Verificacao de assinatura funcional |
| exposed_events | PASS | Eventos expostos: 3 |
| consumed_events | PASS | Eventos consumidos: 4 |
| event_employer_registered | PASS | Evento 'employer_registered' tem consumidores |
| org_mapTss | PASS | Organizacao 'Ministério da Administração Pública e Segurança Social' registada |
| org_inss | PASS | Organizacao 'Instituto Nacional de Segurança Social' registada |

**Configuracao atual:**

- Dono: Ministério da Administração Pública e Segurança Social (MAPTSS)
- Modelo territorial: nacional_provincial_municipal_unidade
- Cadeia de aprovacao: unidade -> municipio -> provincia
- Servicos: registo_empregador, contribuicao, prestacao_social, pensao
- Expõe: employer_registered, social_contribution_received, benefit_granted
- Consome: citizen_updated, identity_verified, payment_confirmed, company_incorporated

## Recomendacoes
