# Testes de Unidade dos Serviços

Este diretório contém testes de unidade focados na lógica de negócio dos serviços do
sistema SILA, com mocking adequado para isolar a camada de persistência.

## 📋 Estrutura

```
tests/unit/
├── conftest.py                    # Configuração e fixtures compartilhadas
├── test_sanitation_service.py     # Testes do serviço de saneamento
├── test_justice_service.py        # Testes do serviço de justiça
├── test_academic_service.py       # Testes do serviço acadêmico
├── run_unit_tests.py             # Script para executar todos os testes
├── reports/                      # Relatórios gerados
│   ├── coverage.json            # Relatório de cobertura
│   ├── unit_test_summary.json   # Resumo dos testes
│   └── htmlcov/                 # Relatório HTML de cobertura
└── README.md                     # Este arquivo
```

## 🎯 Objetivos

1. **Isolar a Lógica de Negócio**: Testar as regras de negócio sem dependências externas
2. **Mocking da Persistência**: Simular interações com banco de dados
3. **Cobertura Abrangente**: Garantir cobertura dos principais fluxos de negócio
4. **Refatoração Segura**: Permitir refatorações com confiança nos testes

## 🧪 Executando os Testes

### Executar Todos os Testes

```bash
python run_unit_tests.py
```

### Executar Testes Específicos

```bash
# Testes do serviço de saneamento
pytest test_sanitation_service.py -v

# Testes do serviço de justiça
pytest test_justice_service.py -v

# Testes do serviço acadêmico
pytest test_academic_service.py -v
```

### Executar com Cobertura

```bash
pytest --cov=modules.sanitation.services test_sanitation_service.py
pytest --cov=modules.justice.services test_justice_service.py
pytest --cov=modules.education.services test_academic_service.py
```

## 📊 Relatórios

Após executar `run_unit_tests.py`, os seguintes relatórios são gerados:

- **`reports/unit_test_summary.json`**: Resumo completo dos testes
- **`reports/coverage.json`**: Dados detalhados de cobertura
- **`reports/htmlcov/index.html`**: Relatório visual de cobertura

## 🔧 Fixtures e Mocks

### Fixtures Disponíveis

- `sample_user_data`: Dados de exemplo para usuário
- `sample_notification_data`: Dados de exemplo para notificação
- `mock_db_session`: Mock de sessão do banco de dados
- `mock_request`: Mock de request FastAPI

### Estrutura de Mocks

```python
@pytest.fixture
def mock_db(self):
    """Mock do banco de dados."""
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    # Mock para query
    query_mock = MagicMock()
    query_mock.filter.return_value = query_mock
    query_mock.first.return_value = None
    query_mock.all.return_value = []
    db.query.return_value = query_mock

    return db
```

## 📋 Categorias de Testes

### 1. Testes de Criação

- Validação de dados de entrada
- Tratamento de erros de banco
- Verificação de duplicatas

### 2. Testes de Validação

- Regras de negócio específicas
- Validação de formatos e ranges
- Verificação de dependências

### 3. Testes de Atualização

- Transições de status válidas/inválidas
- Atualização de campos específicos
- Tratamento de concorrência

### 4. Testes de Cálculo

- Cálculos de custos e taxas
- Médias e estatísticas
- Prazos e datas

### 5. Testes de Regras Complexas

- Verificação de conflitos
- Análise de complexidade
- Geração de relatórios

## 🎯 Foco nos Serviços

### SanitationService

- **Validação de Serviços**: Tipos, localizações, datas
- **Cálculo de Prioridade**: Baseado em tipo e urgência
- **Regras de Agendamento**: Horário comercial, fins de semana
- **Tratamento de Água**: Parâmetros químicos e físicos
- **Estatísticas**: Relatórios e métricas operacionais

### JusticeService

- **Validação de Casos**: Números de processo, valores
- **Transições de Status**: Fluxo processual válido
- **Cálculo de Custas**: Baseado em tipo e valor
- **Prazos Processuais**: Diferentes por tipo de caso
- **Atribuição de Advogados**: Regras de distribuição

### AcademicService

- **Matrículas**: Pré-requisitos, vagas, níveis
- **Notas**: Validação, cálculo de médias
- **Progresso Acadêmico**: Créditos, GPA, status
- **Gestão de Cursos**: Criação, disponibilidade
- **Relatórios**: Desempenho e estatísticas

## 📈 Métricas de Qualidade

### Cobertura Esperada

- **Mínimo**: 70% de cobertura de código
- **Ideal**: 85%+ para lógica crítica
- **Foco**: 100% para regras de negócio principais

### Tipos de Testes

- **Testes Síncronos**: Operações simples
- **Testes Assíncronos**: Operações com I/O
- **Testes de Mock**: Isolamento de dependências
- **Testes de Integração**: Fluxos completos

## 🔍 Boas Práticas

### 1. Nomenclatura Clara

```python
def test_create_sanitation_record_success(self, service, mock_db, sample_data):
def test_create_sanitation_record_with_validation_error(self, service, mock_db):
def test_update_case_status_invalid_transition(self, service, mock_db, mock_case):
```

### 2. Arrange-Act-Assert

```python
async def test_example(self):
    # Arrange
    mock_db.query.return_value.first.return_value = mock_object

    # Act
    result = await service.method_call(params)

    # Assert
    assert result is not None
    mock_db.commit.assert_called_once()
```

### 3. Mocking Adequado

```python
@patch('modules.sanitation.services.get_db')
async def test_with_patch(self, mock_get_db, service):
    mock_session = MagicMock()
    mock_get_db.return_value = mock_session
    # ... teste
```

### 4. Testes de Erro

```python
async def test_error_handling(self, service, mock_db):
    mock_db.commit.side_effect = Exception("Erro de conexão")

    with pytest.raises(Exception, match="Erro de conexão"):
        await service.method_that_fails()
```

## 🚀 Integração CI/CD

### GitHub Actions

```yaml
- name: Run Unit Tests
  run: |
    cd backend/tests/unit
    python run_unit_tests.py

- name: Upload Coverage Reports
  uses: codecov/codecov-action@v3
  with:
    file: ./backend/tests/unit/reports/coverage.json
```

### Qualidade Automatizada

- ✅ Verificação de existência de arquivos
- ✅ Contagem mínimo de testes por módulo
- ✅ Validação de sintaxe
- ✅ Verificação de imports
- ✅ Cobertura mínima de código

## 📝 Relatórios Gerados

### Estrutura do JSON de Resumo

```json
{
  "timestamp": "2025-10-26T10:00:00",
  "test_results": {
    "test_sanitation_service.py": {
      "status": "passed",
      "tests": 25
    }
  },
  "coverage_success": true,
  "analysis": {
    "total_test_functions": 75,
    "async_tests": 45,
    "total_lines": 1200
  },
  "summary": {
    "total_tests": 75,
    "passed_files": 3,
    "failed_files": 0
  }
}
```

## 🔄 Manutenção

### Adicionando Novos Testes

1. Siga o padrão `test_[module]_service.py`
2. Use fixtures compartilhadas quando possível
3. Mantenha foco na lógica de negócio
4. Adicione mocks para dependências externas

### Atualizando Testes

1. Execute testes antes de modificar
2. Atualize mocks se a interface mudar
3. Verifique cobertura após mudanças
4. Documente regras de negócio novas

## 🐛 Debug

### Problemas Comuns

- **Import Error**: Verifique PYTHONPATH
- **Mock não funciona**: Confirme patch correto
- **Teste assíncrono falha**: Use @pytest.mark.asyncio
- **Cobertura baixa**: Verifique branches não testados

### Comandos Úteis

```bash
# Debug específico
pytest test_sanitation_service.py::TestSanitationServiceUnit::test_create_sanitation_record_success -v -s

# Verificar cobertura específica
pytest --cov=modules.sanitation.services --cov-report=term-missing

# Executar com logs
pytest --log-cli-level=DEBUG
```

## 📚 Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Nota**: Estes testes são focados em unidade da lógica de negócio. Para testes de
integração completa, consulte `tests/integration/`.
