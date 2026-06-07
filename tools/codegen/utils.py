#!/usr/bin/env python3
"""
Shared utilities for the SILA code generation system.

This module provides common functionality used across all scaffolding scripts,
including file operations, template management, naming conventions, and validation.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any


class CodeGenError(Exception):
    """Custom exception for code generation errors."""

    pass


class TemplateManager:
    """Manages code templates and their formatting."""

    def __init__(self, template_dir: Path | None = None):
        self.template_dir = template_dir or Path(__file__).parent / "templates"

    def format_template(self, template: str, variables: dict[str, Any]) -> str:
        """Format a template string with given variables."""
        try:
            return template.format(**variables)
        except KeyError as e:
            raise CodeGenError(f"Missing template variable: {e}")
        except Exception as e:
            raise CodeGenError(f"Template formatting error: {e}")


class NamingConvention:
    """Handles naming conventions for different parts of the system."""

    @staticmethod
    def to_snake_case(text: str) -> str:
        """Convert text to snake_case."""
        # Insert underscores before uppercase letters and convert to lowercase
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @staticmethod
    def to_kebab_case(text: str) -> str:
        """Convert text to kebab-case."""
        return NamingConvention.to_snake_case(text).replace("_", "-")

    @staticmethod
    def to_pascal_case(text: str) -> str:
        """Convert text to PascalCase."""
        snake = NamingConvention.to_snake_case(text)
        return "".join(word.capitalize() for word in snake.split("_"))

    @staticmethod
    def to_camel_case(text: str) -> str:
        """Convert text to camelCase."""
        pascal = NamingConvention.to_pascal_case(text)
        return pascal[0].lower() + pascal[1:] if pascal else ""

    @staticmethod
    def generate_names(service_key: str, module_name: str = "") -> dict[str, str]:
        """Generate all naming variations from a service key."""
        service_slug = NamingConvention.to_snake_case(service_key)
        api_slug = NamingConvention.to_kebab_case(service_key)
        table_name = f"{module_name}_{service_slug}" if module_name else service_slug
        model_name = NamingConvention.to_pascal_case(service_key)
        display_name = " ".join(
            word.capitalize() for word in service_slug.replace("_", " ").split()
        )
        display_name_lower = display_name.lower()

        return {
            "service_key": service_key,
            "service_slug": service_slug,
            "api_slug": api_slug,
            "table_name": table_name,
            "model_name": model_name,
            "display_name": display_name,
            "display_name_lower": display_name_lower,
            "module_name": module_name,
        }


class FileManager:
    """Handles file and directory operations."""

    @staticmethod
    def create_directory(path: Path, description: str = "") -> None:
        """Create directory with logging."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            if description:
                print(f"✅ Created {description}: {path}")
        except Exception as e:
            raise CodeGenError(f"Failed to create directory {path}: {e}")

    @staticmethod
    def create_file(path: Path, content: str, description: str = "") -> None:
        """Create file with content and logging."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")
            if description:
                print(f"✅ Created {description}: {path}")
        except Exception as e:
            raise CodeGenError(f"Failed to create file {path}: {e}")

    @staticmethod
    def read_file(path: Path) -> str:
        """Read file content."""
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise CodeGenError(f"Failed to read file {path}: {e}")

    @staticmethod
    def update_file_section(
        file_path: Path, section_start: str, section_end: str, new_content: str
    ) -> None:
        """Update a specific section in a file."""
        content = FileManager.read_file(file_path)

        # Find section boundaries
        start_idx = content.find(section_start)
        if start_idx == -1:
            raise CodeGenError(f"Section start '{section_start}' not found in {file_path}")

        end_idx = content.find(section_end, start_idx)
        if end_idx == -1:
            raise CodeGenError(f"Section end '{section_end}' not found in {file_path}")

        # Replace section
        new_content = (
            content[:start_idx]
            + section_start
            + new_content
            + section_end
            + content[end_idx + len(section_end) :]
        )

        FileManager.create_file(file_path, new_content)


class Validation:
    """Handles validation of inputs and system state."""

    @staticmethod
    def validate_module_exists(module_path: Path) -> None:
        """Validate that a module exists."""
        if not module_path.exists():
            raise CodeGenError(f"Module '{module_path.name}' not found at {module_path}")

        if not module_path.is_dir():
            raise CodeGenError(f"Path {module_path} is not a directory")

    @staticmethod
    def validate_service_not_exists(service_path: Path) -> None:
        """Validate that a service doesn't already exist."""
        if service_path.exists():
            raise CodeGenError(f"Service already exists at {service_path}")

    @staticmethod
    def validate_service_key(service_key: str) -> None:
        """Validate service key format."""
        if not re.match(r"^[A-Za-z][A-Za-z0-9]*$", service_key):
            raise CodeGenError(
                "Service key must start with a letter and contain only letters and numbers"
            )

        if len(service_key) < 2:
            raise CodeGenError("Service key must be at least 2 characters long")

    @staticmethod
    def validate_names(name_pt: str, name_en: str) -> None:
        """Validate Portuguese and English names."""
        if not name_pt or not name_pt.strip():
            raise CodeGenError("Portuguese name cannot be empty")

        if not name_en or not name_en.strip():
            raise CodeGenError("English name cannot be empty")

        if len(name_pt) > 200:
            raise CodeGenError("Portuguese name too long (max 200 characters)")

        if len(name_en) > 200:
            raise CodeGenError("English name too long (max 200 characters)")


class ServiceRegistry:
    """Handles service registration in the system."""

    @staticmethod
    def register_in_services(module_path: Path, names: dict[str, str], service_type: str) -> None:
        """Register service in the module's services.py file."""
        services_path = module_path / "services.py"

        if not services_path.exists():
            return  # Skip if services.py doesn't exist

        # Read current content
        content = FileManager.read_file(services_path)

        # Check if register_service import exists
        import_statement = (
            "from apps.backend.app.modules.service_hub.services import register_service"
        )
        if import_statement not in content:
            # Add import after last import
            lines = content.split("\n")
            last_import_idx = -1
            for i, line in enumerate(lines):
                if line.startswith(("from ", "import ")):
                    last_import_idx = i

            if last_import_idx >= 0:
                lines.insert(last_import_idx + 1, import_statement)
                content = "\n".join(lines)

        # Add service registration template
        template = f'''

@register_service(
    slug="{names["service_slug"]}",
    nome="{names["display_name"]}",
    nome_en="{names["display_name"]}",
    descricao="Serviço para {names["display_name_lower"]}",
    descricao_en="Service for {names["display_name_lower"]}",
    departamento="{names["module_name"]}",
    categoria="{names["module_name"]}",
    tipo_servico="{service_type}"
)
def {names["service_slug"]}_handler(data):
    """
    Handler for {names["display_name"]} / Manipulador para {names["display_name"]}
    """
    return {{"status": "success", "service": "{names["service_slug"]}"}}'''

        content += template

        FileManager.create_file(services_path, content, "service registration")

    @staticmethod
    def register_in_init(module_path: Path, names: dict[str, str]) -> None:
        """Register service in the module's __init__.py file."""
        init_path = module_path / "__init__.py"

        if not init_path.exists():
            return  # Skip if __init__.py doesn't exist

        # Add service comment
        content = FileManager.read_file(init_path)
        content += f"\n# Serviço: {names['display_name']}\n"
        FileManager.create_file(init_path, content, "service comment")

        # Add route registration if router exists
        if "router = APIRouter()" in content:
            # Add route import and include
            route_import = f"from apps.backend.app.modules.{names['module_name']}.routes.{names['service_slug']} import router as {names['service_slug']}_router\n"
            route_include = f"router.include_router({names['service_slug']}_router)\n"

            lines = content.split("\n")
            router_idx = -1
            for i, line in enumerate(lines):
                if "router = APIRouter()" in line:
                    router_idx = i
                    break

            if router_idx >= 0:
                lines.insert(router_idx, route_import)
                lines.insert(router_idx + 2, route_include)
                content = "\n".join(lines)
                FileManager.create_file(init_path, content, "route registration")


class CSVProcessor:
    """Handles CSV file processing for batch operations."""

    @staticmethod
    def read_services_csv(csv_path: Path) -> list[dict[str, str]]:
        """Read services from CSV file."""
        services = []

        try:
            with open(csv_path, encoding="utf-8") as f:
                # Try to detect if there's a header
                first_line = f.readline().strip()

                if "module" in first_line.lower() or "service" in first_line.lower():
                    # Has header, use csv.DictReader
                    f.seek(0)
                    import csv

                    reader = csv.DictReader(f)
                    services = [row for row in reader if not row.get("module", "").startswith("#")]
                else:
                    # No header, assume format: module,service_key,name_pt,name_en,service_type
                    f.seek(0)
                    import csv

                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 4 and not row[0].startswith("#"):
                            services.append(
                                {
                                    "module": row[0].strip(),
                                    "service_key": row[1].strip(),
                                    "service_name_pt": row[2].strip(),
                                    "service_name_en": row[3].strip(),
                                    "service_type": (row[4].strip() if len(row) > 4 else "citizen"),
                                }
                            )

        except Exception as e:
            raise CodeGenError(f"Failed to read CSV file {csv_path}: {e}")

        return services

    @staticmethod
    def create_sample_csv(output_path: Path) -> None:
        """Create a sample CSV file with service definitions."""
        sample_data = [
            [
                "module",
                "service_key",
                "service_name_pt",
                "service_name_en",
                "service_type",
            ],
            [
                "health",
                "AgendamentoConsulta",
                "Agendamento de Consulta",
                "Medical Appointment",
                "citizen",
            ],
            [
                "health",
                "SolicitacaoExame",
                "Solicitação de Exame",
                "Lab Test Request",
                "citizen",
            ],
            [
                "citizenship",
                "EmissaoBI",
                "Emissão de BI",
                "ID Card Issuance",
                "citizen",
            ],
            [
                "education",
                "MatriculaEscolar",
                "Matrícula Escolar",
                "School Enrollment",
                "citizen",
            ],
            [
                "commercial",
                "AberturaProcesso",
                "Abertura de Processo",
                "Process Opening",
                "internal",
            ],
            [
                "urbanism",
                "LicencaConstrucao",
                "Licença de Construção",
                "Building Permit",
                "internal",
            ],
        ]

        try:
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                import csv

                writer = csv.writer(f)
                writer.writerows(sample_data)
            print(f"✅ Sample CSV created: {output_path}")
        except Exception as e:
            raise CodeGenError(f"Failed to create sample CSV: {e}")


class ProgressTracker:
    """Tracks progress during batch operations."""

    def __init__(self, total: int):
        self.total = total
        self.current = 0
        self.success = 0
        self.failed = 0
        self.failed_services: list[tuple[str, str, str]] = []

    def start_service(self, module: str, service_key: str, name: str) -> None:
        """Start processing a service."""
        self.current += 1
        print(f"[{self.current}/{self.total}] Generating {name} in module {module}...")

    def success_service(self, module: str, service_key: str, name: str) -> None:
        """Mark service as successfully generated."""
        self.success += 1
        print(f"✅ {name} generated successfully!")

    def fail_service(self, module: str, service_key: str, name: str, error: str) -> None:
        """Mark service as failed."""
        self.failed += 1
        self.failed_services.append((module, service_key, name))
        print(f"❌ Failed to generate {name}: {error}")

    def print_summary(self) -> None:
        """Print operation summary."""
        print("\n📊 Batch Generation Summary:")
        print(f"   ✅ Successful: {self.success}")
        print(f"   ❌ Failed: {self.failed}")

        if self.failed_services:
            print("\n❌ Failed Services:")
            for module, service_key, name in self.failed_services:
                print(f"   - {module}/{service_key}: {name}")


def get_base_paths() -> dict[str, Path]:
    """Get base paths for the project."""
    script_dir = Path(__file__).resolve().parent.parent.parent
    backend_dir = script_dir / "backend"
    modules_dir = backend_dir / "modules"

    return {"script": script_dir, "backend": backend_dir, "modules": modules_dir}


def get_timestamp() -> str:
    """Get current timestamp for logging."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def validate_environment() -> None:
    """Validate that we're in the correct environment."""
    paths = get_base_paths()

    if not paths["modules"].exists():
        raise CodeGenError(f"Modules directory not found: {paths['modules']}")

    # Check if we're in a backend directory with modules
    if not any(paths["modules"].iterdir()):
        print("⚠️  Warning: Modules directory exists but appears empty")


# Export main classes for easy importing
__all__ = [
    "CodeGenError",
    "TemplateManager",
    "NamingConvention",
    "FileManager",
    "Validation",
    "ServiceRegistry",
    "CSVProcessor",
    "ProgressTracker",
    "get_base_paths",
    "get_timestamp",
    "validate_environment",
]
