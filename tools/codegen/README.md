# 🚀 SILA System - Universal Code Generator

## 📦 Overview

The **Universal SILA Code Generator** is a comprehensive scaffolding system that unifies
all module and service generation functionality into a single, robust tool. This system
replaces four separate legacy scripts with one powerful, feature-rich solution.

---

## 🎯 What This Replaces

This unified system consolidates the following deprecated scripts:

| Legacy Script                | Status        | Replacement                  |
| ---------------------------- | ------------- | ---------------------------- |
| `add_new_service.py`         | ❌ Deprecated | `generate_module.py module`  |
| `batch_generate_services.py` | ❌ Deprecated | `generate_module.py batch`   |
| `create_service.py`          | ❌ Deprecated | `generate_module.py service` |
| `generate_service.py`        | ❌ Deprecated | `generate_module.py service` |

> **⚠️ Migration Notice**: The legacy scripts now show deprecation warnings and redirect
> to the new unified system.

---

## ✨ Features

- 🔧 **Complete Module Generation**: Create full FastAPI modules with all necessary
  files
- 🔌 **Individual Service Generation**: Add services to existing modules
- 📊 **Batch Operations**: Generate multiple services from CSV or predefined lists
- 🌐 **Bilingual Support**: Portuguese and English naming conventions
- 🏷️ **Service Types**: Support for citizen and internal service types
- ✅ **Comprehensive Validation**: Input validation and error handling
- 🔄 **Automatic Registration**: Auto-register services in the system
- 🧪 **Test Generation**: Optional test file creation
- 📚 **Template-Based**: Extensible template system
- 🎛️ **Rich CLI**: Intuitive command-line interface

---

## 📁 Directory Structure

```
tools/codegen/
├── generate_module.py          # 🆕 Main unified generator
├── utils.py                   # 🔧 Shared utilities
├── templates.py               # 📄 Code templates
├── deprecated_wrapper.py      # ⚠️  Deprecation handler
├── add_new_service.py.deprecated         # Legacy scripts
├── batch_generate_services.py.deprecated  # (preserved for reference)
├── create_service.py.deprecated
└── generate_service.py.deprecated
```

---

## 🚀 Quick Start

### Basic Usage

```bash
# Show help
python tools/codegen/generate_module.py --help

# Generate a complete module
python tools/codegen/generate_module.py module health --title "Health Services"

# Generate a single service
python tools/codegen/generate_module.py service health AgendamentoConsulta \
    "Agendamento de Consulta" "Medical Appointment"

# Batch generate from CSV
python tools/codegen/generate_module.py batch --csv services.csv

# Generate default services
python tools/codegen/generate_module.py batch --default
```

---

## 📖 Detailed Usage

### 1. Module Generation

Create a complete FastAPI module with all necessary files:

```bash
python tools/codegen/generate_module.py module <module_name> [options]
```

**Options:**

- `--title`: Module title (defaults to module name)
- `--description`: Module description
- `--no-*`: Skip specific files (e.g., `--no-tests`, `--no-readme`)

**Example:**

```bash
python tools/codegen/generate_module.py module education \
    --title "Education Services" \
    --description "Educational services and school management" \
    --no-tests  # Skip test generation
```

**Generated Structure:**

```
backend/modules/education/
├── __init__.py          # Module initialization and routing
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic schemas
├── crud.py            # CRUD operations
├── services.py        # Business logic
├── endpoints.py       # API endpoints
└── README.md          # Documentation
```

### 2. Service Generation

Add a service to an existing module:

```bash
python tools/codegen/generate_module.py service <module> <service_key> <name_pt> <name_en> [options]
```

**Parameters:**

- `module`: Target module name
- `service_key`: Service identifier (e.g., `AgendamentoConsulta`)
- `name_pt`: Portuguese name
- `name_en`: English name

**Options:**

- `--type`: Service type (`citizen` or `internal`, default: `citizen`)
- `--no-tests`: Skip test file generation
- `--no-registration`: Skip automatic service registration

**Example:**

```bash
python tools/codegen/generate_module.py service health \
    AgendamentoConsulta \
    "Agendamento de Consulta" \
    "Medical Appointment" \
    --type citizen \
    --no-tests
```

**Generated Files:**

```
backend/modules/health/
├── models/agendamento_consulta.py       # SQLAlchemy model
├── schemas/agendamento_consulta.py      # Pydantic schemas
├── routes/agendamento_consulta.py       # API routes
└── tests/test_agendamento_consulta.py   # Tests (if enabled)
```

### 3. Batch Generation

Generate multiple services at once:

```bash
python tools/codegen/generate_module.py batch [source] [options]
```

**Sources:**

- `--csv <file>`: Generate from CSV file
- `--default`: Generate from predefined list
- `--create-csv <file>`: Create sample CSV file

**Options:**

- `--type`: Default service type for CSV generation
- `--no-tests`: Skip test files

**CSV Format:**

```csv
module,service_key,service_name_pt,service_name_en,service_type
health,AgendamentoConsulta,Agendamento de Consulta,Medical Appointment,citizen
health,SolicitacaoExame,Solicitação de Exame,Lab Test Request,citizen
citizenship,EmissaoBI,Emissão de BI,ID Card Issuance,citizen
```

**Example:**

```bash
# Create sample CSV
python tools/codegen/generate_module.py batch --create-csv services.csv

# Generate from CSV
python tools/codegen/generate_module.py batch --csv services.csv --type citizen

# Generate default services
python tools/codegen/generate_module.py batch --default --type internal
```

---

## 🎨 Templates and Customization

### Template System

The generator uses a flexible template system defined in `templates.py`. Templates
support:

- **Variable Substitution**: `{variable_name}` placeholders
- **Conditional Logic**: Service type-based template selection
- **Bilingual Support**: Portuguese and English variants

### Adding Custom Templates

1. Edit `tools/codegen/templates.py`
2. Add new template to `MODULE_TEMPLATES` or `SERVICE_TEMPLATES`
3. Update the generator logic in `generate_module.py`

### Template Variables

**Module Templates:**

- `{module_name}`: Module name (e.g., "health")
- `{module_title}`: Module title (e.g., "Health Services")
- `{module_description}`: Module description

**Service Templates:**

- `{model_name}`: PascalCase model name (e.g., "AgendamentoConsulta")
- `{service_slug}`: snake_case service slug (e.g., "agendamento_consulta")
- `{api_slug}`: kebab-case API slug (e.g., "agendamento-consulta")
- `{display_name_pt}`: Portuguese display name
- `{display_name_en}`: English display name
- `{module_name}`: Parent module name
- `{service_type}`: Service type ("citizen" or "internal")

---

## 🔧 Advanced Features

### Service Types

**Citizen Services:**

- Include user authentication (`municipe_id` field)
- User-scoped operations (users see only their own data)
- Routes: `/api/{service-slug}/`

**Internal Services:**

- No user authentication required
- Administrative operations
- Routes: `/internal/{service-slug}/`

### Automatic Registration

Services are automatically registered in the system:

1. **Service Hub Registration**: Added to `services.py` with `@register_service`
   decorator
2. **Route Integration**: Routes included in module's main router
3. **Documentation**: Comments added to `__init__.py`

### Validation

The system includes comprehensive validation:

- **Module Existence**: Validates target modules exist
- **Service Uniqueness**: Prevents duplicate services
- **Naming Conventions**: Enforces proper naming rules
- **File Structure**: Ensures proper directory structure

---

## 🧪 Testing

### Running Tests

```bash
# Test the generator (dry run)
python tools/codegen/generate_module.py service health TestService \
    "Teste Service" "Test Service" --dry-run

# Generate with tests
python tools/codegen/generate_module.py service health TestService \
    "Teste Service" "Test Service" --no-tests  # Skip tests
```

### Test Structure

Generated tests follow this pattern:

```python
def test_criar_{service_slug}(client: TestClient, db: Session):
    """Test creating a new {display_name_lower}"""
    # Test implementation

def test_obter_{service_slug}(client: TestClient, db: Session):
    """Test getting a {display_name_lower} by ID"""
    # Test implementation

def test_listar_{service_slug}(client: TestClient, db: Session):
    """Test listing {display_name_lower}"""
    # Test implementation
```

---

## 🔄 Migration from Legacy Scripts

### Before (Deprecated)

```bash
# Old way - DON'T USE
python tools/codegen/add_new_service.py Finance --title "Financial Services"
python tools/codegen/create_service.py --single health AgendamentoConsulta "Agendamento" "Appointment"
python tools/codegen/batch_generate_services.py --default
```

### After (New Way)

```bash
# New unified way
python tools/codegen/generate_module.py module finance --title "Financial Services"
python tools/codegen/generate_module.py service health AgendamentoConsulta "Agendamento de Consulta" "Medical Appointment"
python tools/codegen/generate_module.py batch --default
```

### Migration Benefits

- ✅ **Single Tool**: One script for all operations
- ✅ **Better CLI**: Improved argument parsing and help
- ✅ **More Features**: Enhanced templates and validation
- ✅ **Better Error Handling**: Clear error messages and recovery
- ✅ **Documentation**: Comprehensive help and examples

---

## 🛠️ Development and Extension

### Adding New Templates

1. **Edit Templates**: Modify `tools/codegen/templates.py`
2. **Update Generator**: Add template handling in `generate_module.py`
3. **Test**: Validate with `--dry-run` option

### Custom Validation Rules

Add validation in `utils.py`:

```python
@staticmethod
def validate_custom_rule(value: str) -> None:
    """Custom validation logic."""
    if not condition:
        raise CodeGenError("Custom validation failed")
```

### Integration with CI/CD

```bash
#!/bin/bash
# Example CI/CD integration
python tools/codegen/generate_module.py batch --csv services.csv --type citizen
python -m pytest backend/tests/  # Run generated tests
```

---

## 📚 CSV File Format

### Header (Required)

```csv
module,service_key,service_name_pt,service_name_en,service_type
```

### Data Rows

```csv
health,AgendamentoConsulta,Agendamento de Consulta,Medical Appointment,citizen
health,SolicitacaoExame,Solicitação de Exame,Lab Test Request,citizen
education,MatriculaEscolar,Matrícula Escolar,School Enrollment,citizen
commercial,AberturaProcesso,Abertura de Processo,Process Opening,internal
```

### Comments

```csv
# This is a comment line (will be ignored)
module,service_key,service_name_pt,service_name_en,service_type
```

---

## 🚨 Troubleshooting

### Common Issues

**"Module not found" Error:**

```bash
# Check if module exists
ls backend/modules/

# Create module first if needed
python tools/codegen/generate_module.py module newmodule
```

**"Service already exists" Error:**

```bash
# Check existing services in module
ls backend/modules/health/models/

# Use different service key or delete existing
rm backend/modules/health/models/existing_service.py
```

**Template Formatting Errors:**

```bash
# Check template syntax in templates.py
# Validate all required variables are provided
```

### Getting Help

```bash
# Show all options
python tools/codegen/generate_module.py --help

# Show module generation help
python tools/codegen/generate_module.py module --help

# Show service generation help
python tools/codegen/generate_module.py service --help

# Show batch generation help
python tools/codegen/generate_module.py batch --help
```

### Debug Mode

```bash
# Enable verbose output
python tools/codegen/generate_module.py service health TestService \
    "Test Service" "Test Service" --verbose

# Dry run to see what would be generated
python tools/codegen/generate_module.py service health TestService \
    "Test Service" "Test Service" --dry-run
```

---

## 📋 Best Practices

### Naming Conventions

**Module Names:**

- Use singular nouns (e.g., `health`, not `healths`)
- Lowercase with underscores if needed (e.g., `social_services`)

**Service Keys:**

- PascalCase for model names (e.g., `AgendamentoConsulta`)
- Descriptive and unique within module
- Start with letter, contain only letters and numbers

**Display Names:**

- Portuguese: Proper capitalization (e.g., "Agendamento de Consulta")
- English: Proper capitalization (e.g., "Medical Appointment")
- Keep under 200 characters

### Service Types

**Use `citizen` for:**

- Services that citizens directly access
- Operations requiring user authentication
- User-scoped data operations

**Use `internal` for:**

- Administrative operations
- Background processes
- System-to-system integrations

### File Organization

```
backend/modules/{module_name}/
├── __init__.py              # Always include
├── models.py               # Module-level models
├── schemas.py              # Module-level schemas
├── crud.py                 # Module-level CRUD
├── services.py             # Business logic and registrations
├── endpoints.py            # Module-level endpoints
├── models/                 # Individual service models
│   └── {service_slug}.py
├── schemas/                # Individual service schemas
│   └── {service_slug}.py
├── routes/                 # Individual service routes
│   └── {service_slug}.py
└── tests/                  # Individual service tests
    └── test_{service_slug}.py
```

---

## 🤝 Contributing

### Adding Features

1. **Update Templates**: Add new templates in `templates.py`
2. **Enhance Utils**: Add utilities in `utils.py`
3. **Update CLI**: Modify argument parsing in `generate_module.py`
4. **Add Tests**: Create tests for new functionality
5. **Update Docs**: Document new features in this README

### Code Style

- Follow PEP 8 conventions
- Use type hints for all functions
- Add docstrings for public functions
- Include error handling for all operations

---

## 📞 Support

For issues or questions:

- **Documentation**: This README file
- **Code Review**: Submit pull requests with detailed descriptions
- **Issues**: Report bugs with reproduction steps
- **Team Chat**: #sila-dev channel

---

## 🔄 Version History

### v2.0.0 (Current)

- ✅ Unified all legacy scripts into single tool
- ✅ Enhanced CLI with comprehensive options
- ✅ Added bilingual support (Portuguese/English)
- ✅ Improved template system with validation
- ✅ Added batch processing capabilities
- ✅ Comprehensive error handling and logging
- ✅ Automatic service registration
- ✅ Test file generation

### v1.x (Legacy)

- ❌ Multiple separate scripts
- ❌ Limited CLI options
- ❌ Basic template system
- ❌ Manual service registration
- ❌ Limited error handling

---

## 📄 License

This code generator is part of the SILA System and follows the same licensing terms.

---

**Last Updated**: 2025-10-24 **Maintained By**: SILA Development Team
