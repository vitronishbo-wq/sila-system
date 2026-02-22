# Education Module Documentation

## Objetivo

Gestão educacional integrada: histórico escolar individual + gestão macro de
instituições, matrículas, transferências, documentos, faltas, notas e estatísticas.

## Fluxos

- Matrícula
- Transferência
- Solicitação de documentos escolares
- Justificativa de faltas
- Registro de notas
- Estatísticas educacionais

## Diagrama de Integração

Education ⟷ Identity ⟷ Location ⟷ Statistics

- Instituições vinculadas a municípios/províncias
- Alunos e professores vinculados a identidades

## Endpoints REST

- POST `/education/institutions/` (admin)
- GET `/education/institutions/{municipality_id}` (admin/cidadão)
- POST `/education/enrollments/` (cidadão)
- POST `/education/transfers/` (cidadão)
- POST `/education/documents/` (cidadão)
- POST `/education/attendance/` (cidadão)
- POST `/education/grades/` (professor)
- GET `/education/grades/{student_id}` (admin/cidadão)
- GET `/education/statistics/{municipality_id}` (admin)

## Regras

- Controle de capacidade das instituições
- Matrícula, transferência e documentos auditáveis
- Professores associados a instituições
- Estatísticas para planejamento educacional

## Roadmap

- Integração com dashboard educacional
- Relatórios de evasão, aproveitamento, vagas
- Emissão digital de certificados

## Exemplo de dashboard educacional

- Nº de escolas, professores, alunos, vagas
- Taxa de matrícula, evasão, conclusão
