# CRITICAL SCRIPTS INVENTORY - SILA System

_Last Updated: 2025-10-23_

## 🚨 MUST-PRESERVE CRITICAL SCRIPTS

### 🔧 System Orchestration & Deployment

**Priority: CRITICAL** - Essential for system operation

| Script                            | Type  | Purpose                          | Criticality |
| --------------------------------- | ----- | -------------------------------- | ----------- |
| `deploy_multi_ambiente.sh`        | Shell | Multi-environment deployment     | 🔴 CRITICAL |
| `deploy_secret_key_production.sh` | Shell | Production secret key deployment | 🔴 CRITICAL |
| `start_all.sh`                    | Shell | Complete system startup          | 🔴 CRITICAL |
| `run_backend.sh`                  | Shell | Backend service startup          | 🔴 CRITICAL |
| `run_frontend.sh`                 | Shell | Frontend service startup         | 🔴 CRITICAL |
| `run_full.sh`                     | Shell | Full system startup              | 🔴 CRITICAL |

### ?? Backup & Recovery

**Priority: HIGH** - Essential for data protection

| Script                       | Type  | Purpose                    | Criticality |
| ---------------------------- | ----- | -------------------------- | ----------- |
| `automated_backup.sh`        | Shell | Automated system backups   | 🔴 CRITICAL |
| `restore_backup.sh`          | Shell | System restoration         | 🔴 CRITICAL |
| `generate_backup_metrics.sh` | Shell | Backup performance metrics | 🟡 HIGH     |

### 🔐 Security & Authentication

**Priority: HIGH** - Essential for system security

| Script                 | Type   | Purpose                             | Criticality |
| ---------------------- | ------ | ----------------------------------- | ----------- |
| `auto_create_admin.sh` | Shell  | Admin user creation                 | 🔴 CRITICAL |
| `consolidate_auth.sh`  | Shell  | Authentication system consolidation | 🔴 CRITICAL |
| `check_credentials.py` | Python | Credential validation               | 🟡 HIGH     |

### 🧪 Testing & Validation

**Priority: MEDIUM** - Essential for quality assurance

| Script                      | Type   | Purpose                          | Criticality |
| --------------------------- | ------ | -------------------------------- | ----------- |
| `run_tests.py`              | Python | Test suite execution             | 🟡 HIGH     |
| `run_tests.sh`              | Shell  | Test execution wrapper           | 🟡 HIGH     |
| `check-frontend-sync.py`    | Python | Frontend-backend synchronization | 🟡 HIGH     |
| `check_module_integrity.py` | Python | Module integrity validation      | ?? HIGH     |

### 🛠️ Maintenance & Monitoring

**Priority: MEDIUM** - Essential for system health

| Script                        | Type   | Purpose                  | Criticality |
| ----------------------------- | ------ | ------------------------ | ----------- |
| `setup_monitoring_schemas.sh` | Shell  | Monitoring system setup  | 🟡 HIGH     |
| `project_maintenance.py`      | Python | System maintenance tasks | 🟡 HIGH     |
| `cleanup_fragments.py`        | Python | System cleanup           | 🟡 HIGH     |
| `ci_monitor.py`               | Python | CI/CD monitoring         | 🟡 HIGH     |

## 📋 PRESERVATION GUIDELINES

### 🔴 CRITICAL (Must Preserve)

- System cannot function without these
- Core deployment and startup scripts
- Security and authentication scripts
- Backup and recovery scripts

### 🟡 HIGH (Should Preserve)

- Important for system quality and maintenance
- Testing and validation scripts
- Monitoring and maintenance scripts
- Can be recreated if lost but with effort

### 🟢 MEDIUM (Nice to Have)

- Utility scripts
- Development tools
- Can be recreated if necessary

## 🚀 IMMEDIATE ACTION REQUIRED

1. **Backup all CRITICAL scripts** to secure location
2. **Validate script dependencies** and ensure all required files are preserved
3. **Test restoration process** using backup scripts
4. **Document any custom modifications** made to standard scripts

## 📁 RELATED DOCUMENTATION

- `DEPLOYMENT.md` - Deployment procedures
- `PRODUCTION_DEPLOYMENT_GUIDE.md` - Production deployment guide
- Monitoring schemas and configuration files

---

_This inventory should be updated whenever scripts are added, modified, or removed from
the system._
