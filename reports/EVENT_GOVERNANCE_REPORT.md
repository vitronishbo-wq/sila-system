# EVENT GOVERNANCE REPORT

> Gerado em: 2026-06-08
> Proposito: Analisar cobertura de eventos, acoplamento e eventos orfaos

---

## Resumo

| Metrica | Valor |
|---|---|
| Total eventos unicos | 40 |
| Eventos com publisher + subscriber | 12 |
| Eventos ONLY publisher (orphan producer) | 28 |
| Eventos ONLY subscriber (orphan consumer) | 0 |
| Meta | 0 orfaos |

## Matriz de Eventos

| Evento | Publishers | Subscribers | Criticidade |
|---|---|---|---|
| appointment_scheduled | saude | - | ORPHAN_PRODUCER |
| benefit_granted | seguranca-social | - | ORPHAN_PRODUCER |
| bi_issued | identity | educacao | NORMAL |
| biometric_enrolled | identity | - | ORPHAN_PRODUCER |
| birth_registered | registo-civil | identity | NORMAL |
| business_support_granted | apoio-empresarial | - | ORPHAN_PRODUCER |
| certificate_issued | educacao | - | ORPHAN_PRODUCER |
| citizen_updated | identity | educacao, saude, justica, payment, registo-civil, financas-impostos, administracao-local, seguranca-social, apoio-empresarial, comercio, emprego, trabalho-inspecao | HIGH_COUPLING |
| civil_registration_issued | justica | - | ORPHAN_PRODUCER |
| commercial_license_issued | apoio-empresarial | - | ORPHAN_PRODUCER |
| company_incorporated | justica | financas-impostos, seguranca-social | NORMAL |
| company_registered | apoio-empresarial | comercio | NORMAL |
| death_registered | registo-civil | identity | NORMAL |
| employer_registered | seguranca-social | emprego, trabalho-inspecao | NORMAL |
| employment_contract_registered | emprego | trabalho-inspecao | NORMAL |
| fine_issued | trabalho-inspecao | - | ORPHAN_PRODUCER |
| identity_verified | identity | educacao, saude, justica, payment, registo-civil, financas-impostos, administracao-local, seguranca-social, apoio-empresarial, comercio, emprego, trabalho-inspecao | HIGH_COUPLING |
| inspection_completed | comercio, trabalho-inspecao | - | ORPHAN_PRODUCER |
| inspection_scheduled | trabalho-inspecao | - | ORPHAN_PRODUCER |
| invoice_status_changed | payment | - | ORPHAN_PRODUCER |
| job_vacancy_created | emprego | - | ORPHAN_PRODUCER |
| license_issued | administracao-local | - | ORPHAN_PRODUCER |
| license_permit_issued | comercio | - | ORPHAN_PRODUCER |
| marriage_registered | registo-civil | - | ORPHAN_PRODUCER |
| municipal_certificate_issued | administracao-local | - | ORPHAN_PRODUCER |
| nif_issued | financas-impostos | payment, apoio-empresarial | NORMAL |
| notarial_act_signed | justica | - | ORPHAN_PRODUCER |
| payment_confirmed | payment | justica, identity, financas-impostos, administracao-local, seguranca-social, apoio-empresarial, comercio | HIGH_COUPLING |
| payment_failed | payment | - | ORPHAN_PRODUCER |
| payment_reconciled | payment | - | ORPHAN_PRODUCER |
| placement_completed | emprego | - | ORPHAN_PRODUCER |
| prescription_issued | saude | - | ORPHAN_PRODUCER |
| referral_made | saude | - | ORPHAN_PRODUCER |
| residence_confirmed | administracao-local | - | ORPHAN_PRODUCER |
| social_contribution_received | seguranca-social | - | ORPHAN_PRODUCER |
| student_enrolled | educacao | saude, payment | NORMAL |
| student_transferred | educacao | - | ORPHAN_PRODUCER |
| tax_declaration_submitted | financas-impostos | - | ORPHAN_PRODUCER |
| tax_payment_received | financas-impostos | - | ORPHAN_PRODUCER |
| trade_registered | comercio | - | ORPHAN_PRODUCER |

## Modulos sem Eventos no Registry

Dos 81 modulos no backend, apenas 13 tem eventos catalogados no Registry.
Os restantes 68 modulos nao declaram eventos:

- agricultura (MINAGRIF) | - aguas-saneamento (MINAMB) | - ambiente (MINAMB) | - api (UNKNOWN) | - arquivo-nacional (MINCULT)
- assistencia-social (MAPTSS) | - audit (TRANSVERSAL) | - aviacao-civil (MINTRANS) | - ciencia-pesquisa (MINCT) | - civil_protection (MININT)
- comercio-externo (MINECON) | - compliance (TRANSVERSAL) | - cooperacao-internacional (MINEC) | - cultura (MINCULT) | - defesa-consumidor (MINECON)
- desporto (MINJUV) | - documents (TRANSVERSAL) | - economy (MINECON) | - energia (MINENERG) | - energy (MINENERG)
- estatistica (MINPLAN) | - familia (MAPTSS) | - florestas (MINAGRIF) | - gestao-fundiaria (MINAMB) | - governance (TRANSVERSAL)
- habitacao (MINOBRAS) | - igualdade (MAPTSS) | - industria (MINECON) | - industry (MINECON) | - infrastructure (MINOBRAS)
- infrastructure_sector (MINOBRAS) | - integracao-nacional (MULTI) | - intelligence (TRANSVERSAL) | - justice (MINJUSDH) | - juventude (MINJUV)
- logistics (MINTRANS) | - marketplace (MINED) | - meteorologia (MINAMB) | - migracao (MININT) | - migration_service (MININT)
- notifications (TRANSVERSAL) | - obras-publicas (MINOBRAS) | - operations (TRANSVERSAL) | - patrimonio-cultural (MINCULT) | - pecuaria (MINAGRIF)
- pescas (MINPESC) | - pescas-industriais (MINPESC) | - petroleo-gas (MINPET) | - planeamento (MINPLAN) | - portos-logistica (MINTRANS)
- procurement (TRANSVERSAL) | - protecao-civil (MININT) | - protecao-dados (TRANSVERSAL) | - public_security (MININT) | - recursos-minerais (MINPET)
- resources (MULTI) | - seguranca-alimentar (MINAGRIF) | - seguranca-publica (MININT) | - society (MAPTSS) | - tecnologia-inovacao (MINCT)
- telecomunicacoes (MINTEL) | - tests (TRANSVERSAL) | - tourism (MITUR) | - transportes (MINTRANS) | - turismo (MITUR)
- urbanismo (MINOBRAS) | - wallet (MINFIN) | - xroad (TRANSVERSAL) | 

## Plano de Remediacao

| Prioridade | Acao | Responsavel |
|---|---|---|
| ALTA | Registrar eventos nos 15 modulos ja registados que faltam eventos | Time Governance |
| ALTA | Corrigir eventos orfaos (publisher sem subscriber, subscriber sem publisher) | Time Integracao |
| MEDIA | Adicionar eventos a todos os modulos com router + models | Time de cada ministerio |
| BAIXA | Automatizar detecao de eventos via analise de codigo | Time Platform |
