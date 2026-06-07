# \!/usr/bin/env python3
"""
Universal SILA Module and Service Generator

This script unifies all scaffolding functionality into a single, robust tool
that can generate both complete modules and individual services with support
for batch operations, multiple templates, and comprehensive validation.

Usage:
    python generate_module.py module <module_name> [options]
    python generate_module.py service <module> <service_key> <name_pt> <name_en> [options]
    python generate_module.py batch --csv <csv_file> [options]
    python generate_module.py batch --default [options]

Features:
- Generate complete FastAPI modules with all necessary files
- Generate individual services within existing modules
- Batch generation from CSV files or predefined lists
- Support for citizen and internal service types
- Bilingual support (Portuguese/English)
- Template-based code generation
- Comprehensive validation and error handling
- Automatic service registration and routing
"""

import argparse
import sys
from pathlib import Path
from typing import Any

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    CodeGenError,
    CSVProcessor,
    FileManager,
    NamingConvention,
    ProgressTracker,
    ServiceRegistry,
    TemplateManager,
    Validation,
    get_base_paths,
    validate_environment,
)

from templates import MODULE_TEMPLATES, SERVICE_TEMPLATES


def generate_module(name: str, title: str, description: str, options: dict[str, Any]) -> None:
    """Generate a complete FastAPI module."""
    print(f"🔧 Generating module: {name}")

    paths = get_base_paths()
    module_dir = paths["modules"] / name.lower()

    # Validate module doesn't exist
    if module_dir.exists():
        raise CodeGenError(f"Module '{name}' already exists at {module_dir}")

    # Generate names
    names = {
        "module_name": name,
        "module_title": title,
        "module_description": description,
        "module_slug": name.lower(),
    }

    template_manager = TemplateManager()

    # Create directory structure
    FileManager.create_directory(module_dir, "module directory")

    subdirs = ["models", "schemas", "services", "routes", "tests"]
    for subdir in subdirs:
        if options.get(f"include_{subdir}", True):
            FileManager.create_directory(module_dir / subdir, f"{subdir} directory")

    # Generate files
    if options.get("include_init", True):
        content = template_manager.format_template(MODULE_TEMPLATES["init"], names)
        FileManager.create_file(module_dir / "__init__.py", content, "__init__.py")

    if options.get("include_models", True):
        content = template_manager.format_template(MODULE_TEMPLATES["models"], names)
        FileManager.create_file(module_dir / "models.py", content, "models.py")

    if options.get("include_schemas", True):
        content = template_manager.format_template(MODULE_TEMPLATES["schemas"], names)
        FileManager.create_file(module_dir / "schemas.py", content, "schemas.py")

    if options.get("include_crud", True):
        content = template_manager.format_template(MODULE_TEMPLATES["crud"], names)
        FileManager.create_file(module_dir / "crud.py", content, "crud.py")

    if options.get("include_services", True):
        content = template_manager.format_template(MODULE_TEMPLATES["services"], names)
        FileManager.create_file(module_dir / "services.py", content, "services.py")

    if options.get("include_endpoints", True):
        content = template_manager.format_template(MODULE_TEMPLATES["endpoints"], names)
        FileManager.create_file(module_dir / "endpoints.py", content, "endpoints.py")

    if options.get("include_readme", True):
        content = template_manager.format_template(MODULE_TEMPLATES["readme"], names)
        FileManager.create_file(module_dir / "README.md", content, "README.md")

    if options.get("include_tests", True):
        content = template_manager.format_template(MODULE_TEMPLATES["tests"], names)
        FileManager.create_file(module_dir / "tests.py", content, "tests.py")

    print(f"✅ Module '{name}' generated successfully\!")


def generate_service(
    module_name: str,
    service_key: str,
    name_pt: str,
    name_en: str,
    service_type: str,
    options: dict[str, Any],
) -> None:
    """Generate a single service within a module."""
    print(f"🔧 Generating service: {service_key} in module: {module_name}")

    paths = get_base_paths()
    module_path = paths["modules"] / module_name.lower()

    # Validate inputs
    Validation.validate_module_exists(module_path)
    Validation.validate_service_key(service_key)
    Validation.validate_names(name_pt, name_en)

    # Generate names
    names = NamingConvention.generate_names(service_key, module_name.lower())
    names.update(
        {
            "display_name_pt": name_pt,
            "display_name_en": name_en,
            "display_name_pt_lower": name_pt.lower(),
            "display_name_en_lower": name_en.lower(),
            "service_type": service_type,
            "nullable_municipe": "True" if service_type == "internal" else "False",
        }
    )

    template_manager = TemplateManager()

    # Create service directories
    models_dir = module_path / "models"
    schemas_dir = module_path / "schemas"
    routes_dir = module_path / "routes"
    tests_dir = module_path / "tests"

    FileManager.create_directory(models_dir, "models directory")
    FileManager.create_directory(schemas_dir, "schemas directory")
    FileManager.create_directory(routes_dir, "routes directory")

    if options.get("include_tests", True):
        FileManager.create_directory(tests_dir, "tests directory")

    # Validate service doesn't exist
    service_model_path = models_dir / f"{names['service_slug']}.py"
    Validation.validate_service_not_exists(service_model_path)

    # Generate model file
    model_content = template_manager.format_template(SERVICE_TEMPLATES["model"], names)
    FileManager.create_file(service_model_path, model_content, "model file")

    # Generate schema file
    schema_content = template_manager.format_template(SERVICE_TEMPLATES["schema"], names)
    FileManager.create_file(
        schemas_dir / f"{names['service_slug']}.py", schema_content, "schema file"
    )

    # Generate route file based on service type
    route_template = "route_citizen" if service_type == "citizen" else "route_internal"
    route_content = template_manager.format_template(SERVICE_TEMPLATES[route_template], names)
    FileManager.create_file(routes_dir / f"{names['service_slug']}.py", route_content, "route file")

    # Register service in services.py
    ServiceRegistry.register_in_services(module_path, names, service_type)

    # Register in __init__.py
    ServiceRegistry.register_in_init(module_path, names)

    # Generate test file if requested
    if options.get("include_tests", True):
        test_content = template_manager.format_template(SERVICE_TEMPLATES["test"], names)
        FileManager.create_file(
            tests_dir / f"test_{names['service_slug']}.py", test_content, "test file"
        )

    print(f"✅ Service '{name_pt}' generated successfully\!")


def generate_batch(services: list[dict[str, str]], options: dict[str, Any]) -> None:
    """Generate multiple services in batch."""
    if not services:
        print("❌ No services to generate")
        return

    print(f"🚀 Starting batch generation of {len(services)} services...")

    tracker = ProgressTracker(len(services))

    for service in services:
        try:
            tracker.start_service(
                service["module"], service["service_key"], service["service_name_pt"]
            )

            generate_service(
                service["module"],
                service["service_key"],
                service["service_name_pt"],
                service["service_name_en"],
                service.get("service_type", "citizen"),
                options,
            )

            tracker.success_service(
                service["module"], service["service_key"], service["service_name_pt"]
            )

        except Exception as e:
            tracker.fail_service(
                service["module"],
                service["service_key"],
                service["service_name_pt"],
                str(e),
            )

    tracker.print_summary()


def get_default_services() -> list[dict[str, str]]:
    """Get default list of services for batch generation."""
    return [
        {
            "module": "citizenship",
            "service_key": "EmissaoBI",
            "service_name_pt": "Emissão de BI",
            "service_name_en": "ID Card Issuance",
            "service_type": "citizen",
        },
        {
            "module": "citizenship",
            "service_key": "AtualizacaoEndereco",
            "service_name_pt": "Atualização de Endereço",
            "service_name_en": "Address Update",
            "service_type": "citizen",
        },
        {
            "module": "health",
            "service_key": "AgendamentoConsulta",
            "service_name_pt": "Agendamento de Consulta",
            "service_name_en": "Medical Appointment",
            "service_type": "citizen",
        },
        {
            "module": "health",
            "service_key": "SolicitacaoExame",
            "service_name_pt": "Solicitação de Exame",
            "service_name_en": "Lab Test Request",
            "service_type": "citizen",
        },
        {
            "module": "education",
            "service_key": "MatriculaEscolar",
            "service_name_pt": "Matrícula Escolar",
            "service_name_en": "School Enrollment",
            "service_type": "citizen",
        },
        {
            "module": "commercial",
            "service_key": "AberturaProcesso",
            "service_name_pt": "Abertura de Processo",
            "service_name_en": "Process Opening",
            "service_type": "internal",
        },
        {
            "module": "urbanism",
            "service_key": "LicencaConstrucao",
            "service_name_pt": "Licença de Construção",
            "service_name_en": "Building Permit",
            "service_type": "internal",
        },
    ]


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Universal SILA Module and Service Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a complete module
  python generate_module.py module health --title "Health Services" --description "Healthcare management"

  # Generate a single service
  python generate_module.py service health AgendamentoConsulta "Agendamento de Consulta" "Medical Appointment"

  # Generate services from CSV
  python generate_module.py batch --csv services.csv --type internal

  # Generate default services
  python generate_module.py batch --default --tests

  # Create sample CSV
  python generate_module.py batch --create-csv sample.csv
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Module generation
    module_parser = subparsers.add_parser("module", help="Generate a complete FastAPI module")
    module_parser.add_argument("name", help="Module name (e.g., Health, Education)")
    module_parser.add_argument("--title", help="Module title (defaults to module name)")
    module_parser.add_argument("--description", help="Module description")
    module_parser.add_argument("--no-init", action="store_true", help="Skip __init__.py")
    module_parser.add_argument("--no-models", action="store_true", help="Skip models.py")
    module_parser.add_argument("--no-schemas", action="store_true", help="Skip schemas.py")
    module_parser.add_argument("--no-crud", action="store_true", help="Skip crud.py")
    module_parser.add_argument("--no-services", action="store_true", help="Skip services.py")
    module_parser.add_argument("--no-endpoints", action="store_true", help="Skip endpoints.py")
    module_parser.add_argument("--no-readme", action="store_true", help="Skip README.md")
    module_parser.add_argument("--no-tests", action="store_true", help="Skip tests.py")
    module_parser.add_argument("--no-routes", action="store_true", help="Skip routes directory")
    module_parser.add_argument("--no-tests-dir", action="store_true", help="Skip tests directory")

    # Service generation
    service_parser = subparsers.add_parser("service", help="Generate a single service")
    service_parser.add_argument("module", help="Target module name")
    service_parser.add_argument(
        "service_key", help="Service identifier (e.g., AgendamentoConsulta)"
    )
    service_parser.add_argument("name_pt", help="Portuguese name")
    service_parser.add_argument("name_en", help="English name")
    service_parser.add_argument(
        "--type",
        choices=["citizen", "internal"],
        default="citizen",
        help="Service type",
    )
    service_parser.add_argument("--no-tests", action="store_true", help="Skip test file generation")
    service_parser.add_argument(
        "--no-registration", action="store_true", help="Skip service registration"
    )

    # Batch generation
    batch_parser = subparsers.add_parser("batch", help="Generate multiple services")
    batch_group = batch_parser.add_mutually_exclusive_group(required=True)
    batch_group.add_argument("--csv", type=str, help="CSV file with services to generate")
    batch_group.add_argument("--default", action="store_true", help="Use default services list")
    batch_group.add_argument("--create-csv", type=str, help="Create sample CSV file")
    batch_parser.add_argument(
        "--type",
        choices=["citizen", "internal"],
        default="citizen",
        help="Default service type for CSV",
    )
    batch_parser.add_argument("--no-tests", action="store_true", help="Skip test files")

    # Global options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without creating files",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        # Validate environment
        validate_environment()

        # Prepare options
        options = {
            "include_init": not getattr(args, "no_init", False),
            "include_models": not getattr(args, "no_models", False),
            "include_schemas": not getattr(args, "no_schemas", False),
            "include_crud": not getattr(args, "no_crud", False),
            "include_services": not getattr(args, "no_services", False),
            "include_endpoints": not getattr(args, "no_endpoints", False),
            "include_readme": not getattr(args, "no_readme", False),
            "include_tests": not getattr(args, "no_tests", False),
            "include_routes": not getattr(args, "no_routes", False),
            "include_tests_dir": not getattr(args, "no_tests_dir", False),
            "dry_run": getattr(args, "dry_run", False),
            "verbose": getattr(args, "verbose", False),
            "force": getattr(args, "force", False),
        }

        if args.command == "module":
            title = args.title or args.name
            description = (
                args.description or f"gerenciar funcionalidades relacionadas a {title.lower()}"
            )
            generate_module(args.name, title, description, options)

        elif args.command == "service":
            generate_service(
                args.module,
                args.service_key,
                args.name_pt,
                args.name_en,
                args.type,
                options,
            )

        elif args.command == "batch":
            if args.create_csv:
                CSVProcessor.create_sample_csv(Path(args.create_csv))
            else:
                if args.csv:
                    services = CSVProcessor.read_services_csv(Path(args.csv))
                else:  # default
                    services = get_default_services()

                # Override service type if specified
                for service in services:
                    if "service_type" not in service:
                        service["service_type"] = args.type

                generate_batch(services, options)

        print("🎉 Code generation completed successfully\!")

    except CodeGenError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
