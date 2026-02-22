# SILA System Production SECRET_KEY Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the updated SECRET_KEY to
the production environment.

## Prerequisites

- SSH access to production server with sudo privileges
- Existing SILA system installation on production server
- Backup procedures in place

## Deployment Steps

### Step 1: Pre-Deployment Preparation

1. **Backup Current State**:

   ```bash
   # From your local machine
   ssh user@production-server "cd /opt/sila-system && tar -czf sila-backup-pre-secret-key-$(date +%Y%m%d_%H%M%S).tar.gz ."
   ```

2. **Verify Current Setup**:
   ```bash
   ssh user@production-server "cd /opt/sila-system/backend && ls -la .env"
   ```

### Step 2: Deploy New SECRET_KEY

**Option A: Automated Deployment (Recommended)**

```bash
# Copy deployment script to production server
scp /opt/sila-system/scripts/deploy_secret_key_production.sh user@production-server:/tmp/

# Execute deployment script
ssh user@production-server "sudo /tmp/deploy_secret_key_production.sh"
```

**Option B: Manual Deployment**

```bash
# SSH to production server
ssh user@production-server

# Navigate to backend directory
cd /opt/sila-system/backend

# Create backup
sudo cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Update SECRET_KEY
sudo sed -i 's/SECRET_KEY=.*/SECRET_KEY=qybuOyGqalIyHENeMQlxzKeBr_kOrHq5Rmd9brCCgYD6-Wxh1vGLvtG9sF_4-t2pemR_DAk75c7WfZyHNUCDgQ/' .env

# Verify the change
grep "SECRET_KEY=" .env
```

### Step 3: Restart Services

**For Systemd Services**:

```bash
sudo systemctl restart sila-backend
sudo systemctl restart prometheus
sudo systemctl restart grafana
```

**For Docker Compose**:

```bash
cd /opt/sila-system/monitoring
sudo docker-compose -f docker-compose.monitoring.yml restart
```

### Step 4: Post-Deployment Validation

1. **Check Service Status**:

   ```bash
   sudo systemctl status sila-backend --no-pager
   sudo systemctl status prometheus --no-pager
   sudo systemctl status grafana --no-pager
   ```

2. **Test Application Health**:

   ```bash
   curl -f http://localhost:8000/monitoring/health/
   ```

3. **Test Prometheus Metrics**:

   ```bash
   curl -f http://localhost:9090/-/healthy
   curl -f http://localhost:9090/api/v1/query?query=up
   ```

4. **Verify Authentication**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"test","password":"test"}'
   ```

## Monitoring and Alerting

### Immediate Monitoring (First 30 minutes)

- Monitor application logs: `tail -f /opt/sila-system/backend/app.log`
- Monitor system resources: `htop` or `top`
- Monitor service status: `sudo systemctl status sila-backend --no-pager`

### 24-Hour Monitoring Plan

1. **Hourly Checks** (First 4 hours):

   - Service availability
   - Error rates in logs
   - Response times

2. **Every 4 Hours** (Next 20 hours):

   - Application performance metrics
   - Database connection status
   - Backup job status

3. **Alert Thresholds to Monitor**:
   - Error rate > 1%
   - Response time > 2 seconds
   - CPU usage > 80%
   - Memory usage > 85%

## Rollback Procedure

If issues are detected, rollback immediately:

```bash
# SSH to production server
ssh user@production-server

# Navigate to backend directory
cd /opt/sila-system/backend

# Restore from backup
sudo cp .env.backup.LATEST .env

# Restart services
sudo systemctl restart sila-backend
sudo systemctl restart prometheus
sudo systemctl restart grafana

# Verify rollback
grep "SECRET_KEY=" .env
```

## Emergency Contacts

- **System Administrator**: [admin@sila-system.com]
- **Development Team**: [dev-team@sila-system.com]
- **On-call Engineer**: [oncall@sila-system.com]

## Documentation Updates

After successful deployment:

1. Update system documentation with new SECRET_KEY deployment date
2. Update security audit logs
3. Archive old SECRET_KEY in secure location
4. Update monitoring dashboards if needed

## Security Considerations

- The new SECRET_KEY is cryptographically secure (64 characters)
- Previous SECRET_KEY is backed up but should be archived securely
- Monitor for any authentication anomalies after deployment
- Consider implementing SECRET_KEY rotation every 90 days

## Next Scheduled Rotation

- **Next Rotation Date**: $(date -d '+90 days' +%Y-%m-%d)
- **Responsible Team**: Security Team
- **Notification**: 7 days before rotation date

---

_This deployment was completed on $(date) by the SILA System Administration Team_
