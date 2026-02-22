# Arquitetura do Sistema SILA

## Visão Geral

O sistema está em processo de migração de uma arquitetura legada (Django) para uma nova
arquitetura baseada em FastAPI + Prisma. Este documento descreve o estado atual e o
plano de migração.

## 🛠️ ORM: Prisma Client Python

O projeto foi migrado do SQLAlchemy para
[Prisma Client Python](https://prisma-client-py.readthedocs.io/), com os seguintes
benefícios:

- Schema único em `prisma/schema.prisma`
- Cliente gerado automaticamente
- Tipagem forte com Pydantic
- Assíncrono por padrão

### Fluxo de Migração

Para migrar modelos do SQLAlchemy para Prisma:

```powershell
scripts/migrate-sqla-to-prisma.ps1
```

Isso executa:

- Backup dos modelos antigos
- Análise e conversão automática
- Geração do schema Prisma
- Geração do cliente
- Auditoria final

### Reversão

Se necessário:

```powershell
scripts/rollback-prisma-migration.ps1
```

### Relatórios de Migração

Para gerar um relatório detalhado do mapeamento entre SQLAlchemy e Prisma:

```powershell
python scripts/generate-migration-report.py
```

## Estado Atual

### Backend Principal (Novo)

- **Framework**: FastAPI (Python)
- **ORM**: Prisma
- **Banco de Dados**: PostgreSQL
- **Localização**: `/backend/app`

### Backend Legado (Em Desativação)

- **Framework**: Django
- **ORM**: Django ORM
- **Banco de Dados**: SQLite (db.sqlite3)
- **Localização**: `/django-backend`

## Módulos

| Módulo      | Status             | Responsável | Notas                          |
| ----------- | ------------------ | ----------- | ------------------------------ |
| citizenship | Em produção        | -           | Primeiro módulo implementado   |
| health      | Em desenvolvimento | -           | Em consolidação (health/saude) |
| commercial  | Planejado          | -           | Próximo módulo                 |
| users       | Em migração        | -           | Em transição do Django         |

## Banco de Dados

### Estrutura Atual

- **Schema Principal**: Gerenciado pelo Prisma (`/prisma/schema.prisma`)
- **Migrações**: Geridas através do Prisma Migrate
- **Convenções**:
  - Nomes de tabelas em snake_case
  - Timestamps em UTC
  - Soft delete onde aplicável

## Plano de Migração

### Fase 1: Consolidação (2 semanas)

1. [ ] Consolidar módulos duplicados (health/saude)
2. [ ] Documentar todas as rotas e endpoints do Django
3. [ ] Criar plano de migração para cada funcionalidade

### Fase 2: Migração (4 semanas)

1. [ ] Migrar autenticação/autorização
2. [ ] Migrar módulo de usuários
3. [ ] Migrar dados críticos

### Fase 3: Desativação (1 semana)

1. [ ] Desativar rotas do Django
2. [ ] Remover dependências não utilizadas
3. [ ] Remover código legado

## Convenções de Código

### Nomenclatura

- **Código**: Inglês
- **Comentários**: Português (Brasil)
- **Variáveis**: snake_case
- **Classes**: PascalCase

### Estrutura de Diretórios

```
backend/
├── app/
│   ├── modules/
│   │   ├── citizenship/
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── services/
│   │   │   └── api.py
│   │   └── health/
│   ├── core/
│   └── main.py
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

## Próximos Passos

1. [ ] Finalizar consolidação do módulo health
2. [ ] Completar migração do módulo de usuários
3. [ ] Implementar testes de integração
4. [ ] Documentar APIs com OpenAPI/Swagger

## Contato

- **Responsável Técnico**: [Marcelo Truman]
- **E-mail**: [truman10@vitronis.com]
- **Data da Última Atualização**: 2025-08-03

> [2025-08-11] Scripts obsoletos movidos para archived/:

- scripts/fix_and_migrate.ps1
- scripts/fix_and_migrate.sh
- scripts/migrate_sqlite_to_postgres.py
- scripts/clean_project.py
