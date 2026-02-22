# SILA-System: Módulo ServiceHub

Este documento descreve os modelos, endpoints, regras de negócio e integrações do
ServiceHub do SILA-System.

## Modelos

- **Service**: Serviço público digital cadastrado.
- **ServiceLocation**: Local de atendimento do serviço.

## Endpoints REST

- `POST /services/`: Criar serviço
- `GET /services/`: Listar serviços
- `GET /services/{service_id}`: Detalhar serviço
- `PUT /services/{service_id}`: Atualizar serviço
- `PATCH /services/{service_id}/deactivate`: Desativar serviço
- `PATCH /services/{service_id}/activate`: Ativar serviço
- `POST /services/{service_id}/locations`: Adicionar local de atendimento
- `GET /services/locations/`: Listar locais de atendimento
- `GET /services/locations/{location_id}`: Detalhar local de atendimento
- `PUT /services/locations/{location_id}`: Atualizar local de atendimento
- `DELETE /services/locations/{location_id}`: Remover local de atendimento
- `GET /services/categories/{category}/services`: Listar serviços por categoria
- `GET /services/scopes/{scope}/services`: Listar serviços por escopo
- `GET /services/statistics/overview`: Estatísticas gerais

## Regras de Negócio

- Serviços são únicos por nome e categoria.
- Locais de atendimento são únicos por serviço, província e município.
- Serviços podem ser ativados/desativados.
- Estatísticas agregam dados por categoria, escopo e status.

## Integrações

- Integração com todos módulos de serviço (cidadania, saúde, educação, etc).
- Orquestração de serviços pagos via Payment.
- Descoberta e registro de serviços para frontend e APIs externas.

## Testes

- Testes automatizados em `tests/test_service_hub.py` cobrem:
  - Cadastro e listagem de serviços
  - Cadastro e listagem de locais de atendimento

## Segurança

- Acesso restrito por escopo/role
- Auditoria de operações de cadastro e atualização
- Rate limiting e autenticação JWT

## Observações

- Pronto para integração com novos serviços e APIs externas.
- Endpoints seguem padrões REST e retornam erros claros.
