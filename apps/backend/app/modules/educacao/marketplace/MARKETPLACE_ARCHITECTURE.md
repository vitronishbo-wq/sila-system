# Citizen Educational Marketplace Architecture

## Visão Geral

O Citizen Educational Marketplace é um subsistema dentro do módulo `educacao` que implementa um mercado nacional de oportunidades educacionais com foco na experiência do cidadão.

## Objetivo

Transformar o acesso à educação de um processo burocrático manual em uma experiência digital fluida onde:

- **Cidadão abre app** → procura escola → vê vagas reais → vê compatibilidade → compara instituições → confirma → **sistema executa tudo**
- **Sem**: secretaria, papel, despacho, fila, assinatura manual

## Arquitetura de 8 Subdomínios

```
marketplace/
├── discovery/        # Descoberta de vagas e programas educacionais
├── ranking/          # Ranking de instituições e programas
├── matching/         # Matching automático baseado em elegibilidade
├── recommendation/   # Recomendações personalizadas para cidadão
├── search/           # Busca avançada com filtros complexos
├── booking/          # Reserva de vagas e pré-matrícula
├── transfers/        # Transferências self-service
└── admissions/       # Admissão automática e validação de elegibilidade
```

## Padrão Arquitetural

Cada subdomínio segue **Hexagonal Architecture**:

```
subdominio/
├── domain/              # Lógica de negócio pura
│   ├── __init__.py
│   ├── entities.py      # Entidades do domínio
│   ├── value_objects.py # Value objects imutáveis
│   ├── events.py        # Domain events
│   └── exceptions.py    # Exceções específicas do domínio
├── application/         # Casos de uso e orquestração
│   ├── __init__.py
│   ├── services.py      # Serviços de aplicação
│   ├── ports.py         # Portas (interfaces) hexagonais
│   ├── dto.py           # Data Transfer Objects
│   └── commands.py      # Comandos e queries (CQRS optional)
├── api/                 # Interface HTTP (entrada)
│   ├── __init__.py
│   ├── endpoints.py     # Endpoints REST/GraphQL
│   ├── schemas.py       # Schemas Pydantic
│   ├── router.py        # Router FastAPI
│   └── health.py        # Health checks
└── infrastructure/      # Implementações concretas (saída)
    ├── __init__.py
    ├── adapters.py      # Adaptadores para sistemas externos
    ├── repositories.py  # Implementação de repositórios
    ├── orm.py           # Modelos SQLAlchemy
    └── cache.py         # Cache strategies
```

## Fluxo Citizen-Centric

### 1. Discovery
- Cidadão busca programas educacionais disponíveis
- Sistema retorna vagas reais com disponibilidade
- Informações estruturadas: nível, duração, instituição, capacidade

### 2. Ranking
- Comparação de instituições por métricas (qualidade, reputação, localização)
- Filtros por preferências do cidadão
- Score baseado em elegibilidade

### 3. Matching
- Engine de matching automático baseado em:
  - Qualificações do cidadão
  - Histórico acadêmico
  - Localização geográfica
  - Preferências pessoais
- Retorna oportunidades melhor alinhadas

### 4. Recommendation
- Recomendações personalizadas via ML/algoritmos
- Baseado em perfil do cidadão e histórico
- Sugestões proativas de transferências

### 5. Search
- Busca full-text em vagas, instituições, programas
- Filtros: localização, nível, duração, preço, modalidade
- Busca geoespacial com raio de proximidade

### 6. Booking
- Reserva de vaga com confirmação instantânea
- Pré-matrícula automática
- Emissão de comprovante digital
- Sincronização com sistema de matrícula

### 7. Transfers
- Transferência entre instituições self-service
- Validação automática de elegibilidade
- Análise de compatibilidade curricular
- Aprovação sem despacho manual

### 8. Admissions
- Validação automática de elegibilidade
- Verificação de documentos (integração)
- Aprovação instantânea ou notificação de pendências
- Geração de carta de admissão digital

## Integração com Módulo Educacao

### X-Road Interoperability
- Portas hexagonais usam X-Road para comunicação com:
  - Sistema de Matrícula (educacao/matricula)
  - Validação de Elegibilidade (educacao/eligibility)
  - Histórico Escolar (educacao/historico_escolar)
  - Instituições (educacao/escola)

### Preservação de Bounded Contexts
- Marketplace é subdomínio de educacao
- Mantém separação domain/infrastructure
- Evita circular dependencies
- Usa eventos de domínio para comunicação assíncrona

## Atores e Casos de Uso

### Cidadão
- `ListarOportunidades` → Discovery
- `BuscarProgramas` → Search
- `ObtorRecomendacoes` → Recommendation
- `CompararInstituicoes` → Ranking
- `ReservarVaga` → Booking
- `SolicitarTransferencia` → Transfers
- `VerificarStatus` → Admissions

### Instituição
- `PublicarVagas` → Discovery
- `ManutenirCapacidade` → Booking
- `VisualizeMetricas` → Ranking
- `GerenciarElegibilidade` → Admissions

### Admin/Compliance
- `AuditarMarketplace` → Compliance
- `GerenciarRegras` → Governance
- `VisualizarMetricas` → Analytics

## Conformidade e Segurança

- **Auditoria**: Todas as ações registradas em event store
- **GDPR Compliance**: Dados sensíveis criptografados
- **X-Road Security**: Certificados SSL/TLS obrigatórios
- **Rate Limiting**: Proteção contra abuse
- **Validação**: Elegibilidade validada antes de qualquer ação

## Roadmap de Implementação

1. **MVP**: Discovery + Booking + Admissions (v1.0)
2. **v1.1**: Search + Ranking
3. **v1.2**: Matching + Transfers
4. **v1.3**: Recommendation (ML)
5. **v2.0**: Analytics + Compliance Dashboard

## Métricas de Sucesso

- Tempo de matrícula reduzido de 10 dias para < 1 hora
- Taxa de adoção do marketplace: > 80%
- Satisfação do cidadão: > 4.5/5
- Taxa de erro em admissão: < 0.1%

## Referências

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [X-Road Interoperability](https://x-road.global/)

---

**Status**: FASE 3.2 - Under Development  
**Último Update**: 2026-05-26
