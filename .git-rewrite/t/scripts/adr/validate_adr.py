#!/usr/bin/env python3
"""
Script para validar formato e conteúdo de ADRs

Uso:
    python scripts/adr/validate_adr.py --file docs/adr/0001-architecture-overview.md
    python scripts/adr/validate_adr.py --all  # Valida todos os ADRs
    python scripts/adr/validate_adr.py --directory docs/adr/
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Any
import yaml

# Configurações
ADR_DIR = Path("docs/adr")
REQUIRED_SECTIONS = [
    "Contexto",
    "Decisão",
    "Consequências",
    "Implementação",
    "Alternativas Consideradas",
    "Referências",
    "Histórico de Revisões",
]

REQUIRED_FIELDS = ["Status:", "Data:", "Decisores:", "Revisores:"]

VALID_STATUSES = ["Proposto", "Aceito", "Rejeitado", "Supersedido", "Deprecado"]


class ADRValidator:
    """Validador de ADRs"""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_file(self, filepath: Path) -> Dict[str, Any]:
        """Valida um único arquivo ADR"""
        result = {
            "file": str(filepath),
            "valid": True,
            "errors": [],
            "warnings": [],
            "metadata": {},
        }

        if not filepath.exists():
            result["errors"].append(f"Arquivo não encontrado: {filepath}")
            result["valid"] = False
            return result

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            result["errors"].append(f"Erro ao ler arquivo: {e}")
            result["valid"] = False
            return result

        # Validar nome do arquivo
        filename_errors = self._validate_filename(filepath)
        result["errors"].extend(filename_errors)

        # Validar campos obrigatórios no cabeçalho
        header_errors, metadata = self._validate_header(content)
        result["errors"].extend(header_errors)
        result["metadata"] = metadata

        # Validar seções obrigatórias
        section_errors = self._validate_sections(content)
        result["errors"].extend(section_errors)

        # Validar formato
        format_errors = self._validate_format(content)
        result["errors"].extend(format_errors)

        # Validar links
        link_warnings = self._validate_links(content, filepath)
        result["warnings"].extend(link_warnings)

        # Validar status
        status_warnings = self._validate_status(metadata.get("status", ""))
        result["warnings"].extend(status_warnings)

        result["valid"] = len(result["errors"]) == 0

        return result

    def _validate_filename(self, filepath: Path) -> List[str]:
        """Valida formato do nome do arquivo"""
        errors = []
        filename = filepath.name

        # Verificar padrão XXXX-titulo-descritivo.md
        pattern = r"^\d{4}-.+\.md$"
        if not re.match(pattern, filename):
            errors.append(
                f"Nome de arquivo inválido: {filename}. Use formato: XXXX-titulo-descritivo.md"
            )

        # Verificar se não é arquivo especial
        special_files = ["README.md", "template.md", "index.md"]
        if filename in special_files:
            errors.append(
                f"Arquivo especial não deve ser validado como ADR: {filename}"
            )

        return errors

    def _validate_header(self, content: str) -> tuple[List[str], Dict[str, Any]]:
        """Valida cabeçalho do ADR"""
        errors = []
        metadata = {}

        lines = content.split("\n")

        # Extrair título
        title_match = re.search(r"^# (ADR-\d+: .+)$", content, re.MULTILINE)
        if title_match:
            metadata["title"] = title_match.group(1)
        else:
            errors.append(
                "Título não encontrado ou formato inválido. Use: # ADR-XXXX: Título"
            )

        # Validar campos obrigatórios
        for field in REQUIRED_FIELDS:
            pattern = f"^{field}\\s*(.+)$"
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                value = match.group(1).strip()
                field_name = field.replace(":", "").lower()
                metadata[field_name] = value

                # Validações específicas
                if field == "Status:":
                    if value not in VALID_STATUSES:
                        errors.append(
                            f"Status inválido: {value}. Status válidos: {', '.join(VALID_STATUSES)}"
                        )

                elif field == "Data:":
                    # Validar formato da data
                    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
                    if not re.match(date_pattern, value):
                        errors.append(f"Data inválida: {value}. Use formato YYYY-MM-DD")
            else:
                errors.append(f"Campo obrigatório não encontrado: {field}")

        return errors, metadata

    def _validate_sections(self, content: str) -> List[str]:
        """Valida seções obrigatórias"""
        errors = []

        for section in REQUIRED_SECTIONS:
            # Procurar por cabeçalho da seção
            pattern = f"^## 📋 {section}$"
            if not re.search(pattern, content, re.MULTILINE):
                # Tentar sem emoji
                pattern_alt = f"^## {section}$"
                if not re.search(pattern_alt, content, re.MULTILINE):
                    errors.append(f"Seção obrigatória não encontrada: {section}")

        return errors

    def _validate_format(self, content: str) -> List[str]:
        """Valida formato geral do ADR"""
        errors = []

        # Verificar se usa markdown
        if not content.strip():
            errors.append("Arquivo vazio")
            return errors

        # Verificar se tem linhas em branco excessivas
        consecutive_blank_lines = re.findall(r"\n{4,}", content)
        if consecutive_blank_lines:
            errors.append("Arquivo contém excesso de linhas em branco consecutivas")

        # Verificar se tem seções numeradas corretamente
        if "### " in content and "## " not in content:
            errors.append("Use ## para seções principais e ### para subseções")

        # Verificar se tem lista de consequências
        if "## ✅ Consequências" in content:
            if "### Positivas" not in content or "### Negativas" not in content:
                errors.append(
                    "Seção Consequências deve incluir subseções Positivas e Negativas"
                )

        return errors

    def _validate_links(self, content: str, filepath: Path) -> List[str]:
        """Valida links no ADR"""
        warnings = []

        # Encontrar todos os links markdown
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        matches = re.findall(link_pattern, content)

        for text, url in matches:
            # Verificar links relativos para outros ADRs
            if url.startswith("./") and url.endswith(".md"):
                target_path = (filepath.parent / url).resolve()
                if not target_path.exists():
                    warnings.append(
                        f"Link quebrado: [{text}]({url}) -> {target_path} não encontrado"
                    )

            # Verificar links para arquivos locais
            elif not url.startswith(("http://", "https://", "#", "mailto:")):
                if url.endswith(".md"):
                    target_path = (filepath.parent / url).resolve()
                    if not target_path.exists():
                        warnings.append(f"Link quebrado: [{text}]({url})")

        return warnings

    def _validate_status(self, status: str) -> List[str]:
        """Valida status e gera avisos"""
        warnings = []

        if status == "Proposto":
            warnings.append("ADR ainda está proposto - considere submeter para revisão")
        elif status == "Rejeitado":
            warnings.append(
                "ADR foi rejeitado - considere documentar motivo no histórico"
            )
        elif status == "Supersedido":
            warnings.append(
                "ADR foi superseded - verifique se há referência para o novo ADR"
            )

        return warnings

    def validate_directory(self, directory: Path) -> Dict[str, Any]:
        """Valida todos os ADRs em um diretório"""
        results = {
            "directory": str(directory),
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "files": [],
        }

        if not directory.exists():
            print(f"❌ Diretório não encontrado: {directory}")
            return results

        # Encontrar todos os arquivos ADR
        adr_files = list(directory.glob("*.md"))
        adr_files = [
            f
            for f in adr_files
            if f.name not in ["README.md", "template.md", "index.md"]
        ]

        results["total_files"] = len(adr_files)

        for filepath in adr_files:
            file_result = self.validate_file(filepath)
            results["files"].append(file_result)

            if file_result["valid"]:
                results["valid_files"] += 1
            else:
                results["invalid_files"] += 1

        return results


def print_validation_result(result: Dict[str, Any], verbose: bool = False):
    """Imprime resultado da validação"""
    if result.get("directory"):
        # Resultado de diretório
        print(f"\n📁 Validação do diretório: {result['directory']}")
        print(f"📊 Total de arquivos: {result['total_files']}")
        print(f"✅ Arquivos válidos: {result['valid_files']}")
        print(f"❌ Arquivos inválidos: {result['invalid_files']}")

        if result["invalid_files"] > 0:
            print(f"\n❌ Arquivos com problemas:")
            for file_result in result["files"]:
                if not file_result["valid"]:
                    print(f"   📄 {file_result['file']}")
                    for error in file_result["errors"]:
                        print(f"      ❌ {error}")

        if verbose:
            print(f"\n📋 Detalhes de todos os arquivos:")
            for file_result in result["files"]:
                print(f"\n📄 {file_result['file']}")
                print(f"   ✅ Válido: {file_result['valid']}")
                if file_result["metadata"]:
                    print(f"   📋 Metadados: {file_result['metadata']}")
                if file_result["errors"]:
                    for error in file_result["errors"]:
                        print(f"      ❌ {error}")
                if file_result["warnings"]:
                    for warning in file_result["warnings"]:
                        print(f"      ⚠️  {warning}")

    else:
        # Resultado de arquivo único
        filepath = result["file"]
        if result["valid"]:
            print(f"✅ ADR válido: {filepath}")
        else:
            print(f"❌ ADR inválido: {filepath}")
            for error in result["errors"]:
                print(f"   ❌ {error}")

        if result["warnings"]:
            print(f"⚠️  Avisos para {filepath}:")
            for warning in result["warnings"]:
                print(f"   ⚠️  {warning}")

        if verbose and result["metadata"]:
            print(f"📋 Metadados:")
            for key, value in result["metadata"].items():
                print(f"   {key}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description="Validar formato e conteúdo de ADRs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=Path, help="Arquivo ADR específico para validar")
    group.add_argument(
        "--all",
        action="store_true",
        help="Validar todos os ADRs no diretório docs/adr/",
    )
    group.add_argument(
        "--directory", type=Path, help="Validar todos os ADRs no diretório especificado"
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Mostrar detalhes completos da validação"
    )

    parser.add_argument(
        "--strict", action="store_true", help="Tratar avisos como erros"
    )

    args = parser.parse_args()

    validator = ADRValidator()

    try:
        if args.file:
            result = validator.validate_file(args.file)
            print_validation_result(result, args.verbose)
            return 0 if result["valid"] else 1

        elif args.all:
            result = validator.validate_directory(ADR_DIR)
            print_validation_result(result, args.verbose)
            return 0 if result["invalid_files"] == 0 else 1

        elif args.directory:
            result = validator.validate_directory(args.directory)
            print_validation_result(result, args.verbose)
            return 0 if result["invalid_files"] == 0 else 1

    except Exception as e:
        print(f"❌ Erro durante validação: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
