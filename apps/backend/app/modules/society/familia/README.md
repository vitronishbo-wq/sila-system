# Modulo Familia

Bounded context para gestao de agregados familiares, membros, vinculos e dependencias.

## Arquitetura
- DDD com aggregate root `FamilyAggregate`
- CQRS com read model `family_composition_view`
- Outbox `family_domain_events`
