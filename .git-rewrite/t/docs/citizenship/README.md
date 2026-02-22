# Citizenship Module Documentation

## Objetivo

Gerenciar o status legal do cidadão perante o Estado, incluindo nacionalidade, estado
civil, naturalização e revogação de cidadania.

## Fluxos

- Aquisição de cidadania
- Atualização de estado civil ou status
- Revogação de cidadania

## Diagrama de Relacionamento

CitizenIdentity (identity) ⟷ CitizenshipRecord (citizenship)

- Cada identidade tem um registro único de cidadania.
- FK: `identity_id` vincula à tabela de identidades.

## Integrações

- **Identity**: dados vinculados via FK, sem duplicação de nome, BI, nascimento.
- **Documents**: pode exigir BI/passaporte válido para criar cidadania.
- **Justice/Governance**: processos de naturalização ou perda podem ser integrados.

## Notas

- CRUD seguro e auditável.
- Proteções por role/scope.
- Testes automatizados garantem consistência.

## Endpoints REST

- POST `/citizenship/` (admin)
- GET `/citizenship/{identity_id}` (citizenship:read)
- PUT `/citizenship/{identity_id}` (admin)
- DELETE `/citizenship/{identity_id}` (admin)

## Regras

- Não permitir múltiplos registros ativos para mesma identidade.
- Alterações críticas apenas por administradores.

## Roadmap

- Integração com módulos de justiça/governança.
- Validação de documentos obrigatórios.
- Auditoria de alterações.
