# SILA System – Command Index

## 1. Deployment Commands

### 1.1 Official Deployment

1.1.1 `./deploy_official.sh --env=development --services=backend`  Deploy backend in
development environment

1.1.2 `./deploy_official.sh --env=production --services=all`  Full production deployment
with all services

1.1.3 `./deploy_official.sh --env=staging --services=frontend --build`  Deploy frontend
in staging with build

1.1.4 `./deploy_official.sh --env=dev --services=backend --force`  Force deployment even
if checks fail

### 1.2 Alternative Deployment Methods

1.2.1 `./deploy_final.sh`  Final deployment script for production

1.2.2 `./deploy_final_plus.sh`  Enhanced deployment with additional checks

1.2.3 `./deploy_master.sh`  Master deployment orchestrator

1.2.4 `./deploy_inteligente.sh`  Intelligent deployment with auto-detection

1.2.5 `./deploy_multi_ambiente.sh`  Multi-environment deployment

1.2.6 `./deploy_multi_ambiente_ci.sh`  CI/CD multi-environment deployment

### 1.3 Quick Deployment

1.3.1 `./quick_deploy.sh`  Fast deployment for development

1.3.2 `./start.sh`  Quick start script

## 2. Health Checks & Monitoring

### 2.1 Health Checking

2.1.1 `python3 health/health_checker.py`  Run comprehensive system health check

2.1.2 `bash health/test_health_system.sh`  Test health checking system

2.1.3 `python3 backend/scripts/run_health_check.py`  Backend-specific health check

### 2.2 Monitoring System

2.2.1 `bash scripts/start_monitoring_complete.sh`  Start full monitoring stack
(Prometheus + Grafana + Loki)

2.2.2 `bash scripts/start_monitoring_complete.sh stop`  Stop monitoring stack

2.2.3 `bash scripts/start_monitoring_complete.sh restart`  Restart monitoring stack

2.2.4 `bash scripts/start_monitoring_complete.sh status`  Show monitoring service status

2.2.5 `bash scripts/start_monitoring_complete.sh logs`  Show monitoring service logs

2.2.6 `bash scripts/quick_monitoring_check.sh`  Quick monitoring status check

2.2.7 `bash scripts/validate_monitoring_setup.sh`  Validate monitoring configuration

### 2.3 System Monitoring

2.3.1 `./monitor_sila.sh`  Monitor SILA system status

2.3.2 `python3 monitor_documents.py`  Monitor document processing

2.3.3 `./nginx_monitor.sh`  Monitor nginx service

2.3.4 `./nginx_diagnostic.sh`  Nginx diagnostic checks

## 3. Testing & Diagnostics

### 3.1 Test Execution

3.1.1 `python3 scripts/run_tests.py`  Run comprehensive test suite with coverage

3.1.2 `bash scripts/run_tests.sh`  Test runner script

3.1.3 `./test_deploy_final.sh`  Test final deployment

3.1.4 `./test_bootstrap.sh`  Test bootstrap process

3.1.5 `./test_authentication_solution.sh`  Test authentication system

3.1.6 `./test_banner.sh`  Test system banner

3.1.7 `./smoke-test.sh`  Smoke testing

3.1.8 `bash scripts/smoke_login.sh`  Smoke login testing

### 3.2 Integration Tests

3.2.1 `python3 backend/tests/integration/test_*.py`  Run specific integration tests

3.2.2 `python3 ci/run_tests.py`  CI/CD test runner

3.2.3 `python3 scripts/phase5_integration_tests.py`  Phase 5 integration tests

### 3.3 Diagnostic Tools

3.3.1 `python3 scripts/quick_check.py`  Quick system diagnostic

3.3.2 `python3 scripts/quick_test.py`  Quick functionality test

3.3.3 `python3 scripts/validate_py_syntax.py`  Validate Python syntax

3.3.4 `python3 ci/validate_py_syntax.py`  CI Python syntax validation

## 4. Environment & Setup

### 4.1 Bootstrap & Initialization

4.1.1 `./bootstrap.sh`  Initialize development environment

4.1.2 `./bootstrap_sila_backend.sh`  Backend-specific bootstrap

4.1.3 `./bootstrap_sila_backend_enterprise.sh`  Enterprise backend bootstrap

4.1.4 `./prepare_environment.sh`  Prepare deployment environment

4.1.5 `./complete_env.sh`  Complete environment setup

4.1.6 `./setup_env.ps1`  PowerShell environment setup

### 4.2 Database Management

4.2.1 `./init_database.sh`  Initialize database

4.2.2 `python3 init_db.py`  Python database initialization

4.2.3 `python3 backend/init_db.py`  Backend database setup

4.2.4 `python3 backend/create_superuser.py`  Create superuser account

4.2.5 `python3 backend/create_user.py`  Create regular user account

### 4.3 Configuration Management

4.3.1 `python3 config/config_manager.py`  Configuration management tool

4.3.2 `./config/test_config_system.sh`  Test configuration system

4.3.3 `./fix_auth_env.sh`  Fix authentication environment

4.3.4 `python3 auto_fix_auth_env.py`  Auto-fix auth environment

## 5. Development & Maintenance

### 5.1 Code Generation

5.1.1 `python3 tools/codegen/generate_service.py`  Generate new service

5.1.2 `python3 tools/codegen/batch_generate_services.py`  Batch generate services

5.1.3 `python3 tools/codegen/create_service.py`  Create service template

5.1.4 `python3 tools/codegen/add_new_service.py`  Add new service

### 5.2 Import Management

5.2.1 `python3 tools/scan_and_fix_imports.py`  Scan and fix imports

5.2.2 `python3 tools/autoheal_imports.py`  Auto-heal imports

5.2.3 `python3 tools/fix_missing_imports.py`  Fix missing imports

5.2.4 `python3 tools/check_location_import.py`  Check location imports

### 5.3 Module Management

5.3.1 `python3 scripts/create_modules.py`  Create new modules

5.3.2 `python3 scripts/check_module_integrity.py`  Check module integrity

5.3.3 `python3 scripts/validate-module-integrity.py`  Validate module structure

5.3.4 `python3 scripts/generate_modules_structure.py`  Generate module structure

## 6. Documentation & Validation

### 6.1 Documentation Generation

6.1.1 `bash frontend/scripts/gerar_documentacao_backend.sh`  Generate backend
documentation

6.1.2 `bash frontend/scripts/gerar_jsdoc_frontend.sh`  Generate frontend JSDoc

6.1.3 `bash frontend/scripts/validar_documentacao.sh`  Validate documentation

### 6.2 System Validation

6.2.1 `bash frontend/scripts/validar_autenticacao_tokens.sh`  Validate authentication
tokens

6.2.2 `bash frontend/scripts/validar_endpoints_rotas.sh`  Validate endpoints and routes

6.2.3 `bash frontend/scripts/validar_env_compatibilidade.sh`  Validate environment
compatibility

6.2.4 `bash frontend/scripts/validar_estrutura_modular.sh`  Validate modular structure

6.2.5 `bash frontend/scripts/validar_modulos_compatibilidade.sh`  Validate module
compatibility

## 7. Security & Authentication

### 7.1 Security Management

7.1.1 `bash scripts/rotate_secret_key.sh`  Rotate secret keys

7.1.2 `bash scripts/deploy_secret_key_production.sh`  Deploy production secret keys

7.1.3 `python3 scripts/list_users.py`  List system users

7.1.4 `python3 migrate_user_passwords.py`  Migrate user passwords

### 7.2 Authentication

7.2.1 `bash scripts/auto_create_admin.sh`  Auto-create admin user

7.2.2 `bash scripts/create_branch_for_admin.sh`  Create admin branch

7.2.3 `bash scripts/consolidate_auth.sh`  Consolidate authentication

## 8. Backup & Recovery

### 8.1 Backup Operations

8.1.1 `bash scripts/automated_backup.sh`  Automated backup system

8.1.2 `bash scripts/restore_backup.sh`  Restore from backup

8.1.3 `bash scripts/generate_backup_metrics.sh`  Generate backup metrics

### 8.2 Cleanup Operations

8.2.1 `./cleanup_temp_files.sh`  Clean temporary files

8.2.2 `bash scripts/purge_duplicates.sh`  Purge duplicate files

8.2.3 `python3 scripts/cleanup_fragments.py`  Cleanup code fragments

8.2.4 `python3 scripts/cleanup_production_env.py`  Cleanup production environment

## 9. Infrastructure & DevOps

### 9.1 Docker Management

9.1.1 `./get-docker.sh`  Install Docker

9.1.2 `./setup_docker_hd.sh`  Setup Docker on hard drive

9.1.3 `./setup_docker_storage.sh`  Setup Docker storage

9.1.4 `./nginx_automation.sh`  Nginx automation

### 9.2 Service Management

9.1.5 `./start_api_stack.sh`  Start API service stack

9.1.6 `./start_live_stack.sh`  Start live service stack

9.1.7 `bash scripts/start_all.sh`  Start all services

9.1.8 `bash scripts/run_full.sh`  Run full service stack

## 10. Utility Commands

### 10.1 Development Utilities

10.1.1 `./abrir-windsurf.sh`  Open development environment

10.1.2 `./changelog_auto.sh`  Auto-generate changelog

10.1.3 `./update_comandos.sh`  Update command list

10.1.4 `./make_executable.sh`  Make scripts executable

### 10.2 System Utilities

10.2.1 `./clean_pendrive_safe.sh`  Safe pendrive cleanup

10.2.2 `./setup_ssh.sh`  Setup SSH access

10.2.3 `./setup_git_remote.sh`  Setup Git remote

10.2.4 `./install_vsc_extensions.sh`  Install VSCode extensions

## 11. Script Collections

### 11.1 Command Collections

11.1.1 `./COMANDOS_PRONTOS.sh`  Ready-to-use commands

11.1.2 `./COMANDOS_MONITORING_SCHEMAS.sh`  Monitoring schema commands

11.1.3 `bash scripts/automate_rascunho.sh`  Automation draft script

11.1.4 `bash scripts/final_resolution.sh`  Final resolution script

## Usage Notes

- **Environment Variables**: Most commands respect environment variables for
  configuration
- **Log Files**: Check `./logs/` directory for execution logs
- **Permissions**: Some commands may require sudo privileges
- **Dependencies**: Ensure all dependencies are installed before running commands

## Quick Reference

### Development

```bash
./bootstrap.sh                    # Start development
./deploy_official.sh --env=dev    # Deploy to development
python3 scripts/run_tests.py      # Run tests
```

### Production

```bash
./deploy_official.sh --env=production  # Production deployment
bash scripts/start_monitoring_complete.sh  # Start monitoring
python3 health/health_checker.py       # Health check
```

### Maintenance

```bash
bash scripts/automated_backup.sh       # Backup
python3 scripts/cleanup_fragments.py    # Cleanup
bash scripts/rotate_secret_key.sh      # Security
```

_Last updated: 2025-10-23_
