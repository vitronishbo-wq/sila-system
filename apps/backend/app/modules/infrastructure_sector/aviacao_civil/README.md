# Modulo Aviacao Civil

Implementacao vertical inicial do dominio de aviacao civil com:
- Write model para aeronaves, voos e ocorrencias
- Event bus e outbox em memoria
- API FastAPI para operacao basica
- Adapters externos com circuit breaker
- Worker de monitoramento de voos

Este baseline foi desenhado para evoluir para persistencia SQLAlchemy, CQRS read model e streaming sem quebrar contratos.
