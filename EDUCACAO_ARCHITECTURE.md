# Arquitetura do Módulo de Educação

## Camada de Domínio (Domain Layer)

### Agregados Principais

*   **Escola**: Representa uma instituição de ensino.
*   **Turma**: Representa uma classe dentro de uma escola, para um ano letivo.
*   **Matricula**: Representa a matrícula de um aluno numa escola para um ano letivo específico.
*   **Boletim**: Representa o processo de aprovação do boletim de um aluno.
*   **Certificado**: Representa o processo de emissão do certificado de um aluno.
*   **AcademicIdentity**: Representa a identidade académica única de um aluno no sistema.
*   **Transferencia**: Representa o processo de aprovação da transferência de um aluno.

## Camada de API (API Layer)

### Endpoints

A camada de API expõe os seguintes endpoints, agrupados por responsabilidade:

*   **saúde (health)**: Verifica a saúde da aplicação.
*   **vagas (vacancies)**: Gestão de vagas.
*   **identidade académica (academic_identity)**: Gestão da identidade académica dos alunos.
*   **carteira académica (academic_wallet)**: Gestão da carteira académica dos alunos.
*   **boletins**: Gestão de boletins.
*   **certificados**: Gestão de certificados.
*   **concursos**: Gestão de concursos.
*   **emprego**: Gestão de ofertas de emprego.
*   **escolas**: Gestão de escolas.
*   **formações (formacoes)**: Gestão de formações.
*   **FUC (fuc)**: Gestão do Formulário Único de Cadastro.
*   **inscrições (inscricoes)**: Gestão de inscrições.
*   **marketplace**: Gestão do marketplace.
*   **matrículas (matricula)**: Gestão de matrículas.
*   **métricas (metrics)**: Exposição de métricas da aplicação.
*   **propinas**: Gestão de propinas.
*   **assistente de transferência (transfer_wizard)**: Assistente para o processo de transferência.
*   **transferências (transferencias)**: Gestão de transferências.
*   **automação de transferências (transferencias_automacao)**: Automação do processo de transferência.
*   **turmas**: Gestão de turmas.
*   **universidade**: Gestão de universidades.
*   **assistente de matrícula (wizard_matricula)**: Assistente para o processo de matrícula.

## Camada de Aplicação (Application Layer)

### Serviços

A camada de aplicação contém a lógica de negócio, orquestrando as ações a serem tomadas com base nas solicitações da camada de API. Os principais serviços são:

*   **academic_identity_service**: Gestão da identidade académica dos alunos.
*   **academic_record_service**: Gestão dos registos académicos dos alunos.
*   **academic_wallet_service**: Gestão da carteira académica dos alunos.
*   **automation_bridge**: Ponte para processos de automação.
*   **boletim_service**: Gestão de boletins.
*   **certificado_service**: Gestão de certificados.
*   **concurso_service**: Gestão de concursos.
*   **emprego_service**: Gestão de ofertas de emprego.
*   **encarregados_service**: Gestão de encarregados de educação.
*   **enrollment_transaction_service**: Gestão de transações de matrícula.
*   **event_handlers**: Manipulação de eventos.
*   **formacao_service**: Gestão de formações.
*   **identity_governance_service**: Gestão da governança de identidade.
*   **identity_merge_service**: Gestão da fusão de identidades.
*   **identity_resolution_service**: Gestão da resolução de identidades.
*   **inscricao_service**: Gestão de inscrições.
*   **matricula_service**: Gestão de matrículas.
*   **pagamento_matricula_service**: Gestão de pagamentos de matrícula.
*   **propina_service**: Gestão de propinas.
*   **student_number_generator**: Geração de números de estudante.
*   **transfer_transaction_service**: Gestão de transações de transferência.
*   **transferencia_service**: Gestão de transferências.
*   **universidade_service**: Gestão de universidades.
*   **workflow_service**: Gestão de workflows.
*   **wizard_matricula_service**: Gestão do assistente de matrícula.
*   **marketplace**: Gestão do marketplace.
*   **timeline_service**: Gestão de cronogramas.
*   **transfer_wizard_service**: Gestão do assistente de transferência.

## Camada de Infraestrutura (Infrastructure Layer)

### Repositórios

A camada de infraestrutura é responsável pela persistência de dados. Os principais repositórios são:

*   **academic_identity_repository**: Repositório para a identidade académica.
*   **boletim_repository**: Repositório para boletins.
*   **capacity_repository**: Repositório para a capacidade das instituições.
*   **certificado_repository**: Repositório para certificados.
*   **concurso_repository**: Repositório para concursos.
*   **emprego_repository**: Repositório para ofertas de emprego.
*   **enrollment_repository**: Repositório para matrículas.
*   **escola_repository**: Repositório para escolas.
*   **formacao_repository**: Repositório para formações.
*   **guardian_repository**: Repositório para encarregados de educação.
*   **inscricao_repository**: Repositório para inscrições.
*   **matricula_repository**: Repositório para matrículas.
*   **propina_repository**: Repositório para propinas.
*   **transfer_repository**: Repositório para transferências.
*   **transferencia_repository**: Repositório para transferências.
*   **turma_repository**: Repositório para turmas.
*   **universidade_repository**: Repositório para universidades.
*   **wizard_session_repository**: Repositório para sessões do assistente.
*   **workflow_repository**: Repositório para workflows.
