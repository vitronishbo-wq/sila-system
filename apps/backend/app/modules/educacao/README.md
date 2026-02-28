# Educacao

Modulo de matriculas escolares integrado ao nucleo do sistema.

## Capacidades implementadas
- Dominio de matricula, escola, turma e ano letivo
- Fluxo de matricula E2E: criar, ativar, listar por cidadao
- Validacao de duplicidade por ano letivo
- Geracao institucional de numero de processo: `ANO/CODM/SEQUENCIAL`
- Tracking no nucleo `service_requests` por `entity_id`

## Endpoints
- `POST /api/v1/educacao/matriculas/`
- `POST /api/v1/educacao/matriculas/{matricula_id}/ativar`
- `GET /api/v1/educacao/matriculas/citizen/{citizen_id}`
