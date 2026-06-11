# DEMO_DATABASE_BASELINE

Data: 2026-06-10
Objetivo: estabilizacao da demonstracao ministerial de sexta-feira, 2026-06-12.

## Decisao Operacional

Banco oficial da demo:

```text
127.0.0.1:5432/sila_db
```

Nao usar como referencia para a demo:

```text
container sila-db
```

Motivo: o container `sila-db` esta vazio, sem `alembic_version` e sem tabelas em `public`.

## Baseline Confirmada

Consulta executada contra `127.0.0.1:5432/sila_db`:

```sql
SELECT COUNT(*) FROM educacao_escolas;
SELECT COUNT(*) FROM educacao_turmas;
SELECT COUNT(*) FROM educacao_academic_identities;
SELECT COUNT(*) FROM educacao_matriculas;
SELECT COUNT(*) FROM educacao_boletins;
SELECT COUNT(*) FROM educacao_certificados;
SELECT COUNT(*) FROM users;
```

Resultado atual:

| Entidade | Tabela | Quantidade | Status |
| --- | --- | ---: | --- |
| Escolas | `educacao_escolas` | 4 | OK |
| Turmas | `educacao_turmas` | 7 | OK |
| Alunos | `educacao_academic_identities` | 1 | OK |
| Matriculas | `educacao_matriculas` | 1 | OK |
| Boletins | `educacao_boletins` | 1 | OK |
| Certificados | `educacao_certificados` | 1 | OK |
| Utilizadores | `users` | 5 | OK |

## Registo Demo

Registo minimo criado de forma idempotente para garantir o caminho critico:

```text
citizen_id / academic_identity_id: 11111111-1111-4111-8111-111111111111
national_student_number: SILA-DEMO-0001
nome: Estudante Demo Ministerio
matricula: MAT-DEMO-0001
boletim: BOL-DEMO-0001
certificado: CERT-DEMO-0001
escola: Complexo Escolar 4 de Fevereiro
turma: 7A
```

Endpoint FUC a usar no ensaio:

```text
GET /fuc/11111111-1111-4111-8111-111111111111/educacao
```

## Alembic

Estado validado:

```text
20260607_0003_create_provider_homologation_evidence (head)
```

Resultado esperado cumprido:

```text
1 unico head valido
```

Ficheiros retirados do caminho ativo do Alembic e preservados para revisao pos-demo:

```text
apps/backend/alembic/quarantine_demo_20260610/20260610_0001_educacao_alignment_draft.py.disabled
apps/backend/alembic/quarantine_demo_20260610/2026_06_10_1700-6b6357e44962_educacao_core_alignment.py.disabled
```

Razao:

```text
Nao aplicar autogenerate.
Nao aplicar migration com DROP TABLE antes da demo.
Institution capacities nao bloqueia a apresentacao MAT.
```

## Decisao de Prioridade

Tudo que nao impacta diretamente:

```text
Login
Dashboard Educacao
Escola
Turma
Aluno
Matricula
Boletim
Certificado
FUC
403 territorial
```

fica:

```text
POSTERGADO
```
