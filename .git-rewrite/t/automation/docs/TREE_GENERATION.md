# Project Tree Generation System

## Overview

The SILA System uses an automated script to generate clean, focused project structure
documentation. This replaces obsolete and redundant tree generation scripts that were
scattered across the project.

## Purpose

- **Documentation**: Keep project structure documentation up-to-date automatically
- **Auditing**: Provide snapshots of project structure for compliance and auditing
- **CI/CD Integration**: Use in pipelines to validate project organization
- **Development Reference**: Quick reference for project structure during development

## Generated Files

The script generates three hidden markdown files in the project root:

| File                | Scope                | Contents                                        |
| ------------------- | -------------------- | ----------------------------------------------- |
| `.tree-root.md`     | Project Root         | Complete project structure (configurable depth) |
| `.tree-backend.md`  | Backend Application  | Backend-specific structure                      |
| `.tree-frontend.md` | Frontend Application | Frontend-specific structure                     |

These files are:

- **Hidden** (prefixed with `.`) for a clean project root view
- **Ignored** by Git (added to `.gitignore`)
- **Auto-generated** - regenerate with each run to keep current
- **Marked with timestamps** for version tracking

## Usage

### Basic Usage

Generate with default settings (max depth: 4):

```bash
./scripts/generate_project_tree.sh
```

### Custom Depth

Generate with a specific max depth:

```bash
# Depth of 2 - shows only immediate subdirectories
./scripts/generate_project_tree.sh 2

# Depth of 5 - shows deeper nesting
./scripts/generate_project_tree.sh 5

# Depth of 3 (recommended for most use cases)
./scripts/generate_project_tree.sh 3
```

### View Generated Trees

```bash
# View root tree
cat .tree-root.md

# View backend tree
cat .tree-backend.md

# View frontend tree
cat .tree-frontend.md
```

## Features

### File Filtering

Only displays important file types:

- **Backend**: `.py`, `.sh`, `.md`, `.json`, `.yaml`, `.yml`, `Dockerfile*`, `Makefile`,
  `.env`, `.sql`
- **Frontend**: `.ts`, `.tsx`, `.jsx`, `.js`, `.json`, `.md`, `.yaml`, `.yml`
- **Configuration**: `.conf`, `.txt`, `.env`

### Directory Exclusions

Automatically excludes:

- Virtual environments (`venv`, `.venv`)
- Build artifacts (`node_modules`, `build`, `dist`)
- Cache directories (`__pycache__`, `.pytest_cache`, `.mypy_cache`)
- Generated files (`htmlcov`, `.egg-info`)
- Hidden system directories (`.git`, `.github`, `.husky`)
- Backup and temporary files

### Visual Indicators

Files are marked with intuitive icons:

- 🐍 Python files (`.py`)
- ⚙️ Configuration files (`.json`, `.yaml`, `.yml`, `.sh`)
- 🐳 Docker files (`Dockerfile*`)
- 🛠️ Build files (`Makefile`)
- 📄 Documentation (`.md`, `.txt`)
- 📁 Directories

## Integration

### Pre-commit Hook

Add to your pre-commit configuration to automatically regenerate trees before commits:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: update-project-tree
      name: Update Project Tree
      entry: bash scripts/generate_project_tree.sh
      language: script
      pass_filenames: false
      stages: [commit]
```

### CI/CD Pipeline

Use in your CI/CD pipeline to validate project structure:

```yaml
# .gitlab-ci.yml or .github/workflows/
- name: Update and validate project tree
  run: |
    ./scripts/generate_project_tree.sh
    # Check if tree files were generated without errors
    [ -f .tree-root.md ] && echo "✅ Tree generation successful"
```

### Development Workflow

Include in your development startup scripts:

```bash
#!/bin/bash
# scripts/init_dev_environment.sh

echo "🌳 Generating project trees..."
./scripts/generate_project_tree.sh 3

echo "✅ Development environment ready"
```

## Script Structure

### Key Functions

| Function                        | Purpose                          |
| ------------------------------- | -------------------------------- |
| `log_info()`                    | Info messages (blue)             |
| `log_success()`                 | Success messages (green)         |
| `log_warning()`                 | Warning messages (yellow)        |
| `log_error()`                   | Error messages (red)             |
| `should_include_file()`         | Filter files by extension        |
| `generate_tree()`               | Generate tree for a directory    |
| `generate_tree_with_tree_cmd()` | Alternative using `tree` command |
| `main()`                        | Orchestrate generation           |

### Configuration

Key variables at the top of the script:

```bash
MAX_DEPTH="${1:-4}"              # Default max depth
PROJECT_ROOT="$(pwd)/.."        # Project root detection
EXCLUDE_PATTERNS=(...)          # Directories to skip
INCLUDE_EXTENSIONS=(...)        # File types to include
```

## Requirements

### System Requirements

- Bash shell (v4.0+)
- Standard Unix utilities: `find`, `grep`, `awk`, `sort`
- No external dependencies required

### Optional Enhancements

- `tree` command (if installed, used as fallback for better formatting)

## Troubleshooting

### Script won't run

```bash
# Make sure it's executable
chmod +x scripts/generate_project_tree.sh
```

### Permission denied

```bash
# Run with bash explicitly
bash scripts/generate_project_tree.sh
```

### No files in tree

- Check that the filters in `INCLUDE_EXTENSIONS` match your file types
- Verify exclusion patterns don't match too much
- Check file permissions

### Trees are too deep/shallow

- Adjust the depth parameter
- Use `./scripts/generate_project_tree.sh 2` for shallow trees
- Use `./scripts/generate_project_tree.sh 5` for deeper trees

## Maintenance

### When to Regenerate

The script should be regenerated:

- Regularly (daily during development)
- After major project structure changes
- Before releases or milestones
- In CI/CD pipelines (automatically)

### Updating Filters

To modify what files are included:

1. Edit `INCLUDE_EXTENSIONS` array for file types
2. Edit `EXCLUDE_PATTERNS` array for directories
3. Test with: `./scripts/generate_project_tree.sh 2`

## History

This script replaces obsolete tree generation approaches:

- ~~`backend/validate_structure.py`~~ (removed - use project_maintenance.py instead)
- ~~`backend/estrutura_modulos.txt`~~ (removed - now auto-generated)
- ~~`analyze-project-structure.ps1`~~ (removed - bash script is platform-agnostic)

## Related Scripts

- `scripts/project_maintenance.py` - General project maintenance (clean-files,
  fix-schemas, check-db-urls)
- `devops/validate_compose_structure.sh` - Validate docker-compose.yml structure
- `scripts/bootstrap.sh` - Project bootstrap and initialization

## Example Output

### .tree-backend.md

```markdown
# SILA System - Project Structure

# Scope: Backend Application

# Generated: 20251113T151231Z

# Max Depth: 3
```

⚙️ app/ ····🐍 main.py ····🐍 core.py ····📁 api/ ········🐍 routes.py ········🐍
dependencies.py ····📁 modules/ ········🐍 auth/

```

## Best Practices

1. **Regenerate frequently** - Keep trees in sync with actual structure
2. **Use appropriate depth** - 2-3 for overviews, 4-5 for detailed views
3. **Review before commits** - Check that tree structure reflects changes
4. **Archive old versions** - Keep git history of structure changes
5. **Document structure** - Use `.tree-*.md` files as reference in PRs/code reviews

## Contributing

To improve this script:
1. Test changes in a branch
2. Verify all three trees generate correctly
3. Check file filtering works as expected
4. Update this documentation
5. Submit PR with improvements

## Support

For issues or improvements:
- Check the Troubleshooting section above
- Review the script comments
- Check script output for error messages
- Ask the development team

---

**Last Updated**: 2025-11-13
**Version**: 1.0 (Clean, Functional)
**Status**: ✅ Active and Maintained
```
