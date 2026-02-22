# SILA System Production Deployment Guide - SECRET_KEY Update

## Overview

This guide provides instructions for updating the SECRET_KEY in the production
environment and restarting services to apply the changes.

## Prerequisites

- SSH access to production server
- sudo privileges on production server
- Backup of current .env file (automatically created)

## Step 1: Backup Current Environment

A backup of your current .env file has already been created:

```bash
ls -la /opt/sila-system/backend/.env.backup.*
```

## Step 2: Generate New SECRET_KEY (if not already done)

If you haven't generated a new SECRET_KEY yet, run:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

## Step 3: Update Production Environment File

SSH into your production server and update the SECRET_KEY:

```bash
# Navigate to backend directory
cd /opt/sila-system/backend

# Create backup (if not exists)
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Update SECRET_KEY in .env file
# Replace 'NEW_SECRET_KEY_HERE' with your actual new secret key
sed -i 's/SECRET_KEY=.*/SECRET_KEY=NEW_SECRET_KEY_HERE/' .env
```

## Step 4: Validate Environment File

Ensure the .env file is properly formatted:

```bash
cd /opt/sila-system/backend
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
secret = os.getenv('SECRET_KEY')
print(f'SECRET_KEY length: {len(secret) if secret else 0}')
print(f'SECRET_KEY preview: {secret[:20]}...' if secret else 'SECRET_KEY not found')
"
```

## Step 5: Restart Services

Restart all SILA services to apply the new SECRET_KEY:

### Option A: Using Docker Compose (if using containerized deployment)

```bash
# Navigate to monitoring directory
cd /opt/sila-system/monitoring

# Restart monitoring stack
docker-compose -f docker-compose.monitoring.yml restart

# If using main application containers
cd /opt/sila-system
docker-compose restart  # or your main compose file
```

### Option B: Using Systemd (if using systemd services)

```bash
# Restart SILA backend service
sudo systemctl restart sila-backend

# Restart monitoring services
sudo systemctl restart prometheus
sudo systemctl restart grafana
sudo systemctl restart alertmanager
```

### Option C: Manual Process Restart

```bash
# Kill existing Python processes
pkill -f "uvicorn" || true
pkill -f "python.*main" || true

# Restart backend application
cd /opt/sila-system/backend
source venv/bin/activate  # if using virtual environment
python custom_server.py &  # or your startup command
```

## Step 6: Verify Services Status

Check that all services are running properly:

```bash
# Check application health
curl -f http://localhost:8000/monitoring/health/ || echo "Health check failed"

# Check monitoring services
curl -f http://localhost:9090/-/healthy || echo "Prometheus not healthy"
curl -f http://localhost:3000/api/health || echo "Grafana not healthy"

# Check service processes
docker ps | grep -E "(sila|prometheus|grafana)" || echo "No relevant containers running"
```

## Step 7: Verify SECRET_KEY Application

Test that the new SECRET_KEY is being used:

```bash
# Check application logs for any SECRET_KEY related errors
tail -f /opt/sila-system/backend/app.log | grep -i secret || echo "No SECRET_KEY errors found"

# Test API endpoints that require authentication
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}' || echo "Auth endpoint test completed"
```

## Step 8: Monitor for Issues

Monitor the application and services for the next 15-30 minutes:

```bash
# Monitor application logs
tail -f /opt/sila-system/backend/app.log

# Monitor system resources
htop  # or top

# Monitor service status
watch -n 5 'docker ps | grep -E "(sila|prometheus|grafana)"'
```

## Troubleshooting

### Common Issues:

1. **Service fails to start**

   - Check logs: `journalctl -u sila-backend -f`
   - Verify .env file syntax
   - Check database connectivity

2. **Authentication fails**

   - Verify SECRET_KEY is properly set in .env
   - Check token expiration settings
   - Verify user credentials in database

3. **Monitoring services fail**
   - Check Prometheus targets: http://localhost:9090/targets
   - Verify Grafana datasources
   - Check container logs: `docker logs <container_name>`

### Rollback Procedure:

If issues occur, rollback to previous SECRET_KEY:

```bash
cd /opt/sila-system/backend
cp .env.backup.LATEST .env
# Restart services as in Step 5
```

## Security Notes

- The new SECRET_KEY should be at least 64 characters long and cryptographically secure
- Never commit SECRET_KEY to version control
- Regularly rotate SECRET_KEY (recommended every 90 days)
- Monitor for any suspicious authentication activity after the change

## Next Steps

1. Monitor application performance for 24 hours
2. Verify all scheduled backups are working with new configuration
3. Update monitoring alerts if needed
4. Document the change in your security log
