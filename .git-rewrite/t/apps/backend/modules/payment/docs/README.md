# SILA-System: Módulo de Pagamento

Este documento descreve os modelos, endpoints, regras de negócio e integrações do módulo
de pagamento do SILA-System.

## Modelos

- **Payment**: Pagamento de faturas ou impostos.
- **Refund**: Solicitação e processamento de reembolso.

## Endpoints REST

- `POST /payment/process`: Processar pagamento
- `GET /payment/citizen/{citizen_id}`: Listar pagamentos de cidadão
- `POST /payment/refund`: Solicitar reembolso
- `GET /payment/refunds/citizen/{citizen_id}`: Listar reembolsos de cidadão

## Regras de Negócio

- Pagamentos podem ser vinculados a faturas ou impostos.
- Reembolsos só podem ser solicitados para pagamentos concluídos.
- Status: pending, completed, failed, refunded.

## Integrações

- **Finance**: Pagamentos de faturas e impostos.
- **ServiceHub**: Orquestração de serviços pagos.
- **Mock Payment Provider**: Simulação de processamento real.

## Testes

- Testes automatizados em `tests/test_payment.py` cobrem:
  - Processamento e listagem de pagamentos
  - Solicitação e listagem de reembolsos

## Segurança

- Acesso restrito por escopo/role
- Auditoria de operações de pagamento
- Rate limiting e autenticação JWT

## Observações

- Integração pronta para provedores reais de pagamento.
- Endpoints seguem padrões REST e retornam erros claros.
