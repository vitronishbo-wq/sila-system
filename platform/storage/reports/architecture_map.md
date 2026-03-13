# Architecture Map

- Generated at: `2026-03-07 13:24:31Z`
- Source of truth: `app/core/module_registry.py`

## Federation Domains

### governance

`administracao_local`, `arquivo_nacional`, `cooperacao_internacional`, `justica`, `planeamento`

### economy

`agricultura`, `apoio_empresarial`, `comercio_externo`, `comercio_servicos`, `financas`, `financas_impostos`, `financas_publicas`, `industria`, `pecuaria`, `pescas`, `pescas_industriais`, `taxpayer`, `turismo`

### social

`assistencia_social`, `ciencia_pesquisa`, `cultura`, `desporto`, `educacao`, `emprego`, `familia`, `igualdade`, `juventude`, `saude`, `saude_primaria`, `seguranca_social`, `tecnologia_inovacao`, `trabalho_inspecao`

### infrastructure

`aguas_saneamento`, `aviacao_civil`, `energia`, `gestao_fundiaria`, `obras_publicas`, `portos_logistica`, `telecomunicacoes`, `transportes_logistica`, `urbanismo_habitacao`

### environment

`ambiente`, `florestas`, `meteorologia`, `patrimonio_cultural`, `petroleo_gas`, `recursos_minerais`

### security

`defesa_consumidor`, `protecao_civil`, `seguranca_alimentar`, `seguranca_publica`

### identity

`identidade_civil`, `identity`, `migracao`, `protecao_dados`, `registo_civil`

### core_system

`bi`, `estatistica`, `operations`, `service_requests`, `statistics`, `workflow`

## Bootstrap Scopes

### API Scope

`agricultura`, `aguas_saneamento`, `ambiente`, `assistencia_social`, `aviacao_civil`, `bi`, `ciencia_pesquisa`, `comercio_externo`, `comercio_servicos`, `cooperacao_internacional`, `cultura`, `defesa_consumidor`, `desporto`, `educacao`, `energia`, `estatistica`, `familia`, `financas`, `financas_impostos`, `financas_publicas`, `florestas`, `gestao_fundiaria`, `identity`, `industria`, `justica`, `juventude`, `meteorologia`, `obras_publicas`, `operations`, `patrimonio_cultural`, `pecuaria`, `pescas`, `protecao_civil`, `registo_civil`, `seguranca_publica`, `seguranca_social`, `service_requests`, `taxpayer`, `telecomunicacoes`, `transportes_logistica`

### Main Scope

`saude`, `statistics`, `workflow`

## Registry Integrity

- Unregistered module folders: **0**
- Bootstrap misalignment (registered but missing on disk): **0**

## Dependency Snapshot

- Distinct edges: **65**
- Circular groups: **0**
