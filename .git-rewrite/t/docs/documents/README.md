# Documents Module Documentation

## Objetivo

Repositório oficial de documentos legais digitais do cidadão e do Estado.

## Fluxos

- Criação de documento
- Emissão
- Consulta
- Renovação
- Revogação
- Auditoria de histórico

## Diagrama de Integração

Documents ⟷ Identity ⟷ Citizenship

- Cada documento vinculado a um cidadão.
- Certidões e registros civis vinculados à cidadania.

## Integrações

- **Identity**: vincula cidadão ao documento.
- **Citizenship**: certidões e registros civis.
- **Appointments**: agendamento de emissão/renovação.
- **Governance/Reports**: estatísticas de documentos.
- **Notifications**: lembretes de expiração.

## Endpoints REST

- POST `/documents/` (admin)
- GET `/documents/{id}` (admin/cidadão)
- GET `/documents/citizen/{citizen_id}` (admin/cidadão)
- PUT `/documents/{id}` (admin)
- POST `/documents/{id}/revoke` (admin)
- POST `/documents/{id}/renew` (admin)
- GET `/documents/{id}/history` (admin)

## Regras

- Não permitir duplicidade de número/tipo.
- Auditoria de todas as ações.
- Cidadão só consulta seus próprios documentos.
- Admin gerencia todos os documentos.

## Roadmap

- Integração com notificações automáticas.
- Auditoria detalhada de alterações.
- Relatórios estatísticos.

## Exemplo de JSON de documento

```json
{
  "id": "uuid",
  "citizen_id": "uuid",
  "type": "identity_card",
  "number": "123456789",
  "issued_by": "MININT",
  "issue_date": "2025-01-01",
  "expiry_date": "2035-01-01",
  "status": "valid",
  "file_path": "/secure/path/bi.pdf",
  "metadata": { "observacao": "Primeira via" },
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```
