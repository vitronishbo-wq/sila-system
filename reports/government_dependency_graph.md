# Government Dependency Graph

_Gerado automaticamente do Registry Catalog_

_13 módulos registados, 38 eventos expostos, 41 eventos consumidos_

## Mapa de Dependências entre Módulos

```text
 apoio-empresarial
  ├── comercio

 educacao
  ├── payment
  ├── saude

 financas-impostos
  ├── apoio-empresarial
  ├── integracao-nacional-nif
  ├── payment

 identity
  ├── administracao-local
  ├── apoio-empresarial
  ├── comercio
  ├── educacao
  ├── financas-impostos
  ├── integracao-nacional-bi
  ├── integracao-nacional-nif
  ├── justica
  ├── payment
  ├── registo-civil
  ├── saude
  ├── seguranca-social

 justica
  ├── financas-impostos
  ├── seguranca-social

 payment
  ├── administracao-local
  ├── apoio-empresarial
  ├── comercio
  ├── financas-impostos
  ├── identity
  ├── justica
  ├── seguranca-social

 registo-civil
  ├── identity

```

## Matriz Processos × Módulos

| Processo | administracao-local | apoio-empresarial | comercio | educacao | financas-impostos | identity | integracao-nacional-bi | integracao-nacional-nif | justica | payment | registo-civil | saude | seguranca-social |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aposentação / Pensão |   |   |   |   | ✅ | ✅ |   |   |   | ✅ |   |   | ✅ |
| Constituição de Empresa | ✅ | ✅ |   |   | ✅ |   |   |   | ✅ | ✅ |   |   | ✅ |
| Contratação Laboral |   |   |   |   | ✅ | ✅ |   |   |   |   |   |   | ✅ |
| Emissão de Bilhete de Identidade |   |   |   |   |   | ✅ |   |   |   | ✅ | ✅ |   |   |
| Emissão de NIF |   |   |   |   | ✅ | ✅ |   |   |   | ✅ |   |   |   |
| Licenciamento Comercial | ✅ | ✅ | ✅ |   | ✅ |   |   |   |   | ✅ |   |   |   |
| Matrícula Escolar | ✅ |   |   | ✅ |   | ✅ |   |   |   |   |   |   |   |
| Nascimento de Cidadão | ✅ |   |   | ✅ |   | ✅ |   |   |   |   | ✅ | ✅ |   |
| Pagamento de Impostos |   |   |   |   | ✅ | ✅ |   |   |   | ✅ |   |   |   |
| Transferência Escolar | ✅ |   |   | ✅ |   |   |   |   |   |   |   |   |   |

## Eventos por Módulo

### educacao (MINED)

- Expõe: student_enrolled, student_transferred, certificate_issued
- Consome: citizen_updated, identity_verified, bi_issued

### saude (MINSA)

- Expõe: appointment_scheduled, prescription_issued, referral_made
- Consome: citizen_updated, identity_verified, student_enrolled

### justica (MINJUSDH)

- Expõe: civil_registration_issued, company_incorporated, notarial_act_signed
- Consome: citizen_updated, identity_verified, payment_confirmed

### identity (MININT)

- Expõe: citizen_updated, identity_verified, bi_issued, biometric_enrolled
- Consome: birth_registered, payment_confirmed, death_registered

### payment (MINFIN)

- Expõe: payment_confirmed, payment_failed, invoice_status_changed, payment_reconciled
- Consome: citizen_updated, identity_verified, student_enrolled, nif_issued

### registo-civil (MINJUSDH)

- Expõe: birth_registered, marriage_registered, death_registered
- Consome: citizen_updated, identity_verified

### financas-impostos (MINFIN)

- Expõe: nif_issued, tax_declaration_submitted, tax_payment_received
- Consome: citizen_updated, identity_verified, company_incorporated, payment_confirmed

### administracao-local (MAT)

- Expõe: license_issued, residence_confirmed, municipal_certificate_issued
- Consome: citizen_updated, identity_verified, payment_confirmed

### seguranca-social (MAPTSS)

- Expõe: employer_registered, social_contribution_received, benefit_granted
- Consome: citizen_updated, identity_verified, payment_confirmed, company_incorporated

### integracao-nacional-bi (MININT)

- Expõe: bi_verified, bi_consulted
- Consome: citizen_updated, identity_verified

### integracao-nacional-nif (MINFIN)

- Expõe: nif_verified
- Consome: citizen_updated, nif_issued

### apoio-empresarial (MINECON)

- Expõe: company_registered, commercial_license_issued, business_support_granted
- Consome: citizen_updated, identity_verified, payment_confirmed, nif_issued

### comercio (MINECON)

- Expõe: trade_registered, license_permit_issued, inspection_completed
- Consome: citizen_updated, identity_verified, company_registered, payment_confirmed

## Módulos Órfãos

Nenhum módulo órfão — todos consomem ou são consumidos.