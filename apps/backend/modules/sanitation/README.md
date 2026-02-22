# Módulo Sanitation

Este módulo gerencia registros de saneamento básico no sistema SILA, incluindo:

- Abastecimento de água
- Tratamento de esgoto
- Coleta de resíduos
- Higiene pública

## Melhorias Implementadas

### Novos Campos nos Modelos

- **responsible_entity**: Entidade responsável (ex.: EPAL, ELISAL)
- **technical_manager**: Gestor técnico responsável
- **coverage_percentage**: Percentual de cobertura (substituindo households_covered)

### Estatísticas Avançadas

- Endpoint `/sanitation/{municipality_id}/stats` para estatísticas agregadas
- Cálculo de cobertura média por município
- Breakdown por tipo de saneamento
- Informações de última atualização

### CRUD Completo

- Operações completas de Create, Read, Update, Delete
- Filtros por município
- Validação robusta com Pydantic

## Modelos

### SanitationRecord

```python
class SanitationRecord(Base):
    id: int (Primary Key)
    municipality_id: int (Foreign Key)
    sanitation_type: SanitationType (Enum)
    coverage_percentage: float
    responsible_entity: str (Optional)
    technical_manager: str (Optional)
    last_updated: datetime
```

### SanitationType (Enum)

- `WATER`: Abastecimento de água
- `SEWAGE`: Tratamento de esgoto
- `WASTE`: Coleta de resíduos
- `HYGIENE`: Higiene pública

## Schemas

### SanitationCreate

```python
{
    "municipality_id": 1,
    "sanitation_type": "water",
    "coverage_percentage": 75.5,
    "responsible_entity": "EPAL Angola",
    "technical_manager": "Eng. João Silva"
}
```

### SanitationUpdate

```python
{
    "coverage_percentage": 80.0,
    "technical_manager": "Eng. João Silva (Atualizado)"
}
```

## Endpoints

### Operações CRUD

- `POST /sanitation/`: Criar registro
- `GET /sanitation/`: Listar registros (com filtro por municipality_id)
- `GET /sanitation/{record_id}`: Obter registro específico
- `PUT /sanitation/{record_id}`: Atualizar registro
- `DELETE /sanitation/{record_id}`: Deletar registro

### Estatísticas

- `GET /sanitation/{municipality_id}/stats`: Estatísticas do município

#### Exemplo de Resposta de Estatísticas

```json
{
  "municipality": {
    "id": 1,
    "name": "Luanda",
    "province_id": 1
  },
  "total_records": 3,
  "avg_coverage": 66.67,
  "by_type": {
    "water": 85.0,
    "sewage": 45.0,
    "waste": 70.0
  },
  "last_updated": "2024-09-14T08:30:00"
}
```

## Testes

### Cobertura de Testes

- Criação de registros
- Listagem e filtros
- Atualização parcial
- Deleção
- Estatísticas por município
- Casos edge (município vazio)
- Filtros por município

### Executar Testes

```bash
pytest backend/app/modules/sanitation/tests/test_sanitation.py -v
```

## Dados de Exemplo

O arquivo `examples/sample_data.py` contém:

- Dados realistas para municípios angolanos
- Entidades responsáveis reais (EPAL, ELISAL)
- Gestores técnicos de exemplo
- Funções para popular a base de dados

## Integração com Governance

Este módulo integra-se com o sistema de governance para:

- Auditoria de mudanças
- Relatórios de transparência
- Decisões administrativas sobre saneamento
- Controle de mandatos dos gestores técnicos

## Uso Típico

```python
from app.modules.sanitation.services.sanitation_service import SanitationService
from app.modules.sanitation.schemas.sanitation import SanitationCreate

# Criar registro
data = SanitationCreate(
    municipality_id=1,
    sanitation_type="water",
    coverage_percentage=85.0,
    responsible_entity="EPAL",
    technical_manager="Eng. João Silva"
)
record = SanitationService.create_record(db, data)

# Obter estatísticas
stats = SanitationService.get_statistics(db, municipality_id=1)
```
