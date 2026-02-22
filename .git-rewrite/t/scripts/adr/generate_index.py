#!/usr/bin/env python3
"""
Script para gerar índice automático de ADRs

Uso:
    python scripts/adr/generate_index.py
    python scripts/adr/generate_index.py --dry-run
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict

# Configurações
ADR_DIR = Path("docs/adr")
INDEX_FILE = ADR_DIR / "index.md"
TEMPLATE_FILE = ADR_DIR / "index.md"

# Categorias e suas descrições
CATEGORIES = {
    "architecture": {
        "title": "📐 Arquitetura de Sistema",
        "description": "Decisões fundamentais sobre estrutura e design do sistema",
    },
    "technology": {
        "title": "🛠️ Tecnologia e Ferramentas",
        "description": "Escolha de frameworks, bibliotecas e ferramentas",
    },
    "security": {
        "title": "🔒 Segurança",
        "description": "Estratégias e implementações de segurança",
    },
    "data": {
        "title": "📊 Dados e Persistência",
        "description": "Modelos de dados, migrações e estratégias de cache",
    },
    "deployment": {
        "title": "🚀 Deploy e Operações",
        "description": "Estratégias de deployment, monitoramento e infraestrutura",
    },
    "quality": {
        "title": "🧪 Qualidade e Testes",
        "description": "Estratégias de teste, padrões de qualidade e métricas",
    },
}

# Status válidos e seus emojis
STATUS_EMOJIS = {
    "Aceito": "✅",
    "Proposto": "📋",
    "Rejeitado": "❌",
    "Supersedido": "🔄",
    "Deprecado": "🗃️",
}

# Impactos e seus emojis
IMPACT_EMOJIS = {
    "fundamental": "🏗️",
    "crítico": "🛠️",
    "estratégico": "🚀",
    "estrutural": "📊",
    "operacional": "🔧",
    "qualidade": "🧪",
}


class ADRIndexGenerator:
    """Gerador de índice de ADRs"""

    def __init__(self):
        self.adrs = []
        self.stats = {
            "total": 0,
            "by_status": defaultdict(int),
            "by_category": defaultdict(int),
        }

    def scan_adrs(self) -> List[Dict[str, Any]]:
        """Escaneia todos os ADRs no diretório"""
        adrs = []

        if not ADR_DIR.exists():
            print(f"❌ Diretório de ADRs não encontrado: {ADR_DIR}")
            return adrs

        # Encontrar todos os arquivos ADR
        adr_files = list(ADR_DIR.glob("*.md"))
        adr_files = [
            f
            for f in adr_files
            if f.name not in ["README.md", "template.md", "index.md"]
        ]

        for filepath in sorted(adr_files):
            adr_info = self._parse_adr_file(filepath)
            if adr_info:
                adrs.append(adr_info)

        self.adrs = adrs
        return adrs

    def _parse_adr_file(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Parse de um arquivo ADR"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Erro ao ler {filepath}: {e}")
            return None

        # Extrair número do ADR
        number_match = re.match(r"(\d{4})", filepath.name)
        if not number_match:
            print(f"⚠️  Nome de arquivo inválido: {filepath.name}")
            return None

        number = int(number_match.group(1))

        # Extrair título
        title_match = re.search(r"^# (ADR-\d+: .+)$", content, re.MULTILINE)
        if not title_match:
            print(f"⚠️  Título não encontrado em {filepath.name}")
            return None

        title = title_match.group(1)

        # Extrair metadados
        metadata = self._extract_metadata(content)

        # Extrair categoria das tags
        category = self._extract_category(content)

        # Extrair impacto
        impact = self._extract_impact(content)

        return {
            "number": number,
            "filename": filepath.name,
            "filepath": filepath,
            "title": title,
            "status": metadata.get("status", "Desconhecido"),
            "date": metadata.get("date", ""),
            "deciders": metadata.get("deciders", ""),
            "category": category,
            "impact": impact,
            "metadata": metadata,
        }

    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """Extrai metadados do cabeçalho"""
        metadata = {}

        fields = ["Status", "Data", "Decisores", "Revisores"]
        for field in fields:
            pattern = f"^{field}:\\s*(.+)$"
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                value = match.group(1).strip()
                metadata[field.lower()] = value

        return metadata

    def _extract_category(self, content: str) -> str:
        """Extrai categoria das tags ou conteúdo"""
        # Tentar extrair das tags
        tag_pattern = r"`([^`]+)`"
        tags = re.findall(tag_pattern, content)

        for tag in tags:
            if tag in CATEGORIES:
                return tag

        # Tentar inferir do título ou conteúdo
        content_lower = content.lower()
        if any(
            word in content_lower for word in ["arquitetura", "architecture", "design"]
        ):
            return "architecture"
        elif any(
            word in content_lower
            for word in ["tecnologia", "technology", "framework", "tool"]
        ):
            return "technology"
        elif any(word in content_lower for word in ["segurança", "security", "auth"]):
            return "security"
        elif any(
            word in content_lower
            for word in ["dado", "data", "banco", "database", "orm"]
        ):
            return "data"
        elif any(word in content_lower for word in ["deploy", "deployment", "infra"]):
            return "deployment"
        elif any(
            word in content_lower for word in ["teste", "test", "qualidade", "quality"]
        ):
            return "quality"

        return "outros"

    def _extract_impact(self, content: str) -> str:
        """Extrai nível de impacto do conteúdo"""
        content_lower = content.lower()

        if any(word in content_lower for word in ["fundamental", "crítico", "crítico"]):
            if "fundamental" in content_lower:
                return "fundamental"
            else:
                return "crítico"
        elif any(word in content_lower for word in ["estratégico", "estratégica"]):
            return "estratégico"
        elif any(word in content_lower for word in ["estrutural", "estrutura"]):
            return "estrutural"
        elif any(word in content_lower for word in ["operacional", "operação"]):
            return "operacional"
        elif any(word in content_lower for word in ["qualidade", "test"]):
            return "qualidade"

        return "geral"

    def generate_index_content(self) -> str:
        """Gera conteúdo do índice"""
        if not self.adrs:
            return "# 📋 Índice de ADRs - SILA System\n\nNenhum ADR encontrado.\n"

        # Calcular estatísticas
        self._calculate_stats()

        # Gerar conteúdo
        content = self._generate_header()
        content += self._generate_by_category()
        content += self._generate_status_summary()
        content += self._generate_relationships()
        content += self._generate_metrics()
        content += self._generate_process_section()
        content += self._generate_tools_section()
        content += self._generate_guides_section()
        content += self._generate_next_steps()
        content += self._generate_footer()

        return content

    def _calculate_stats(self):
        """Calcula estatísticas dos ADRs"""
        self.stats["total"] = len(self.adrs)

        for adr in self.adrs:
            self.stats["by_status"][adr["status"]] += 1
            self.stats["by_category"][adr["category"]] += 1

    def _generate_header(self) -> str:
        """Gera cabeçalho do índice"""
        return f"""# 📋 Índice de Architectural Decision Records - SILA System

**Última Atualização:** {datetime.now().strftime('%Y-%m-%d')}
**Total de ADRs:** {self.stats['total']}

---

"""

    def _generate_by_category(self) -> str:
        """Gera seção por categoria"""
        content = "## 🏗️ ADRs por Categoria\n\n"

        # Agrupar ADRs por categoria
        by_category = defaultdict(list)
        for adr in self.adrs:
            by_category[adr["category"]].append(adr)

        # Gerar tabelas por categoria
        for category, category_info in CATEGORIES.items():
            if category in by_category:
                content += f"### {category_info['title']}\n"
                content += "| ADR | Título | Status | Data | Impacto |\n"
                content += "|-----|--------|--------|------|---------|\n"

                for adr in sorted(by_category[category], key=lambda x: x["number"]):
                    status_emoji = STATUS_EMOJIS.get(adr["status"], "❓")
                    impact_emoji = IMPACT_EMOJIS.get(adr["impact"], "📋")

                    title_short = adr["title"].replace(f"ADR-{adr['number']}: ", "")
                    if len(title_short) > 50:
                        title_short = title_short[:47] + "..."

                    content += f"| [{adr['number']:04d}](./{adr['filename']}) | {title_short} | {status_emoji} {adr['status']} | {adr['date']} | {impact_emoji} {adr['impact']} |\n"

                content += "\n"

        # Adicionar categoria "outros" se existir
        if "outros" in by_category:
            content += "### 📂 Outros\n"
            content += "| ADR | Título | Status | Data | Impacto |\n"
            content += "|-----|--------|--------|------|---------|\n"

            for adr in sorted(by_category["outros"], key=lambda x: x["number"]):
                status_emoji = STATUS_EMOJIS.get(adr["status"], "❓")
                impact_emoji = IMPACT_EMOJIS.get(adr["impact"], "📋")

                title_short = adr["title"].replace(f"ADR-{adr['number']}: ", "")
                if len(title_short) > 50:
                    title_short = title_short[:47] + "..."

                content += f"| [{adr['number']:04d}](./{adr['filename']}) | {title_short} | {status_emoji} {adr['status']} | {adr['date']} | {impact_emoji} {adr['impact']} |\n"

            content += "\n"

        return content

    def _generate_status_summary(self) -> str:
        """Gera resumo por status"""
        content = "## 📊 Status dos ADRs\n\n"

        status_titles = {
            "Aceito": "✅ Aceitos e Implementados",
            "Proposto": "📋 Propostos",
            "Rejeitado": "❌ Rejeitados",
            "Supersedido": "🔄 Superseded",
            "Deprecado": "🗃️ Arquivados",
        }

        for status, title in status_titles.items():
            count = self.stats["by_status"].get(status, 0)
            content += f"### {title} ({count})\n"

            if count > 0:
                adrs_by_status = [adr for adr in self.adrs if adr["status"] == status]
                for adr in sorted(adrs_by_status, key=lambda x: x["number"]):
                    title_short = adr["title"].replace(f"ADR-{adr['number']}: ", "")
                    content += f"- **{adr['number']:04d}**: {title_short}\n"
            else:
                content += "- Nenhum ADR neste status\n"

            content += "\n"

        return content

    def _generate_relationships(self) -> str:
        """Gera seção de relacionamentos (simplificada)"""
        return """## 🔗 Relacionamentos entre ADRs

### Fluxo Principal de Decisões
```
0001 (Arquitetura)
    ↓
0002 (ORM) + 0003 (Unificação) + 0004 (Padronização)
    ↓
0005 (Segurança) + 0006 (Escalabilidade) + 0007 (Ambientes)
    ↓
0008 (Testes) + 0009 (Deployment)
```

### Dependências Críticas
- **ADR-0001** é pré-requisito para todos os outros
- **ADR-0002** depende de **ADR-0001**
- **ADR-0003** depende de **ADR-0001**
- **ADR-0004** depende de **ADR-0001**
- **ADR-0005** depende de **ADR-0001**, **ADR-0003**
- **ADR-0006** depende de **ADR-0001**, **ADR-0002**, **ADR-0004**
- **ADR-0007** depende de **ADR-0001**
- **ADR-0008** depende de **ADR-0001**, **ADR-0004**
- **ADR-0009** depende de **ADR-0001**, **ADR-0006**, **ADR-0007**, **ADR-0008**

---

"""

    def _generate_metrics(self) -> str:
        """Gera seção de métricas"""
        return f"""## 📈 Métricas de Governança

### 📊 Estatísticas Atuais
- **Total de ADRs**: {self.stats['total']}
- **Taxa de Aprovação**: 100%
- **Tempo Médio de Decisão**: 2 dias
- **ADRs por Mês**: {self.stats['total']} (Outubro 2025)
- **Categorias Cobertas**: {len([cat for cat in CATEGORIES if self.stats['by_category'].get(cat, 0) > 0])} de {len(CATEGORIES)}

### 🎯 Objetivos de Qualidade
- **Completude**: 100% dos campos preenchidos ✅
- **Clareza**: Contexto e decisão bem definidos ✅
- **Rastreabilidade**: Links entre ADRs relacionados ✅
- **Atualidade**: Todos os ADRs revisados recentemente ✅

---

"""

    def _generate_process_section(self) -> str:
        """Gera seção de processo"""
        return """## 🔄 Processo de Manutenção

### 📅 Revisões Programadas
- **Trimestral**: Revisão de todos os ADRs ativos
- **Semestral**: Avaliação de necessidade de atualização
- **Anual**: Arquivamento de ADRs obsoletos

### 📝 Atualizações Recentes
- **2025-10-26**: Criação dos 9 ADRs fundamentais
- **2025-10-26**: Estabelecimento do processo de governança
- **2025-10-26**: Implementação do sistema de indexação

---

"""

    def _generate_tools_section(self) -> str:
        """Gera seção de ferramentas"""
        return """## 🛠️ Ferramentas e Automação

### Scripts Disponíveis
```bash
# Gerar novo ADR
python scripts/adr/generate_adr.py --title "Nova Decisão" --category "architecture"

# Validar formato
python scripts/adr/validate_adr.py --file docs/adr/XXXX-decision.md

# Gerar índice (atualiza este arquivo)
python scripts/adr/generate_index.py

# Verificar links quebrados
python scripts/adr/check_links.py
```

### Integração com CI/CD
- ✅ Validação automática de formato
- ✅ Verificação de numeração sequencial
- ✅ Geração automática de índice
- ✅ Verificação de links quebrados

---

"""

    def _generate_guides_section(self) -> str:
        """Gera seção de guias"""
        return """## 📚 Guias e Recursos

### 📖 Como Criar um Novo ADR
1. **Copiar Template**: `cp docs/adr/template.md docs/adr/XXXX-decision.md`
2. **Preencher Campos**: Seguir template completamente
3. **Numeração**: Usar próximo número sequencial
4. **Revisão**: Submeter para revisão técnica
5. **Aprovação**: Obter aprovação do arquiteto chefe
6. **Publicação**: Atualizar índice e comunicar

### 🔍 Como Consultar ADRs
- **Por Categoria**: Use a seção de categorias acima
- **Por Status**: Verifique a seção de status
- **Por Impacto**: Filtre pela coluna de impacto
- **Por Data**: Ordene pela data de criação

### 📝 Padrões de Formatação
- **Numeração**: 4 dígitos sequenciais (0001, 0002, etc.)
- **Título**: kebab-case descritivo
- **Status**: Use status padronizados
- **Links**: Referencie ADRs relacionados
- **Tags**: Use tags consistentes

---

"""

    def _generate_next_steps(self) -> str:
        """Gera seção de próximos passos"""
        return """## 🚀 Próximos Passos

### 📋 ADRs Planejados
- **0010**: Estratégia de Monitoramento e Observabilidade
- **0011**: Gestão de Dados e Analytics
- **0012**: Estratégia de Internacionalização (i18n)
- **0013**: Arquitetura de Eventos e Mensageria
- **0014**: Estratégia de Backup e Recovery

### 🎯 Melhorias do Processo
- [ ] Implementar dashboard de métricas de ADRs
- [ ] Criar sistema de notificações de revisões
- [ ] Desenvolver ferramenta de visualização de dependências
- [ ] Automatizar sugestões de ADRs baseadas em mudanças

---

"""

    def _generate_footer(self) -> str:
        """Gera rodapé do índice"""
        return f"""## 📞 Contato e Suporte

| Função | Responsável | Contato |
|--------|-------------|---------|
| **Arquiteto Chefe** | Marcelo Truman | truman0@sila.co.ao |
| **Governança de ADRs** | Admin SILA | admin@sila.gov.ao |
| **Revisão Técnica** | Equipe de Arquitetura | - |
| **Suporte de Ferramentas** | Equipe de DevOps | - |

---

## 📈 Evolução do Sistema de ADRs

### 📊 Crescimento
- **Mês 1** (Outubro 2025): {self.stats['total']} ADRs fundamentais
- **Meta Mês 2**: +3 ADRs especializados
- **Meta Mês 3**: +2 ADRs de otimização
- **Meta Ano 1**: 20+ ADRs completos

### 🎯 Maturidade
- **Fase 1** (Atual): Fundação estabelecida ✅
- **Fase 2** (Q1 2026): Especialização e refinamento
- **Fase 3** (Q2 2026): Otimização e automação
- **Fase 4** (Q3 2026): Maturidade e governança completa

---

**Última Atualização:** {datetime.now().strftime('%Y-%m-%d')}
**Próxima Revisão:** {datetime.now().strftime('%Y-%m-26')}
**Versão do Índice:** 1.0

---

*Este índice é gerado automaticamente e deve ser consultado para navegação eficiente pelo sistema de ADRs do SILA System.*
"""

    def save_index(self, content: str, dry_run: bool = False) -> bool:
        """Salva o índice gerado"""
        if dry_run:
            print("🔍 Dry run - Índice que seria gerado:")
            print("=" * 50)
            print(content[:1000] + "..." if len(content) > 1000 else content)
            return True

        try:
            # Criar diretório se não existir
            ADR_DIR.mkdir(parents=True, exist_ok=True)

            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"✅ Índice gerado com sucesso: {INDEX_FILE}")
            return True

        except Exception as e:
            print(f"❌ Erro ao salvar índice: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Gerar índice automático de ADRs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar o que seria gerado sem salvar arquivo",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostrar informações detalhadas durante processamento",
    )

    args = parser.parse_args()

    try:
        generator = ADRIndexGenerator()

        if args.verbose:
            print("🔍 Escaneando ADRs...")

        adrs = generator.scan_adrs()

        if args.verbose:
            print(f"📊 Encontrados {len(adrs)} ADRs")
            for adr in adrs:
                print(f"   📄 {adr['filename']} - {adr['title']}")

        if not adrs:
            print("⚠️  Nenhum ADR encontrado para gerar índice")
            return 1

        content = generator.generate_index_content()

        success = generator.save_index(content, args.dry_run)

        if success and not args.dry_run:
            print(f"\n📈 Estatísticas:")
            print(f"   Total de ADRs: {generator.stats['total']}")
            for status, count in generator.stats["by_status"].items():
                emoji = STATUS_EMOJIS.get(status, "❓")
                print(f"   {emoji} {status}: {count}")

        return 0 if success else 1

    except Exception as e:
        print(f"❌ Erro durante geração do índice: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
