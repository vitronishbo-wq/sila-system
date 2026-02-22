# SILA System - CI/CD & Deployment Guide

**Last Updated**: 2025-11-25 **Status**: Production Ready **Version**: 1.0

---

## 📋 Quick Start: Deployment Checklist

### Pre-Deployment (Day 0)

```bash
# 1. Environment Verification
[ ] Verify .env.production has correct DATABASE_URL
[ ] Verify .env.production has correct credentials
[ ] Verify LOG_LEVEL is set to INFO (not DEBUG)
[ ] Verify DEBUG is set to False

# 2. Code Verification
[ ] Run full test suite: pytest tests/ -v
[ ] Verify 7/7 payment tests pass
[ ] Run linting: black --check apps/backend/
[ ] Run type checking: mypy apps/backend/ (if configured)

# 3. Database Verification
[ ] Backup current production database
[ ] Run database migrations: alembic upgrade head
[ ] Verify schema integrity: SELECT COUNT(*) FROM information_schema.tables

# 4. Service Health Check
[ ] Verify Redis connection (if used)
[ ] Verify logging system configuration
[ ] Verify monitoring/alerting system
[ ] Test SMTP configuration (if email needed)

# 5. Documentation Verification
[ ] Read QUICK_START_DEV_GUIDE.md
[ ] Review PRODUCTION_READINESS_REPORT.md
[ ] Verify team has access to copilot-instructions.md
```

### Deployment Day (Day 1)

```bash
# 1. Pre-deployment snapshot
[ ] Create database snapshot
[ ] Record current API metrics baseline
[ ] Document current error rate baseline

# 2. Deploy application
[ ] Stop current FastAPI server gracefully
[ ] Deploy new code to server
[ ] Run migrations if needed
[ ] Start new FastAPI server
[ ] Verify server is responding to health checks

# 3. Post-deployment validation
[ ] Run smoke tests (see "Smoke Test Suite" below)
[ ] Monitor error logs for 30 minutes
[ ] Monitor application metrics
[ ] Confirm all endpoints responding correctly

# 4. Communication
[ ] Notify team of successful deployment
[ ] Post update to status page
[ ] Document any issues encountered
```

---

## 🚀 CI/CD Pipeline Setup

### GitHub Actions Configuration

```yaml
# .github/workflows/production-deploy.yml
name: Production Deployment

on:
  push:
    branches: [main]
    paths:
      - 'apps/backend/**'
      - '.github/workflows/production-deploy.yml'

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12.3'

      - name: Install dependencies
        run: |
          pip install -r requirements/backend.txt
          pip install black mypy pytest pytest-asyncio

      - name: Lint code
        run: black --check apps/backend/

      - name: Run tests
        env:
          PYTHONPATH: apps/backend
          DATABASE_URL: sqlite:///:memory:
        run: |
          pytest tests/modules/payment/ -v
          pytest tests/modules/documents/ -v --tb=short

      - name: Build Docker image
        run: docker build -t sila-backend:${{ github.sha }} .

      - name: Push to registry
        run: |
          docker tag sila-backend:${{ github.sha }} sila-backend:latest
          docker push sila-backend:latest

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
          DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
        run: |
          ssh -i $DEPLOY_KEY deploy@$DEPLOY_HOST \
            "cd /app && docker-compose pull && docker-compose up -d"

      - name: Verify deployment
        run: |
          curl -f http://${{ secrets.DEPLOY_HOST }}:8000/health || exit 1
```

### Manual Deployment Steps

```bash
#!/bin/bash
# deploy.sh - Manual production deployment

set -e

PROJECT_ROOT="/app/sila-system"
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🔄 Starting SILA System production deployment..."

# 1. Backup database
echo "💾 Creating database backup..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $BACKUP_DIR/sila_$TIMESTAMP.sql
gzip $BACKUP_DIR/sila_$TIMESTAMP.sql

# 2. Pull latest code
echo "📦 Pulling latest code..."
cd $PROJECT_ROOT
git pull origin main

# 3. Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements/backend.txt

# 4. Run migrations
echo "🔄 Running database migrations..."
export PYTHONPATH=$PROJECT_ROOT/apps/backend
alembic upgrade head

# 5. Run tests
echo "🧪 Running test suite..."
pytest tests/modules/payment/test_service.py -v || exit 1

# 6. Restart service
echo "🚀 Restarting application..."
systemctl restart sila-backend
sleep 5

# 7. Health check
echo "✅ Running health checks..."
curl -f http://localhost:8000/health || {
  echo "❌ Health check failed! Rolling back..."
  git revert HEAD --no-edit
  systemctl restart sila-backend
  exit 1
}

echo "✅ Deployment successful!"
```

---

## 🧪 Smoke Test Suite

### Manual Testing

```bash
#!/bin/bash
# smoke_tests.sh

API_URL="${1:-http://localhost:8000}"
PASSED=0
FAILED=0

test_endpoint() {
  local method=$1
  local endpoint=$2
  local expected=$3

  echo -n "Testing $method $endpoint... "

  response=$(curl -s -w "\n%{http_code}" -X $method $API_URL$endpoint)
  status=$(echo "$response" | tail -n1)
  body=$(echo "$response" | head -n-1)

  if [[ $status == $expected ]]; then
    echo "✅ PASS ($status)"
    ((PASSED++))
  else
    echo "❌ FAIL (got $status, expected $expected)"
    echo "Response: $body"
    ((FAILED++))
  fi
}

# Test core endpoints
test_endpoint "GET" "/health" "200"
test_endpoint "GET" "/docs" "200"
test_endpoint "GET" "/redoc" "200"

# Payment endpoints
test_endpoint "GET" "/payments/ping" "200"

# Documents endpoints
test_endpoint "GET" "/documents/ping" "200"

# Location endpoints
test_endpoint "GET" "/location/provinces" "200"

echo ""
echo "Summary: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ]
```

### Automated Performance Testing

```python
# tests/performance/load_test.py

import requests
import time
from concurrent.futures import ThreadPoolExecutor
import statistics

def test_payment_creation():
    """Test payment creation performance"""
    BASE_URL = "http://localhost:8000"

    payload = {
        "amount": 100.0,
        "method": "BNA",
        "currency": "AOA"
    }

    times = []
    errors = 0

    def make_request():
        try:
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/payments",
                json=payload,
                timeout=10
            )
            elapsed = time.time() - start

            if response.status_code in [200, 201]:
                return elapsed
            else:
                return None
        except Exception as e:
            return None

    # Run 100 requests concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: make_request(), range(100)))

    valid_times = [t for t in results if t is not None]
    errors = len(results) - len(valid_times)

    print(f"\nPerformance Test Results:")
    print(f"Requests: 100")
    print(f"Successful: {len(valid_times)}")
    print(f"Failed: {errors}")
    print(f"Average Response Time: {statistics.mean(valid_times):.3f}s")
    print(f"Median Response Time: {statistics.median(valid_times):.3f}s")
    print(f"P95 Response Time: {statistics.quantiles(valid_times, n=20)[18]:.3f}s")

    # Assert performance
    assert statistics.mean(valid_times) < 1.0, "Average response time too high"
    assert errors == 0, "Some requests failed"
    print("\n✅ Performance test PASSED")

if __name__ == "__main__":
    test_payment_creation()
```

---

## 📊 Monitoring & Logging Setup

### Logging Configuration

```python
# apps/backend/core/logging.py

import logging
import logging.handlers
from pythonjsonlogger import jsonlogger

def setup_logging(environment: str = "production"):
    """Configure structured logging for production"""

    logger = logging.getLogger()
    logger.setLevel(logging.INFO if environment == "production" else logging.DEBUG)

    # JSON formatter for structured logging
    json_formatter = jsonlogger.JsonFormatter()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # File handler (rotate daily)
    file_handler = logging.handlers.RotatingFileHandler(
        filename='logs/sila.log',
        maxBytes=10485760,  # 10MB
        backupCount=30      # Keep 30 days
    )
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)

    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        filename='logs/sila_errors.log',
        maxBytes=10485760,
        backupCount=30,
        level=logging.ERROR
    )
    error_handler.setFormatter(json_formatter)
    logger.addHandler(error_handler)

    return logger

# Usage in FastAPI
from fastapi import FastAPI

app = FastAPI()
logger = setup_logging(os.getenv("ENVIRONMENT", "production"))

@app.middleware("http")
async def log_requests(request, call_next):
    """Log all HTTP requests"""
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    logger.info(
        f"Request: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration * 1000
        }
    )

    return response
```

### Prometheus Metrics

```python
# apps/backend/core/metrics.py

from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Payment metrics
payment_processed = Counter(
    'payments_processed_total',
    'Total payments processed',
    ['status']
)

# Database metrics
db_connections = Gauge(
    'db_connections_active',
    'Active database connections'
)

def track_request(method, endpoint, status, duration):
    """Track HTTP request metrics"""
    request_count.labels(method=method, endpoint=endpoint, status=status).inc()
    request_duration.labels(method=method, endpoint=endpoint).observe(duration)

def track_payment(status):
    """Track payment processing"""
    payment_processed.labels(status=status).inc()
```

---

## 🚨 Alerting Rules

### Alert Configuration (Prometheus)

```yaml
# monitoring/alerts.yml

groups:
  - name: sila_system_alerts
    rules:
      # Payment processing failures
      - alert: PaymentProcessingFailures
        expr: rate(payments_processed_total{status="FAILED"}[5m]) > 0.1
        for: 5m
        annotations:
          summary: "High payment failure rate"

      # API errors
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High API error rate"

      # Database connectivity
      - alert: DatabaseConnectionError
        expr: db_connections_active == 0
        for: 1m
        annotations:
          summary: "No active database connections"

      # Response time degradation
      - alert: SlowResponses
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
        for: 10m
        annotations:
          summary: "API response times degraded"
```

---

## 📈 Rollback Procedure

### Automatic Rollback

```bash
#!/bin/bash
# rollback.sh

BACKUP_DIR="/backups"
LATEST_BACKUP=$(ls -t $BACKUP_DIR/*.sql.gz | head -1)

echo "🔄 Rolling back to previous deployment..."

# 1. Stop application
systemctl stop sila-backend

# 2. Restore database
echo "Restoring database from $LATEST_BACKUP..."
gunzip -c $LATEST_BACKUP | psql -h $DB_HOST -U $DB_USER -d $DB_NAME

# 3. Revert code
cd /app/sila-system
git revert HEAD --no-edit

# 4. Restart application
systemctl start sila-backend

# 5. Verify
sleep 5
curl -f http://localhost:8000/health || {
  echo "❌ Rollback failed!"
  exit 1
}

echo "✅ Rollback completed successfully"
```

---

## 📋 Module Deployment Checklist

Use this before deploying ANY new module:

```markdown
## Pre-Deployment Validation

- [ ] **Code Quality**

  - [ ] All imports are absolute (no relative imports)
  - [ ] All type hints present
  - [ ] Docstrings on public methods
  - [ ] No print() statements (use logging)
  - [ ] All functions properly async where needed

- [ ] **Database**

  - [ ] Table names follow {module}\_{entity} pattern
  - [ ] Foreign keys use full table names with module prefix
  - [ ] All relationships use back_populates
  - [ ] Migrations created and tested

- [ ] **Pydantic Schemas**

  - [ ] Response schemas have from_attributes=True
  - [ ] Optional fields use Optional[Type] = None
  - [ ] Field validators for complex validation
  - [ ] ConfigDict properly configured

- [ ] **Testing**

  - [ ] Unit tests written for all service methods
  - [ ] Tests use central conftest.py
  - [ ] All tests pass: pytest tests/modules/[module]/ -v
  - [ ] Test coverage >= 80%

- [ ] **Error Handling**

  - [ ] Service methods raise ValueError for validation errors
  - [ ] Endpoints map errors to appropriate HTTP codes
  - [ ] Error messages are descriptive
  - [ ] Logging included in critical paths

- [ ] **API Endpoints**

  - [ ] All routes return proper status codes
  - [ ] Request/response models documented
  - [ ] CORS properly configured
  - [ ] Rate limiting applied where needed

- [ ] **Documentation**

  - [ ] README.md with setup instructions
  - [ ] API endpoint documentation
  - [ ] Code examples provided
  - [ ] Architecture diagram included

- [ ] **Performance**

  - [ ] Database queries indexed appropriately
  - [ ] No N+1 query problems
  - [ ] Response times acceptable
  - [ ] Memory usage reasonable

- [ ] **Security**

  - [ ] Input validation via Pydantic
  - [ ] SQL injection prevention (ORM usage)
  - [ ] HTTPS/TLS enabled
  - [ ] Secrets not in code

- [ ] **Monitoring**
  - [ ] Logging configured
  - [ ] Metrics exposed
  - [ ] Health endpoint working
  - [ ] Error alerts configured
```

---

## 📞 Escalation Contacts

| Issue              | Contact        | Phone        | Email               |
| ------------------ | -------------- | ------------ | ------------------- |
| Payment Processing | Payment Team   | xxx-xxx-xxxx | payments@sila.local |
| Database           | DevOps         | xxx-xxx-xxxx | devops@sila.local   |
| API/Performance    | Infrastructure | xxx-xxx-xxxx | infra@sila.local    |
| Security           | Security       | xxx-xxx-xxxx | security@sila.local |
| General            | Team Lead      | xxx-xxx-xxxx | lead@sila.local     |

---

## ✅ Deployment Sign-Off

- [ ] All checklists completed
- [ ] All tests passing
- [ ] Backup created
- [ ] Team notified
- [ ] Monitoring configured
- [ ] Rollback procedure tested

**Deployed By**: ******\_\_\_****** **Date**: ******\_\_\_****** **Approved By**:
******\_\_\_****** **Time Started**: ******\_\_\_****** **Time Completed**:
******\_\_\_******
