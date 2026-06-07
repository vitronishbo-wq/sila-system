# FASE 3.2 — Citizen Educational Marketplace

**Status**: 📋 PLANEJAMENTO (Implementação: Depois)  
**Data**: 26 de Maio de 2026  
**Pré-requisito**: Core transacional sólido (PASSO 6-14 ✅)

---

## 🎯 Visão Geral

Criar um marketplace educacional que permite:
1. **Procura de vagas** — Filtro por critérios
2. **Matching** — Recomendação inteligente
3. **Ranking** — Ordenação por score/fit
4. **Transferência em 1 clique** — Solicitação express
5. **Matrícula automática** — Webhook confirmation

### Objetivo
Transformar transferências de estudantes de processo manual em **self-service automático**.

---

## 📊 Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│         Citizen Educational Marketplace                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. VACANCY DISCOVERY                                  │
│     ├─ Filter by criteria (class, institution, etc)   │
│     ├─ Search API (Elasticsearch optional)            │
│     └─ Availability check (real-time)                 │
│                                                         │
│  2. INTELLIGENT MATCHING                              │
│     ├─ Student profile analysis                        │
│     ├─ Academic fit scoring                            │
│     ├─ Proximity scoring                               │
│     └─ Career track alignment                          │
│                                                         │
│  3. RANKING ENGINE                                     │
│     ├─ Combined score (fit + proximity + track)       │
│     ├─ Sort by score descending                        │
│     └─ Personalized recommendations                    │
│                                                         │
│  4. ONE-CLICK TRANSFER                                │
│     ├─ Pre-filled form with top match                 │
│     ├─ Auto-evaluation                                 │
│     └─ Async processing (PASSO 13)                    │
│                                                         │
│  5. AUTO-ENROLLMENT                                    │
│     ├─ Webhook listener for approval                   │
│     ├─ Automatic matriculation                         │
│     └─ Confirmation email                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🏗️ Componentes Principais

### 1. Vacancy Discovery Service
```python
# Location: apps/backend/app/modules/educacao/application/
class VacancyDiscoveryService:
    """
    Busca e lista vagas disponíveis
    
    Métodos:
    - search_vacancies(filters: VacancyFilters) → List[VacancyDto]
    - get_vacancy(vacancy_id: UUID) → VacancyDetail
    - get_availability(institution_id, class_id) → int (count)
    """
```

**Filters Suportados:**
```python
@dataclass
class VacancyFilters:
    student_id: UUID  # Para análise de perfil
    institution_ids: List[UUID] | None = None
    class_level: List[str] | None = None  # 7º, 8º, 9º, 10º, etc
    distance_km: int | None = None  # Raio geográfico
    academic_track: str | None = None  # Geral, Científico, etc
    sort_by: str = "score"  # score, distance, availability
```

---

### 2. Intelligent Matching Engine
```python
# Location: apps/backend/app/modules/educacao/application/
class MatchingEngine:
    """
    Avalia fit entre aluno e vagas
    
    Score Components:
    - academic_fit: 0-100 (histórico + avaliação)
    - proximity_score: 0-100 (distância geográfica)
    - track_alignment: 0-100 (alinhamento de carreira)
    - combined_score: average(academic_fit, proximity, track)
    
    Métodos:
    - score_vacancy(student_id, vacancy_id) → MatchScore
    - rank_vacancies(student_id, vacancies) → List[RankedVacancy]
    """

@dataclass
class MatchScore:
    vacancy_id: UUID
    academic_fit: float  # 0-100
    proximity_score: float  # 0-100
    track_alignment: float  # 0-100
    combined_score: float  # 0-100 (weighted average)
    reasoning: str  # "Excelente fit académico, proximal, alinhado"
```

**Algoritmo de Score:**
```
academic_fit (40%) = f(student_gpa, institution_ranking, class_difficulty)
proximity_score (30%) = f(distance_km, transport_options)
track_alignment (30%) = f(career_goals, institution_specialization)

combined = (0.4 * academic) + (0.3 * proximity) + (0.3 * track)
```

---

### 3. Ranking & Recommendation
```python
# Location: apps/backend/app/modules/educacao/application/
class RecommendationService:
    """
    Ordena e recomenda vagas
    
    Métodos:
    - get_top_recommendations(student_id, limit=5) → List[RecommendedVacancy]
    - explain_recommendation(student_id, vacancy_id) → ExplanationDto
    """

@dataclass
class RecommendedVacancy:
    vacancy_id: UUID
    institution_name: str
    class_level: str
    distance_km: float
    score: float
    is_auto_approved: bool  # Se elegível automaticamente
    action_url: str  # Pre-filled transfer form
```

---

### 4. One-Click Transfer
```python
# Location: apps/backend/app/modules/educacao/api/endpoints/
@router.post("/vacancies/{vacancy_id}/transfer")
async def request_transfer_one_click(
    vacancy_id: UUID,
    service: VacancyDiscoveryService = Depends(),
    user: Dict = Depends(get_current_user),
):
    """
    Solicita transferência para vaga recomendada
    
    Response 202:
    {
        "status": "scheduled",
        "transfer_id": "TRF-2026-001234",
        "vacancy": {...},
        "evaluation": {...},
        "estimated_time": "5-10 minutes"
    }
    """
```

---

### 5. Auto-Enrollment Webhook
```python
# Location: apps/backend/app/modules/educacao/api/endpoints/
@router.post("/webhooks/transfer-approval")
async def on_transfer_approved(
    payload: TransferApprovalPayload,
    service: MatriculaService = Depends(),
):
    """
    Webhook listener para aprovação de transferência
    
    Payload:
    {
        "transfer_id": "TRF-2026-001234",
        "status": "approved",
        "timestamp": "2026-05-26T20:30:00Z"
    }
    
    Ações:
    1. Atualizar status da transferência
    2. Criar matrícula automaticamente
    3. Enviar confirmação por email
    4. Log de auditoria
    """
```

---

## 📦 Estrutura de Pastas

```
apps/backend/app/modules/educacao/
├── application/
│   ├── vacancy_discovery_service.py      (NEW)
│   ├── matching_engine.py                 (NEW)
│   ├── recommendation_service.py          (NEW)
│   └── vacancy_ports/                     (NEW)
│       ├── vacancy_repository_port.py
│       └── matching_engine_port.py
│
├── api/
│   ├── endpoints/
│   │   ├── marketplace.py                 (NEW)
│   │   └── webhooks.py                    (NEW)
│   └── schemas/
│       ├── vacancy_dto.py                 (NEW)
│       ├── matching_score_dto.py          (NEW)
│       └── recommendation_dto.py          (NEW)
│
├── domain/
│   ├── vacancy.py                         (NEW)
│   ├── matching_result.py                 (NEW)
│   └── recommendation.py                  (NEW)
│
└── infrastructure/
    ├── models/
    │   ├── vacancy_model.py               (NEW)
    │   └── matching_cache_model.py        (NEW)
    │
    └── repositories/
        ├── vacancy_repository.py          (NEW)
        └── matching_cache_repository.py   (NEW)
```

---

## 🔌 Integrações

### Com Componentes Existentes

1. **PASSO 6 (Lock Concorrente)**
   - Usar para reservar vaga durante transferência
   
2. **PASSO 13 (Automação)**
   - Usar `AutomationEngine.request_transfer()` para solicitar
   
3. **PASSO 14 (DLQ)**
   - Capturar erros de matrícula e alertar

4. **VacancyMarketplace (Existente)**
   - Reutilizar `get_available_for(school, class)`

### Novos Serviços

1. **Elasticsearch (Opcional)**
   - Índice: `sila_vacancies`
   - Busca rápida por critérios

2. **Redis Cache**
   - Scores de matching (TTL 1h)
   - Recomendações personalizadas (TTL 30min)

3. **Webhook Service**
   - Listener para aprovação de transferências
   - Retry com exponential backoff

---

## 📋 Checklist de Implementação

### Fase A: Core Discovery
- [ ] VacancyDiscoveryService
- [ ] Endpoints de busca
- [ ] Filtros funcionais
- [ ] Testes unitários

### Fase B: Intelligent Matching
- [ ] MatchingEngine
- [ ] Algoritmo de scoring
- [ ] Cache de scores
- [ ] Testes de acurácia

### Fase C: Ranking
- [ ] RecommendationService
- [ ] Ordenação por score
- [ ] Explicabilidade (reasoning)
- [ ] Personalização

### Fase D: One-Click Transfer
- [ ] Endpoint `/vacancies/{id}/transfer`
- [ ] Pre-filled form
- [ ] Integração com PASSO 13
- [ ] Status tracking

### Fase E: Auto-Enrollment
- [ ] Webhook listener
- [ ] Matrícula automática
- [ ] Confirmação por email
- [ ] Error handling + DLQ

---

## 📊 Métricas de Sucesso

| Métrica | Target |
|---------|--------|
| Tempo de busca | < 200ms |
| Acurácia de matching | > 85% |
| Taxa de conversão (clique → transferência) | > 40% |
| Taxa de aprovação automática | > 70% |
| Tempo de matrícula automática | < 5 min |

---

## 🔐 Considerações de Segurança

✅ **Autenticação:** Bearer Token (estudante)  
✅ **Autorização:** Só pode ver/transferir para própria instituição ou vizinhas  
✅ **Auditoria:** Todas as ações logged  
✅ **Rate Limiting:** 10 transferências/dia por estudante  
✅ **Dados Sensíveis:** Não expor informações de outros estudantes  

---

## 🚀 Timeline Estimada

- **Fase A**: 1-2 semanas
- **Fase B**: 2-3 semanas
- **Fase C**: 1 semana
- **Fase D**: 1 semana
- **Fase E**: 1-2 semanas

**Total**: 6-9 semanas (1.5-2 meses)

---

## 📝 Notas Importantes

> ⚠️ **NÃO INICIAR ANTES DE:**
> - Core transacional (PASSO 6-14) estar sólido ✅
> - Testes de carga em PASSO 13 completados
> - DLQ validado em produção
> - Endpoint `/async` estável em staging

> 💡 **ESTRATÉGIA:**
> - Começar com Fase A (busca simples)
> - Iterar feedback de usuários
> - Depois Fase B (matching inteligente)
> - Deploy progressivo ao vivo

---

## 🔗 Documentação de Referência

- PASSO_13_14_IMPLEMENTATION_SUMMARY.md — Core automação
- PASSO_6_LOCK_CONCORRENTE_REAL.md — Controle de concorrência
- VACANCY_MARKETPLACE_API.md — Vagas existentes

---

**Preparado por:** GitHub Copilot  
**Para iniciação em:** Quando core transacional estiver sólido
