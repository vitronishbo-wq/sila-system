# SILA Scripts Directory

## 🏗️ Optimized Structure

This directory has been optimized as part of Phase 4.1: Tooling and Governance
Optimization.

### Directory Structure

- **`essential/`** - Core system operation scripts
- **`security/`** - Security audit and remediation tools
- **`deployment/`** - Deployment and setup utilities
- **`backup/`** - Backup and recovery operations
- **`archive/`** - Deprecated and one-time migration scripts

### Automation Integration

- **Pre-commit hooks** handle code formatting, linting, and basic validation
- **CI/CD pipelines** handle testing, building, and security scanning
- **Security tools** run automatically in development and deployment

### Usage

```bash
# Run security audit
python scripts/security/security_audit.py

# Deploy to production
./scripts/deployment/deploy_production.sh

# Create backup
./scripts/backup/create_backup.sh
```

For detailed documentation, see each subdirectory.
