# ==============================================================================
# SILA System - Gerador de Documentos da Fase 2
# ------------------------------------------------------------------------------
# Objetivo:
#   Gerar os documentos de marco (TODO Oficial e Sumário Visual) para a Fase 2
#   (Análise de Repetitividade e Consolidação de Bibliotecas Compartilhadas),
#   garantindo consistência com os documentos FASE_1_* e PRE_FASE_2_*.
#
# Uso:
#   python generate_phase2_docs.py list
#   python generate_phase2_docs.py generate --all
#   python generate_phase2_docs.py generate --name FASE_2_TODO_OFICIAL --force
# ==============================================================================

import argparse
import os
import pathlib
from datetime import datetime
from typing import Dict, Any, List


# Ensure directory utility (idempotent)
def ensure_dir(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


# --- Simulação de Utilitários de Codegen (para ser self-contained) ---


class FileManager:
    """Gerencia a escrita segura de arquivos."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

    def write_file(self, filepath: str, content: str, force: bool = False) -> bool:
        """Escreve o conteúdo no caminho especificado."""
        if self.dry_run:
            print(f"[DRY-RUN] Arquivo seria gerado em: {filepath}")
            return True

        if os.path.exists(filepath) and not force:
            print(
                f"[WARN] Arquivo já existe: {filepath}. Use --force para sobrescrever."
            )
            return False

        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[OK] Arquivo gerado/atualizado em: {filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Falha ao escrever {filepath}: {e}")
            return False


# --- Definição dos Templates ---

PHASE2_DOC_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "FASE_2_TODO_OFICIAL": {
        "output_path": "FASE_2_TODO_OFICIAL.md",
        "title": "Documento de Planejamento e TODO Oficial da Fase 2",
        "description": "Focada na Análise de Repetitividade de Scripts e na Criação de Bibliotecas Compartilhadas (scripts/lib).",
        "template": """# FASE 2: TODO OFICIAL - Análise e Consolidação de Scripts

> Status: EM EXECUÇÃO | Responsável: [Responsável aqui] | Data de Geração: {timestamp}

---

## 1. Contexto e Princípios Obrigatórios

A Fase 2 visa atacar a repetitividade funcional em scripts de Nível 2 e Nível 3, preparando o terreno para a refatoração de Nível 1 na Fase 3. É **OBRIGATÓRIO** respeitar os documentos mestres:

* **[MAPA_DE_TOQUE_SEGURO_FASE_2.md]**: Limites estruturais (Nível 1 intocável)
* **[PRE_FASE_2_ANALISE_CRITICA_LIMITES.md]**: Metas de consolidação (redução de 20% de código duplicado em funções comuns)
* **[SEIS_PRINCIPIOS_OBRIGATORIOS.txt]**: Princípios de segurança e idempotência (NÃO PODEM ser violados)

---

## 2. Fase 2A: Análise de Repetitividade (Diagnóstico)

O foco é identificar e mapear as funções duplicadas ou que podem ser externalizadas em helpers. **NENHUM script deve ser alterado nesta subfase, apenas analisado.**

| Item | Descrição | Status | Observações |
|------|-----------|--------|-------------|
| **[2A.1] Escaneamento** | Uso da ferramenta de análise (`tools/analysis/project_analyzer.sh` ou similar) para gerar o primeiro relatório de repetitividade de código. | ⬜ Pendente | Gerar relatório `FASE_2_RELATORIO_ANALISE_REPETITIVIDADE.md` |
| **[2A.2] Mapeamento de Helpers** | Criar um mapa de 1:1 (Função Duplicada -> Helper Comum) para `deploy`, `database` e `nginx` | ⬜ Pendente | Foco em scripts de Nível 2 e Nível 3 |
| **[2A.3] Checklist de Nível 2** | Aplicação do checklist de manutenção/segurança (para scripts em `maintenance/`) | ⬜ Pendente | Utilizar `FASE_2_CHECKLIST_ANALISE_SCRIPTS.md` |
| **[2A.4] Aprovação de Design** | Aprovação da arquitetura de helpers (funções, nomes e contratos) pelo time de Core | ⬜ Pendente | Evitar acoplamento com o Nível 1 |

---

## 3. Fase 2B: Bibliotecas Compartilhadas (`scripts/lib/`)

Esta fase é a de implementação, criando os arquivos de biblioteca sem modificar os scripts que os chamarão (apenas a implementação da função).

| Item | Descrição | Status | Destino Sugerido |
|------|-----------|--------|------------------|
| **[2B.1] Criação de `scripts/lib`** | Criar o diretório para isolar as bibliotecas compartilhadas | ⬜ Pendente | `scripts/lib/` |
| **[2B.2] Helper de Deploy** | Extração de funções de start/stop/status comuns | ⬜ Pendente | `scripts/lib/deploy_helpers.sh` |
| **[2B.3] Helper de Database** | Extração de funções de conexão/validação/inicialização de DB | ⬜ Pendente | `scripts/lib/database_helpers.sh` |
| **[2B.4] Helper de NGINX** | Extração de funções de log/status/diagnóstico do NGINX | ⬜ Pendente | `scripts/lib/nginx_helpers.sh` |
| **[2B.5] Integração e Testes** | Garantir que o `require`/`source` das bibliotecas funciona em Nível 2 e Nível 3 | ⬜ Pendente | Testes de integração automatizados (sempre!) |

---

## 4. Saídas Oficiais e Gate para Fase 3

A Fase 2 só é considerada completa após a geração dos relatórios e a execução de testes de não-regressão.

### Relatórios Obrigatórios

- **Relatório de Análise:** `FASE_2_RELATORIO_ANALISE_REPETITIVIDADE.md`
- **Status de Bibliotecas:** `FASE_2_LIBS_COMPARTILHADAS_STATUS.md`
- **Sumário Visual:** `FASE_2_SUMARIO_VISUAL.md` com status `FASE 2A: CONCLUÍDA` e `FASE 2B: [Em progresso/Concluída]`

---

## 5. Roadmap Temporal

| Semana | Atividade | Responsável | Status |
|--------|-----------|------------|--------|
| Semana 1 | Fase 2A: Análise completa | TBD | ⬜ Não iniciado |
| Semana 2 | Fase 2B: Criação de libs | TBD | ⬜ Não iniciado |
| Semana 3 | Testes de integração | TBD | ⬜ Não iniciado |
| Semana 4 | Gate para Fase 3 | TBD | ⬜ Não iniciado |

---

## 6. Critérios de Sucesso

- ✅ Zero scripts Nível 1 modificados estruturalmente
- ✅ Mínimo 20% redução de duplicação de código
- ✅ 100% de testes de não-regressão passando
- ✅ Documentação completa de cada helper
- ✅ Aprovação pelo time de Core para transição à Fase 3

---

## 7. Anexos e Referências

- 📄 `PRE_FASE_2_ANALISE_CRITICA_LIMITES.md`
- 📄 `MAPA_DE_TOQUE_SEGURO_FASE_2.md`
- 📄 `SEIS_PRINCIPIOS_OBRIGATORIOS.txt`
- 📄 `PRE_FASE_2_README.md`
- 🔧 `tools/codegen/generate_phase2_docs.py`

---

**Data de Criação:** {timestamp}
**Última Atualização:** {timestamp}
**Próximo Marco:** FASE 2A Diagnóstico Completo
""",
    },
    "FASE_2_SUMARIO_VISUAL": {
        "output_path": "FASE_2_SUMARIO_VISUAL.md",
        "title": "Sumário Visual da Fase 2",
        "description": "Visão rápida do status da Fase 2 (Análise e Consolidação de Scripts).",
        "template": """# FASE 2: SUMÁRIO VISUAL DE CONSOLIDAÇÃO

> Data de Geração: {timestamp}

---

## 📊 Status da Consolidação de Scripts

| Métrica | Fase 1 (Base) | Meta Fase 2 | Status Atual |
|---------|---------------|------------|--------------|
| **Scripts Total** | 57 | 57 | 57 |
| **Scripts no Nível 1** | 21 | 21 (intocável) | 21 ✅ |
| **Scripts no Nível 2/3** | 41 | 41 (analisável) | 41 |
| **Duplicação Estimada** | N/A | Redução de 20% | Aguardando análise |
| **Funções em `scripts/lib`** | 0 | 12+ | 0 |

---

## 🚧 Status das Subfases

### FASE 2A: Análise de Repetitividade

- **[✔]** Leitura e aceitação de `PRE_FASE_2_*`
- **[✔]** Geração de ferramenta de análise (`tools/codegen/generate_phase2_docs.py`)
- **[ ]** Relatório de análise gerado (`FASE_2_RELATORIO_ANALISE_REPETITIVIDADE.md`)
- **[ ]** Mapa de helpers aprovado
- **[ ]** Checklist de Nível 2 aplicado

**Progresso:** 2/5 ✅

### FASE 2B: Implementação de Libs Compartilhadas

- **[ ]** Diretório `scripts/lib/` criado
- **[ ]** `scripts/lib/deploy_helpers.sh` implementado
- **[ ]** `scripts/lib/database_helpers.sh` implementado
- **[ ]** `scripts/lib/nginx_helpers.sh` implementado
- **[ ]** Testes de integração validados

**Progresso:** 0/5 ⏳

---

## 🔒 Princípios de Segurança (Requisito Obrigatório)

Os documentos `MAPA_DE_TOQUE_SEGURO_FASE_2.md` e `SEIS_PRINCIPIOS_OBRIGATORIOS.txt` **PROÍBEM** modificações diretas no Nível 1.

| Aspecto | Valor | Status |
|--------|-------|--------|
| **Toques no Nível 1** | 0 (ZERO) | ✅ Mantido |
| **Compliance com 6 Princípios** | 100% | 🔍 Sob revisão |
| **Reversibilidade** | 100% | ✅ Garantida |

---

## 📈 Projeção de Impacto

```
Hoje:               57 scripts (9 categorias, 0 libs)
Após FASE 2A:       57 scripts (análise completa, documentado)
Após FASE 2B:       57 scripts (com 3 libs compartilhadas)
Antes FASE 3:       Pronto para consolidação Nível 3
```

---

## 🎯 Próximos Passos

1. **IMEDIATO:** Iniciar FASE 2A (Análise de repetitividade)
2. **SEMANA 1:** Gerar `FASE_2_RELATORIO_ANALISE_REPETITIVIDADE.md`
3. **SEMANA 2:** Iniciar FASE 2B (Criação de libs)
4. **SEMANA 3:** Testes e aprovação
5. **SEMANA 4:** Gate para Fase 3

---

## 📞 Documentos de Referência

- 📄 `FASE_2_TODO_OFICIAL.md` (Este documento de tarefas)
- 📄 `PRE_FASE_2_ANALISE_CRITICA_LIMITES.md` (Fundação técnica)
- 📄 `MAPA_DE_TOQUE_SEGURO_FASE_2.md` (Matriz de permissões)
- 📄 `SEIS_PRINCIPIOS_OBRIGATORIOS.txt` (Regras não-negociáveis)
- 🔧 `tools/codegen/generate_phase2_docs.py` (Gerador de docs)

---

**Status Geral:** 🟡 EM PROGRESSO (PRÉ-FASE 2 CONCLUÍDA)
**Próximo Marco:** FASE 2A Completa (Target: 1 semana)
**Última Atualização:** {timestamp}
""",
    },
    # ============================================================
    # NEW: CHECKLIST FASE 2 (prefixo médio)
    # ============================================================
    "FASE_2_CHECKLIST_ANALISE_SCRIPTS": {
        "output_path": "docs/fase_2/checklist_fase2_analise_scripts.md",
        "title": "Checklist Fase 2 – Análise Estrutural de Scripts",
        "description": "Checklist completo para mapeamento de duplicações e classificação de scripts.",
        "template": """# Checklist Fase 2 – Análise Estrutural de Scripts
Data de Geração: {timestamp}

Este checklist cobre toda a análise de duplicações, mapeamento de funções
repetidas, identificação de padrões, classificação por Nível (1/2/3),
e aplicação dos 6 Princípios Obrigatórios.

## 1. Princípios Obrigatórios
- [ ] **P1 — Intocabilidade Nível 1**
- [ ] **P2 — Reversibilidade 100%**
- [ ] **P3 — Nenhuma alteração funcional na Fase 2A**
- [ ] **P4 — Libs só na Fase 2B**
- [ ] **P5 — Idempotência**
- [ ] **P6 — Transparência completa**

## 2. Classificação de Scripts
- [ ] Confirmar lista final:
  - 21 scripts → **Nível 1 (intocáveis)**
  - 36 scripts → **Nível 2**
  - 15 scripts → **Nível 3**

## 3. Mapeamento de Duplicações
- [ ] Identificar funções repetidas entre scripts
- [ ] Criar matriz de correspondência
- [ ] Detectar agrupamentos (clusters) de repetição
- [ ] Qualificar funções candidatas a libs

## 4. Análise Técnica (por script)
- [ ] Extrair funções
- [ ] Classificar por Nível
- [ ] Apontar duplicações
- [ ] Registrar dependências
- [ ] Registrar chamadas a binários externos

## 5. Saídas Obrigatórias
- [ ] Relatório técnico fase2_relatorio_analise.md
- [ ] Mapa de helpers fase2_helpers_map.md
- [ ] Atualizar fase2_libs_status.md

## 6. Gate de Conclusão Fase 2A
- [ ] TODAS as duplicações registradas
- [ ] TODAS as funções mapeadas
- [ ] Checklist 100% concluído
""",
    },
    # ============================================================
    # NEW: STATUS DAS LIBS FASE 2 (prefixo médio)
    # ============================================================
    "FASE_2_LIBS_STATUS": {
        "output_path": "docs/fase_2/fase2_libs_status.md",
        "title": "Status das Libs Compartilhadas – Fase 2",
        "description": "Rastreamento de bibliotecas compartilhadas da Fase 2B.",
        "template": """# Status das Libs Compartilhadas – Fase 2
Data de Geração: {timestamp}

Aqui são rastreadas todas as libs que surgirem da consolidação de funções
duplicadas durante a Fase 2B. Nenhuma deve tocar diretamente os scripts
originais até a Fase 3.

## Regras
- Libs devem ser **puras**, sem side-effects
- Libs devem ser **shell-agnósticas** (ou claramente bash/zsh)
- Nenhum script deve ser modificado ainda

## Tabela de Status

| Lib | Status | Origem | Observações |
|-----|--------|---------|-------------|
| deploy_helpers.sh | Planejado | duplicações em deploy/automação | aguardando Fase 2A |
| database_helpers.sh | Planejado | duplicações em init_db/migrate | aguardando Fase 2A |
| nginx_helpers.sh | Planejado | duplicações nos scripts nginx_* | aguardando Fase 2A |
| system_helpers.sh | Planejado | duplicações genéricas | aguardando análise |

## Estrutura Recomendada
- scripts/lib/deploy_helpers.sh
- scripts/lib/database_helpers.sh
- scripts/lib/nginx_helpers.sh
- scripts/lib/system_helpers.sh

## Gatilho de Evolução
Somente após o checklist completo da Fase 2A. Antes disso, nenhuma lib
pode ser criada de fato.
""",
    },
}

# --- Lógica Principal de Execução ---


def generate_docs(doc_names: List[str], force: bool, file_manager: FileManager):
    """Gera os documentos com base nos templates."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for name in doc_names:
        if name not in PHASE2_DOC_TEMPLATES:
            print(f"[ERROR] Template não encontrado: {name}")
            continue

        doc_info = PHASE2_DOC_TEMPLATES[name]

        # Prepara o contexto para o template
        context = {"timestamp": timestamp, **doc_info.get("variables", {})}

        # Substitui variáveis no template (simples substituição de string)
        content = doc_info["template"]
        for key, value in context.items():
            content = content.replace("{" + key + "}", str(value))

        # Escreve o arquivo
        output_path = doc_info["output_path"]

        # Create parent dir if needed
        parent = os.path.dirname(output_path)
        if parent and not os.path.exists(parent):
            ensure_dir(parent)

        file_manager.write_file(output_path, content, force)


def main():
    parser = argparse.ArgumentParser(
        description="Gerador de Documentos de Marco para a Fase 2 do SILA System."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando 'list'
    list_parser = subparsers.add_parser(
        "list", help="Lista os templates de documentos disponíveis."
    )

    # Comando 'generate'
    generate_parser = subparsers.add_parser(
        "generate", help="Gera documentos a partir dos templates."
    )
    generate_group = generate_parser.add_mutually_exclusive_group(required=True)
    generate_group.add_argument(
        "--all", action="store_true", help="Gera todos os documentos."
    )
    generate_group.add_argument(
        "--name",
        type=str,
        help="Gera um documento específico pelo nome (ex: FASE_2_TODO_OFICIAL).",
    )
    generate_parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescreve arquivos existentes sem confirmação.",
    )
    generate_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o que seria feito sem modificar arquivos.",
    )

    args = parser.parse_args()

    if args.command == "list":
        print("\n--- Templates de Documentos da Fase 2 ---")
        for name, info in PHASE2_DOC_TEMPLATES.items():
            print(f"{name}: {info['description']} -> {info['output_path']}")
        print("---------------------------------------")
        return

    if args.command == "generate":
        file_manager = FileManager(dry_run=args.dry_run)
        doc_names_to_generate = []

        if args.all:
            doc_names_to_generate = list(PHASE2_DOC_TEMPLATES.keys())
        elif args.name:
            doc_names_to_generate = [args.name]

        if args.dry_run:
            print(f"[DRY-RUN MODE] Nenhum arquivo será escrito.")
            print(
                f"[DRY-RUN] Documentos a processar: {', '.join(doc_names_to_generate)}"
            )

        generate_docs(doc_names_to_generate, args.force, file_manager)


if __name__ == "__main__":
    main()
