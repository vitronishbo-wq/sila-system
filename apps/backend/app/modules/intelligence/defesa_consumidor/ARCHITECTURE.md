# Arquitetura do Modulo: DEFESA_CONSUMIDOR

## Contexto
Este modulo pertence ao SILA System e segue o padrao universal de Bounded Context.

## Fronteira (Contracts)
- **API Entrypoint:** `api/router.py`
- **Domain Exceptions:** `domain/exceptions.py`
- **Persistence Layer:** `infrastructure/repository.py`
