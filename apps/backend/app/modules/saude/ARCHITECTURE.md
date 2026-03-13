# Saude Module Architecture

Este modulo segue a arquitetura hexagonal do SILA.

- api: expõe rotas e health checks.
- application: casos de uso e orquestracao de servicos.
- domain: regras de negocio puras e invariantes.
- infrastructure: adaptadores concretos (DB, APIs externas).

O objetivo e manter contratos claros entre camadas, reduzir acoplamento e
permitir evolucao segura do dominio de saude.
