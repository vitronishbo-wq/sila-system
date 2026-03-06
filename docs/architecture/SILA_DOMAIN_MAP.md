# SILA Domain Map

Status: draft de governança arquitetural.  
Objetivo: organizar os módulos sem mover código nesta fase.

## Domínios Prioritários

1. Governança e Identidade
- `administracao_local`, `arquivo_nacional`, `identidade_civil`, `identity`, `registo_civil`, `migracao`, `planeamento`, `protecao_dados`

2. Serviços Sociais
- `assistencia_social`, `educacao`, `emprego`, `familia`, `igualdade`, `juventude`, `saude`, `saude_primaria`, `seguranca_social`

3. Economia e Produção
- `agricultura`, `apoio_empresarial`, `comercio_externo`, `comercio_servicos`, `financas`, `financas_impostos`, `financas_publicas`, `industria`, `pecuaria`, `pescas`, `pescas_industriais`, `taxpayer`

4. Infraestrutura e Operações
- `aguas_saneamento`, `aviacao_civil`, `energia`, `gestao_fundiaria`, `obras_publicas`, `portos_logistica`, `telecomunicacoes`, `transportes_logistica`, `urbanismo_habitacao`, `operations`, `service_requests`, `workflow`

5. Segurança e Proteção
- `defesa_consumidor`, `justica`, `protecao_civil`, `seguranca_alimentar`, `seguranca_publica`

6. Ambiente e Patrimônio
- `ambiente`, `ciencia_pesquisa`, `cultura`, `estatistica`, `florestas`, `meteorologia`, `patrimonio_cultural`, `petroleo_gas`, `recursos_minerais`, `statistics`, `tecnologia_inovacao`

## Regras da Fase

- Não mover módulos automaticamente nesta etapa.
- Usar `reports/module_inventory.txt` como inventário base.
- Usar `reports/domain_overlap_report.md` para priorizar fusões.
- Executar guardrails antes de qualquer refatoração de fronteira.
