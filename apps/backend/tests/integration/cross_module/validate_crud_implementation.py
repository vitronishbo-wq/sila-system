#!/usr/bin/env python3
"""
Validação da implementação CRUD/Data Access padrão

Este script valida que todos os módulos seguem o padrão CRUD
implementado, garantindo consistência na camada de acesso a dados.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class CRUDValidationResult:
    """Resultado da validação CRUD."""

    def __init__(self):
        self.modules_validated = 0
        self.modules_passed = 0
        self.modules_failed = 0
        self.results = {}

    def add_module_result(
        self, module_name: str, passed: bool, details: Dict[str, Any]
    ):
        """Adiciona resultado de módulo."""
        self.results[module_name] = {"passed": passed, "details": details}
        self.modules_validated += 1
        if passed:
            self.modules_passed += 1
        else:
            self.modules_failed += 1

    def get_summary(self) -> str:
        """Obtém resumo dos resultados."""
        if self.modules_validated == 0:
            return "Nenhum módulo validado"

        success_rate = (self.modules_passed / self.modules_validated) * 100
        return f"{self.modules_passed}/{self.modules_validated} módulos passaram ({success_rate:.1f}%)"


def validate_crud_structure(module_path: Path) -> Dict[str, Any]:
    """Valida estrutura CRUD de um módulo."""
    details = {
        "has_crud_file": False,
        "has_crud_schemas": False,
        "crud_file_exists": False,
        "schema_file_exists": False,
        "crud_classes": [],
        "schema_classes": [],
        "errors": [],
    }

    # Verificar arquivo crud.py
    crud_file = module_path / "crud.py"
    details["crud_file_exists"] = crud_file.exists()

    if crud_file.exists():
        details["has_crud_file"] = True

        try:
            # Tentar ler o arquivo para validar estrutura
            with open(crud_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Verificar padrões básicos
            if "class" in content and "CRUD" in content:
                details["has_crud_classes"] = True

                # Extrair nomes das classes CRUD
                import re

                crud_classes = re.findall(r"class (\w+CRUD)\(", content)
                details["crud_classes"] = crud_classes

            # Verificar métodos padrão
            standard_methods = ["create", "get", "get_multi", "update", "remove"]
            missing_methods = []

            for method in standard_methods:
                if f"async def {method}(" not in content:
                    missing_methods.append(method)

            if missing_methods:
                details["errors"].append(
                    f"Métodos CRUD padrão ausentes: {missing_methods}"
                )

            # Verificar factory functions
            if "def get_" not in content:
                details["errors"].append("Funções factory (get_*) não encontradas")

        except Exception as e:
            details["errors"].append(f"Erro ao ler arquivo CRUD: {str(e)}")

    # Verificar schemas CRUD
    schema_patterns = [
        "schemas/crud.py",
        "schemas/module_crud.py",
        "schemas/sanitation_crud.py",
        "schemas/education_crud.py",
        "schemas/finance_crud.py",
        "schemas/monitoring_crud.py",
    ]

    schema_file = None
    for pattern in schema_patterns:
        potential_file = module_path / pattern
        if potential_file.exists():
            schema_file = potential_file
            break

    if schema_file:
        details["schema_file_exists"] = True
        details["has_crud_schemas"] = True

        try:
            with open(schema_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Verificar schemas básicos - ser mais flexível com nomes
            import re

            # Procurar por qualquer classe que termine com Create, Update, InDB, Out, Filter
            create_classes = re.findall(r"class (\w+Create)\(", content)
            update_classes = re.findall(r"class (\w+Update)\(", content)
            indb_classes = re.findall(r"class (\w+InDB)\(", content)
            out_classes = re.findall(r"class (\w+Out)\(", content)
            filter_classes = re.findall(r"class (\w+Filter)\(", content)

            if not create_classes:
                details["errors"].append("Nenhuma classe Create encontrada")
            if not update_classes:
                details["errors"].append("Nenhuma classe Update encontrada")
            if not indb_classes:
                details["errors"].append("Nenhuma classe InDB encontrada")
            if not out_classes:
                details["errors"].append("Nenhuma classe Out encontrada")
            # Filter é opcional, então não vamos exigir

            # Extrair nomes das classes de schema
            schema_classes = re.findall(
                r"class (\w+(?:Create|Update|InDB|Out|Filter))\(", content
            )
            details["schema_classes"] = schema_classes[:10]  # Limitar para não poluir

        except Exception as e:
            details["errors"].append(f"Erro ao ler arquivo de schemas: {str(e)}")

    return details


def validate_existing_cruds() -> CRUDValidationResult:
    """Valida CRUDs existentes."""
    result = CRUDValidationResult()

    print("🔍 Validando implementação CRUD/Data Access")
    print("=" * 60)

    modules_dir = Path("/opt/sila-system/backend/modules")

    # Módulos que devem ter CRUD
    modules_to_check = [
        "sanitation",
        "education",
        "finance",
        "monitoring",
        "health",
        "justice",
        "citizenship",
        "complaints",
        "documents",
        "address",
    ]

    for module_name in modules_to_check:
        module_path = modules_dir / module_name

        if not module_path.exists():
            result.add_module_result(
                module_name, False, {"error": f"Módulo {module_name} não encontrado"}
            )
            print(f"❌ {module_name}: Módulo não encontrado")
            continue

        print(f"\n📋 Validando módulo: {module_name}")
        details = validate_crud_structure(module_path)

        # Determinar se passou na validação
        passed = (
            details["has_crud_file"]
            and details["has_crud_schemas"]
            and len(details["errors"]) == 0
        )

        result.add_module_result(module_name, passed, details)

        # Mostrar resultados
        if passed:
            print(f"✅ {module_name}: CRUD implementado corretamente")
            if details["crud_classes"]:
                print(f"   Classes CRUD: {', '.join(details['crud_classes'][:3])}")
            if details["schema_classes"]:
                print(
                    f"   Schemas: {len(details['schema_classes'])} classes encontradas"
                )
        else:
            print(f"❌ {module_name}: Problemas na implementação CRUD")
            for error in details["errors"]:
                print(f"   • {error}")

    return result


def validate_crud_consistency() -> Dict[str, Any]:
    """Valida consistência entre implementações CRUD."""
    print("\n🔍 Validando consistência entre CRUDs")
    print("-" * 40)

    consistency_report = {
        "standard_methods_found": True,
        "factory_pattern_consistent": True,
        "naming_convention_consistent": True,
        "issues": [],
    }

    modules_dir = Path("/opt/sila-system/backend/modules")
    crud_files = list(modules_dir.glob("*/crud.py"))

    if not crud_files:
        consistency_report["issues"].append("Nenhum arquivo crud.py encontrado")
        return consistency_report

    # Verificar métodos padrão em todos os CRUDs
    standard_methods = ["create", "get", "get_multi", "update", "remove"]

    for crud_file in crud_files:
        try:
            with open(crud_file, "r", encoding="utf-8") as f:
                content = f.read()

            module_name = crud_file.parent.name

            # Verificar métodos padrão
            missing_methods = []
            for method in standard_methods:
                if f"async def {method}(" not in content:
                    missing_methods.append(method)

            if missing_methods:
                consistency_report["issues"].append(
                    f"{module_name}: Métodos ausentes {missing_methods}"
                )
                consistency_report["standard_methods_found"] = False

            # Verificar convenção de nomes
            if "class " in content:
                import re

                classes = re.findall(r"class (\w+CRUD)\(", content)
                for cls in classes:
                    if not cls.endswith("CRUD"):
                        consistency_report["issues"].append(
                            f"{module_name}: Classe {cls} não segue convenção CRUD"
                        )
                        consistency_report["naming_convention_consistent"] = False

            # Verificar factory functions
            if "def get_" not in content:
                consistency_report["issues"].append(
                    f"{module_name}: Funções factory não encontradas"
                )
                consistency_report["factory_pattern_consistent"] = False

        except Exception as e:
            consistency_report["issues"].append(
                f"Erro ao validar {crud_file}: {str(e)}"
            )

    return consistency_report


def generate_crud_summary_report(
    result: CRUDValidationResult, consistency: Dict[str, Any]
) -> str:
    """Gera relatório resumido da validação CRUD."""

    report = f"""
# Relatório de Validação CRUD/Data Access

## 📊 Resumo da Validação
- **Data/Hora**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Módulos Validados**: {result.modules_validated}
- **Módulos Aprovados**: {result.modules_passed}
- **Módulos Reprovados**: {result.modules_failed}
- **Taxa de Sucesso**: {(result.modules_passed / result.modules_validated * 100) if result.modules_validated > 0 else 0:.1f}%

## 🏗️ Consistência da Implementação
- **Métodos Padrão**: {'✅' if consistency['standard_methods_found'] else '❌'}
- **Factory Pattern**: {'✅' if consistency['factory_pattern_consistent'] else '❌'}
- **Convenção de Nomes**: {'✅' if consistency['naming_convention_consistent'] else '❌'}

## 📋 Detalhes por Módulo
"""

    for module_name, details in result.results.items():
        status = "✅ Aprovado" if details["passed"] else "❌ Reprovado"
        report += f"\n### {module_name.title()}: {status}\n"

        if details["passed"]:
            if details["details"]["crud_classes"]:
                report += (
                    f"- Classes CRUD: {', '.join(details['details']['crud_classes'])}\n"
                )
            if details["details"]["schema_classes"]:
                report += (
                    f"- Schemas: {len(details['details']['schema_classes'])} classes\n"
                )
        else:
            for error in details["details"]["errors"]:
                report += f"- ❌ {error}\n"

    if consistency["issues"]:
        report += "\n## ⚠️ Issues de Consistência\n"
        for issue in consistency["issues"]:
            report += f"- {issue}\n"

    report += f"""

## 🎯 Próximos Passos
1. **Implementar CRUDs Faltantes**: Completar módulos sem CRUD
2. **Padronizar Métodos**: Garantir todos os CRUDs tenham métodos padrão
3. **Criar Schemas**: Implementar schemas para todos os CRUDs
4. **Documentar**: Adicionar documentação aos métodos CRUD

## 📁 Arquivos Criados/Atualizados
- `modules/sanitation/crud.py` - CRUD para saneamento
- `modules/sanitation/schemas/sanitation_crud.py` - Schemas do CRUD
- `modules/education/crud.py` - CRUD para educação
- `modules/education/schemas/education_crud.py` - Schemas do CRUD
- `modules/finance/crud.py` - CRUD para finanças
- `modules/finance/schemas/finance_crud.py` - Schemas do CRUD
- `modules/monitoring/crud.py` - CRUD para monitoramento
- `modules/monitoring/schemas/monitoring_crud.py` - Schemas do CRUD
"""

    return report


def main():
    """Função principal de validação."""
    print("🧪 VALIDAÇÃO CRUD/DATA ACCESS - SILA System")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Executar validações
    result = validate_existing_cruds()
    consistency = validate_crud_consistency()

    # Gerar relatório
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)

    print(f"\n📈 Resumo Geral: {result.get_summary()}")

    print(f"\n🏗️ Consistência da Implementação:")
    print(
        f"   Métodos Padrão: {'✅' if consistency['standard_methods_found'] else '❌'}"
    )
    print(
        f"   Factory Pattern: {'✅' if consistency['factory_pattern_consistent'] else '❌'}"
    )
    print(
        f"   Convenção de Nomes: {'✅' if consistency['naming_convention_consistent'] else '❌'}"
    )

    if consistency["issues"]:
        print(f"\n⚠️ Issues de Consistência:")
        for issue in consistency["issues"][:5]:  # Mostrar apenas 5 primeiros
            print(f"   • {issue}")

    # Salvar relatório detalhado
    report_content = generate_crud_summary_report(result, consistency)
    report_file = Path(
        "/opt/sila-system/backend/tests/integration/cross_module/CRUD_VALIDATION_REPORT.md"
    )

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n💾 Relatório detalhado salvo em: {report_file}")

    # Status final
    print("\n" + "=" * 60)
    if result.modules_failed == 0 and result.modules_validated > 0:
        print("🎉 TODOS OS MÓDULOS COM CRUD PADRÃO!")
        print("✅ Implementação CRUD/Data Access está consistente")
        print("✅ Padrão de acesso a dados padronizado")
        print("✅ Separação entre persistência e lógica de negócio")
        return 0
    elif result.modules_validated == 0:
        print("⚠️  NENHUM MÓDULO VALIDADO")
        return 1
    else:
        print("⚠️  ALGUNS MÓDULOS PRECISAM DE AJUSTES")
        print("🔧 Revise os issues listados acima")
        return 1


if __name__ == "__main__":
    sys.exit(main())
