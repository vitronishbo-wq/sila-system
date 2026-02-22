# Módulo Training - Sistema SILA

## Visão Geral

O módulo Training é responsável pelo gerenciamento completo de programas de treinamento,
capacitação e certificação no sistema SILA. Oferece funcionalidades para criação de
programas educacionais, gestão de inscrições, acompanhamento de progresso e emissão de
certificados.

## Características Principais

- **Gestão de Programas**: Criação e administração de programas de treinamento
- **Sistema de Inscrições**: Controle de inscrições com validação de capacidade
- **Acompanhamento de Progresso**: Registro de notas e frequência
- **Certificação Automática**: Emissão de certificados baseada em critérios
- **Estatísticas e Relatórios**: Análise de desempenho e participação
- **Integração Modular**: Conecta com outros módulos do sistema SILA

## Modelos de Dados

### TrainingProgram

Representa um programa de treinamento ou capacitação.

```python
class TrainingProgram(Base):
    id: int                    # Identificador único
    title: str                 # Título do programa
    description: str           # Descrição detalhada
    category: TrainingCategory # Categoria (professional, civic, government, technical)
    start_date: datetime       # Data de início
    end_date: datetime         # Data de término
    location: str              # Local de realização
    instructor: str            # Instrutor responsável
    max_participants: int      # Capacidade máxima
    requirements: str          # Pré-requisitos
    objectives: str            # Objetivos do programa
    created_at: datetime       # Data de criação
    updated_at: datetime       # Última atualização
```

### TrainingEnrollment

Representa uma inscrição de usuário em um programa.

```python
class TrainingEnrollment(Base):
    id: int                     # Identificador único
    program_id: int             # ID do programa
    user_id: int                # ID do usuário
    status: EnrollmentStatus    # Status (pending, confirmed, completed, cancelled)
    enrollment_date: datetime   # Data da inscrição
    completion_date: datetime   # Data de conclusão
    grade: float                # Nota final (0-20)
    attendance_percentage: float # Percentual de frequência
    certificate_issued: bool    # Certificado emitido
    certificate_number: str     # Número do certificado
    feedback: str               # Feedback do participante
    created_at: datetime        # Data de criação
    updated_at: datetime        # Última atualização
```

## Schemas Pydantic

### Criação de Programa

```python
class TrainingProgramCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: TrainingCategory
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    instructor: Optional[str] = None
    max_participants: Optional[int] = None
    requirements: Optional[str] = None
    objectives: Optional[str] = None
```

### Inscrição

```python
class EnrollmentCreate(BaseModel):
    program_id: int
    user_id: int
```

### Conclusão de Inscrição

```python
class EnrollmentCompletion(BaseModel):
    grade: float = Field(ge=0, le=20)
    attendance_percentage: float = Field(ge=0, le=100)
    feedback: Optional[str] = None
```

## Endpoints da API

### Programas de Treinamento

| Método | Endpoint                              | Descrição                    | Autenticação |
| ------ | ------------------------------------- | ---------------------------- | ------------ |
| GET    | `/training/programs`                  | Lista programas com filtros  | Não          |
| POST   | `/training/programs`                  | Cria novo programa           | Sim          |
| GET    | `/training/programs/{id}`             | Obtém programa específico    | Não          |
| PUT    | `/training/programs/{id}`             | Atualiza programa            | Sim          |
| DELETE | `/training/programs/{id}`             | Remove programa              | Sim          |
| GET    | `/training/programs/{id}/enrollments` | Lista inscrições do programa | Não          |

### Inscrições

| Método | Endpoint                              | Descrição                  | Autenticação |
| ------ | ------------------------------------- | -------------------------- | ------------ |
| GET    | `/training/enrollments`               | Lista inscrições           | Não          |
| POST   | `/training/enrollments`               | Cria nova inscrição        | Sim          |
| GET    | `/training/enrollments/{id}`          | Obtém inscrição específica | Não          |
| PUT    | `/training/enrollments/{id}`          | Atualiza inscrição         | Sim          |
| POST   | `/training/enrollments/{id}/complete` | Completa inscrição         | Sim          |
| POST   | `/training/enrollments/{id}/cancel`   | Cancela inscrição          | Sim          |

### Usuários e Certificados

| Método | Endpoint                                      | Descrição             | Autenticação |
| ------ | --------------------------------------------- | --------------------- | ------------ |
| GET    | `/training/users/{user_id}/enrollments`       | Inscrições do usuário | Não          |
| GET    | `/training/certificates/{certificate_number}` | Verifica certificado  | Não          |

### Estatísticas e Descoberta

| Método | Endpoint               | Descrição                    | Autenticação |
| ------ | ---------------------- | ---------------------------- | ------------ |
| GET    | `/training/stats`      | Estatísticas gerais          | Não          |
| GET    | `/training/categories` | Lista categorias disponíveis | Não          |

## Regras de Negócio

### Inscrições

- **Duplicação**: Usuário não pode se inscrever duas vezes no mesmo programa
- **Capacidade**: Respeitado limite máximo de participantes
- **Status**: Fluxo controlado (pending → confirmed → completed/cancelled)

### Certificação

- **Critérios**: Nota ≥ 10 E frequência ≥ 75%
- **Numeração**: Certificados têm numeração única
- **Verificação**: Certificados podem ser verificados publicamente

### Validações

- **Datas**: Data de fim deve ser posterior à data de início
- **Notas**: Escala de 0 a 20 pontos
- **Frequência**: Percentual de 0 a 100%

## Exemplos de Uso

### Criar Programa de Capacitação

```python
program_data = {
    "title": "Formação em Administração Pública",
    "description": "Capacitação de servidores municipais",
    "category": "government",
    "start_date": "2025-10-01T09:00:00",
    "end_date": "2025-11-01T17:00:00",
    "location": "Centro de Formação - Luanda",
    "instructor": "Dr. António Silva",
    "max_participants": 30,
    "requirements": "Ensino médio completo",
    "objectives": "Melhorar eficiência administrativa"
}

response = requests.post(
    "http://localhost:8000/training/programs",
    json=program_data,
    headers={"Authorization": "Bearer <token>"}
)
```

### Inscrever Usuário

```python
enrollment_data = {
    "program_id": 1,
    "user_id": 123
}

response = requests.post(
    "http://localhost:8000/training/enrollments",
    json=enrollment_data,
    headers={"Authorization": "Bearer <token>"}
)
```

### Completar Treinamento

```python
completion_data = {
    "grade": 16.5,
    "attendance_percentage": 90.0,
    "feedback": "Excelente programa, muito útil"
}

response = requests.post(
    "http://localhost:8000/training/enrollments/1/complete",
    json=completion_data,
    headers={"Authorization": "Bearer <token>"}
)
```

## Integração com Outros Módulos

### Education

- Compartilha categorias educacionais
- Integra com sistema de usuários estudantes
- Complementa formação acadêmica

### Governance

- Programas de capacitação para servidores
- Treinamentos obrigatórios por função
- Relatórios de compliance

### Citizens

- Programas de educação cívica
- Capacitação profissional
- Certificações para serviços públicos

### Service Hub

- Registro de serviços de treinamento
- Roteamento de requisições
- Monitoramento de uso

## Segurança

### Autenticação

- Endpoints de modificação requerem JWT válido
- Verificação de permissões por role
- Auditoria de ações administrativas

### Autorização

- Instrutores podem gerenciar seus programas
- Administradores têm acesso completo
- Usuários veem apenas suas inscrições

### Validação

- Sanitização de dados de entrada
- Validação de tipos e formatos
- Prevenção de ataques de injeção

## Monitoramento e Métricas

### Estatísticas Disponíveis

- Total de programas ativos/inativos
- Taxa de conclusão por categoria
- Certificados emitidos por período
- Participação por região/município
- Avaliação média dos programas

### Logs e Auditoria

- Criação/modificação de programas
- Inscrições e cancelamentos
- Emissão de certificados
- Tentativas de fraude

## Testes Automatizados

O módulo inclui suite completa de testes cobrindo:

- **Criação e validação** de programas
- **Gestão de inscrições** e duplicação
- **Regras de certificação** automática
- **Filtros e paginação** de listagens
- **Validações de negócio** e edge cases
- **Integração de endpoints** completa

### Executar Testes

```bash
# Testes específicos do módulo
pytest backend/app/modules/training/tests/

# Com cobertura
pytest --cov=app.modules.training backend/app/modules/training/tests/
```

## Estrutura de Arquivos

```
training/
├── __init__.py
├── README.md
├── models/
│   ├── __init__.py
│   └── training.py
├── schemas/
│   ├── __init__.py
│   └── training.py
├── services/
│   ├── __init__.py
│   └── training_service.py
├── routes/
│   └── training_routes.py
├── tests/
│   ├── __init__.py
│   └── test_training.py
└── examples/
    └── sample_data.py
```

## Roadmap e Melhorias Futuras

### Versão 2.0

- [ ] Sistema de avaliação por competências
- [ ] Integração com plataformas de e-learning
- [ ] Certificados digitais com blockchain
- [ ] Gamificação e badges

### Versão 2.1

- [ ] Relatórios avançados com BI
- [ ] API para dispositivos móveis
- [ ] Notificações push e email
- [ ] Sistema de recomendação de cursos

### Integrações Planejadas

- [ ] Microsoft Teams/Zoom para aulas online
- [ ] Sistema de pagamento para cursos pagos
- [ ] Integração com LinkedIn Learning
- [ ] Exportação para sistemas de RH

## Suporte e Contribuição

Para dúvidas, sugestões ou contribuições:

1. **Issues**: Reporte bugs ou solicite features
2. **Pull Requests**: Contribua com melhorias
3. **Documentação**: Ajude a melhorar a documentação
4. **Testes**: Adicione casos de teste

## Licença

Este módulo faz parte do Sistema SILA e está sob a mesma licença do projeto principal.

---

## Tabela-Resumo dos Módulos SILA-System

### Módulos de Serviços Públicos

| Módulo          | Objetivo Principal                                                  | Dependências Principais                               |
| --------------- | ------------------------------------------------------------------- | ----------------------------------------------------- |
| **citizenship** | Gestão de processos de cidadania, naturalização e nacionalidade     | `auth`, `documents`, `registry`, `governance`         |
| **commercial**  | Licenças comerciais, registros empresariais e atividades econômicas | `finance`, `documents`, `registry`, `service_hub`     |
| **education**   | Sistema educacional, matrículas, notas e certificados acadêmicos    | `citizens`, `documents`, `training`, `statistics`     |
| **health**      | Serviços de saúde, consultas, vacinas e registros médicos           | `citizens`, `appointments`, `documents`, `statistics` |
| **justice**     | Processos judiciais, certidões criminais e serviços jurídicos       | `citizens`, `documents`, `registry`, `governance`     |
| **sanitation**  | Saneamento básico, água, esgoto e gestão ambiental                  | `citizens`, `finance`, `urbanism`, `monitoring`       |
| **social**      | Assistência social, benefícios e programas sociais                  | `citizens`, `finance`, `documents`, `statistics`      |
| **urbanism**    | Planejamento urbano, licenças de construção e zoneamento            | `citizens`, `documents`, `finance`, `location`        |

### Módulos de Gestão e Administração

| Módulo         | Objetivo Principal                                            | Dependências Principais                           |
| -------------- | ------------------------------------------------------------- | ------------------------------------------------- |
| **governance** | Estrutura administrativa, mandatos e decisões governamentais  | `auth`, `citizens`, `documents`, `statistics`     |
| **finance**    | Gestão financeira, orçamentos, receitas e despesas públicas   | `citizens`, `documents`, `payment`, `statistics`  |
| **registry**   | Registro civil, nascimentos, óbitos e estado civil            | `citizens`, `documents`, `identity`, `statistics` |
| **documents**  | Gestão documental, emissão e validação de documentos oficiais | `citizens`, `auth`, `identity`, `service_hub`     |
| **identity**   | Gestão de identidades, cartões de identidade e autenticação   | `citizens`, `documents`, `auth`, `registry`       |

### Módulos de Infraestrutura e Suporte

| Módulo           | Objetivo Principal                                         | Dependências Principais              |
| ---------------- | ---------------------------------------------------------- | ------------------------------------ |
| **auth**         | Autenticação, autorização e controle de acesso             | `citizens`, `identity`, `monitoring` |
| **service_hub**  | Orquestração e descoberta de serviços públicos digitais    | Todos os módulos de serviço          |
| **integration**  | Integração com sistemas externos e APIs de terceiros       | `auth`, `service_hub`, `monitoring`  |
| **monitoring**   | Monitoramento, logs, métricas e observabilidade do sistema | Todos os módulos                     |
| **notification** | Sistema de notificações, alertas e comunicações            | `citizens`, `auth`, `service_hub`    |
| **payment**      | Processamento de pagamentos e taxas de serviços públicos   | `finance`, `citizens`, `service_hub` |

### Módulos de Dados e Análise

| Módulo         | Objetivo Principal                                        | Dependências Principais               |
| -------------- | --------------------------------------------------------- | ------------------------------------- |
| **statistics** | Estatísticas, relatórios e análise de dados do sistema    | Todos os módulos de serviço           |
| **reports**    | Geração de relatórios gerenciais e operacionais           | `statistics`, `governance`, `finance` |
| **location**   | Gestão de localização geográfica e divisão administrativa | `citizens`, `governance`, `address`   |
| **address**    | Gestão de endereços e códigos postais                     | `citizens`, `location`, `registry`    |

### Módulos Especializados

| Módulo           | Objetivo Principal                                    | Dependências Principais                              |
| ---------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| **training**     | Programas de treinamento, capacitação e certificação  | `citizens`, `education`, `governance`, `service_hub` |
| **appointments** | Agendamento de consultas e atendimentos públicos      | `citizens`, `health`, `service_hub`                  |
| **complaints**   | Sistema de ouvidoria, reclamações e feedback cidadão  | `citizens`, `governance`, `monitoring`               |
| **journeys**     | Jornadas do cidadão e fluxos de processos             | `service_hub`, `citizens`, `statistics`              |
| **internal**     | Processos internos e gestão administrativa            | `auth`, `governance`, `monitoring`                   |
| **common**       | Utilitários, helpers e funcionalidades compartilhadas | Nenhuma (base para outros módulos)                   |

### Resumo Quantitativo

- **Total de Módulos**: 30
- **Módulos de Serviços Públicos**: 8
- **Módulos de Gestão**: 5
- **Módulos de Infraestrutura**: 6
- **Módulos de Dados**: 4
- **Módulos Especializados**: 6
- **Módulo Base**: 1 (common)

### Dependências Mais Críticas

1. **citizens** - Usado por 20+ módulos
2. **auth** - Usado por 15+ módulos
3. **documents** - Usado por 12+ módulos
4. **service_hub** - Usado por 10+ módulos
5. **statistics** - Usado por 8+ módulos

### Arquitetura Modular

O sistema SILA segue uma arquitetura modular onde:

- Módulos de **infraestrutura** fornecem serviços base
- Módulos de **serviços públicos** implementam funcionalidades específicas
- Módulos de **gestão** controlam processos administrativos
- Módulos de **dados** agregam informações para análise
- **service_hub** orquestra a comunicação entre módulos
