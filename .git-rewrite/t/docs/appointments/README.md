# Appointments Module Documentation

## Objetivo

Gerenciar agendamentos de serviços públicos para cidadãos.

## Fluxos

- Cidadão cria agendamento
- Recebe confirmação
- Comparece ao atendimento
- Status atualizado (confirmed, completed, cancelled)

## Diagrama de Integração

CitizenIdentity (identity) ⟷ Appointments ⟷ ServiceHub

- Cada agendamento vinculado a um cidadão e a um serviço.

## Integrações

- **Identity**: vincula cidadão ao agendamento.
- **Service Hub**: vincula serviço público ao agendamento.
- **Notification**: pode enviar lembretes por e-mail/SMS.
- **Reports/Statistics**: coleta dados de tempo de espera, taxa de cancelamento.

## Endpoints REST

- POST `/appointments/` (cidadão)
- GET `/appointments/me` (cidadão)
- GET `/appointments/{id}` (admin ou dono)
- PUT `/appointments/{id}` (cidadão/admin)
- DELETE `/appointments/{id}` (cidadão)

## Regras

- Não permitir sobreposição de horários para mesmo cidadão/serviço.
- Validar serviço ativo antes de agendar.
- Cidadão só gerencia seus próprios agendamentos.
- Admin pode gerenciar todos e alterar status.

## Roadmap

- Integração com notificações automáticas.
- Relatórios de estatísticas de agendamento.
- Auditoria de alterações.
