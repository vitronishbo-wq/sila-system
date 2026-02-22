# SILA-System: Módulo de Notificação

Este documento descreve os modelos, endpoints, regras de negócio e integrações do módulo
de notificação do SILA-System.

## Modelos

- **Notification**: Notificação enviada ao cidadão (email, sms, push).
- **NotificationLog**: Registro de eventos da notificação.

## Endpoints REST

- `POST /notification/send`: Enviar notificação
- `GET /notification/citizen/{citizen_id}`: Listar notificações de cidadão
- `GET /notification/logs/{notification_id}`: Consultar logs de notificação

## Regras de Negócio

- Notificações podem ser enviadas por email, sms ou push.
- Logs registram eventos: criação, envio, entrega, falha.
- Apenas cidadãos válidos podem receber notificações.

## Integrações

- **Identity**: Validação de cidadão.
- **Finance**: Notificações de faturas, impostos, pagamentos.
- **Mock Notification Provider**: Simulação de envio real.

## Testes

- Testes automatizados em `tests/test_notification.py` cobrem:
  - Envio e listagem de notificações
  - Consulta de logs de notificação

## Segurança

- Acesso restrito por escopo/role
- Auditoria de eventos de notificação
- Rate limiting e autenticação JWT

## Observações

- Integração pronta para provedores reais de notificação.
- Endpoints seguem padrões REST e retornam erros claros.
