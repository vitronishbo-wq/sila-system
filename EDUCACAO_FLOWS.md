# Fluxos de Trabalho do Módulo de Educação

## Fluxo de Matrícula

Este fluxo descreve o processo de criação de uma nova matrícula no sistema.

```
Endpoint
↓
Schema
↓
Service
↓
Repository
↓
Model
↓
Tabela
```

1.  **Endpoint**: `POST /matriculas/`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/api/endpoints/matricula_routes.py`
    *   **Responsabilidade**: Receber a requisição HTTP para criar uma nova matrícula.

2.  **Schema**: `MatriculaCreate`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/api/schemas/matricula_schema.py`
    *   **Responsabilidade**: Validar os dados de entrada da requisição.

3.  **Service**: `MatriculaService.criar_matricula`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/application/matricula_service.py`
    *   **Responsabilidade**: Orquestrar a lógica de negócio para a criação da matrícula, incluindo validações de regras de negócio, geração de número de processo e persistência.

4.  **Repository**: `SQLAlchemyMatriculaRepository.save`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/infrastructure/repositories/sqlalchemy_matricula_repository.py`
    *   **Responsabilidade**: Mapear o objeto de domínio `Matricula` para o modelo `MatriculaModel` e persistir na base de dados.

5.  **Model**: `MatriculaModel`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/infrastructure/models/matricula_model.py`
    *   **Responsabilidade**: Representar a estrutura da tabela `educacao_matriculas` na base de dados.

6.  **Tabela**: `educacao_matriculas`
    *   **Responsabilidade**: Armazenar os dados da matrícula na base de dados.

## Fluxo de Boletim

Este fluxo descreve o processo de criação de um novo boletim no sistema.

```
Endpoint
↓
Schema
↓
Service
↓
Repository
↓
Model
↓
Tabela
```

1.  **Endpoint**: `POST /boletins/`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/api/endpoints/boletins.py`
    *   **Responsabilidade**: Receber a requisição HTTP para criar um novo boletim.

2.  **Schema**: `BoletimCreate`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/api/schemas/boletim_schema.py`
    *   **Responsabilidade**: Validar os dados de entrada da requisição.

3.  **Service**: `BoletimService` -> `WorkflowService.create_record`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/application/workflow_service.py`
    *   **Responsabilidade**: Orquestrar a lógica de negócio para a criação do boletim, incluindo validações, geração de número de processo e persistência.

4.  **Repository**: `SQLAlchemyBoletimRepository` -> `SQLAlchemyWorkflowRepository.save`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/infrastructure/repositories/_workflow_sqlalchemy_repository.py`
    *   **Responsabilidade**: Mapear o objeto de domínio `WorkflowRecord` para o modelo `BoletimModel` e persistir na base de dados.

5.  **Model**: `BoletimModel`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/infrastructure/models/boletim_model.py`
    *   **Responsabilidade**: Representar a estrutura da tabela `educacao_boletins` na base de dados.

6.  **Tabela**: `educacao_boletins`
    *   **Responsabilidade**: Armazenar os dados do boletim na base de dados.

## Fluxo de Certificado

Este fluxo descreve o processo de criação de um novo certificado no sistema.

```
Endpoint
↓
Schema
↓
Service
↓
Repository
↓
Model
↓
Tabela
```

1.  **Endpoint**: `POST /certificados/conclusao/` (e outros)
    *   **Ficheiro**: `apps/backend/app/modules/educacao/api/endpoints/certificados.py`
    *   **Responsabilidade**: Receber a requisição HTTP para criar um novo certificado.

2.  **Schema**: `CertificadoCreate`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/api/schemas/certificado_schema.py`
    *   **Responsabilidade**: Validar os dados de entrada da requisição.

3.  **Service**: `CertificadoService` -> `WorkflowService.create_record`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/application/workflow_service.py`
    *   **Responsabilidade**: Orquestrar a lógica de negócio para a criação do certificado, incluindo validações, geração de número de processo e persistência.

4.  **Repository**: `SQLAlchemyCertificadoRepository` -> `SQLAlchemyWorkflowRepository.save`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/infrastructure/repositories/_workflow_sqlalchemy_repository.py`
    *   **Responsabilidade**: Mapear o objeto de domínio `WorkflowRecord` para o modelo `CertificadoModel` e persistir na base de dados.

5.  **Model**: `CertificadoModel`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/infrastructure/models/certificado_model.py`
    *   **Responsabilidade**: Representar a estrutura da tabela `educacao_certificados` na base de dados.

6.  **Tabela**: `educacao_certificados`
    *   **Responsabilidade**: Armazenar os dados do certificado na base de dados.

## Fluxo de Transferência

Este fluxo descreve o processo de solicitação de uma transferência de matrícula no sistema.

```
Endpoint
↓
Schema
↓
Service
↓
Repository
↓
Model
↓
Tabela
```

1.  **Endpoint**: `POST /transferencias/`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/api/endpoints/transferencias.py`
    *   **Responsabilidade**: Receber a requisição HTTP para solicitar uma nova transferência.

2.  **Schema**: `TransferenciaCreate`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/api/schemas/transferencia_schema.py`
    *   **Responsabilidade**: Validar os dados de entrada da requisição.

3.  **Service**: `TransferenciaService.solicitar_transferencia`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/application/transferencia_service.py`
    *   **Responsabilidade**: Orquestrar a lógica de negócio para a solicitação da transferência, incluindo validações, verificação de vagas e persistência.

4.  **Repository**: `SQLAlchemyTransferenciaRepository` -> `SQLAlchemyWorkflowRepository.save`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/infrastructure/repositories/sqlalchemy_transferencia_repository.py`
    *   **Responsabilidade**: Mapear o objeto de domínio `WorkflowRecord` para o modelo `TransferenciaModel` e persistir na base de dados.

5.  **Model**: `TransferenciaModel`
    *   **Ficheiro**: `apps/backend/app/modules/educacao/infrastructure/models/transferencia_model.py`
    *   **Responsabilidade**: Representar a estrutura da tabela `educacao_transferencias` na base de dados.

6.  **Tabela**: `educacao_transferencias`
    *   **Responsabilidade**: Armazenar os dados da transferência na base de dados.
