#!/bin/bash
set -e
cd /home/dev03wsl/sila-system
eval "$(./scripts/dev/load_runtime_env.sh host)"
export PYTHONPATH=/home/dev03wsl/sila-system/apps/backend
setsid .venv/bin/uvicorn apps.backend.app.main:app --host 0.0.0.0 --port 8000 --log-level warning > /tmp/uvicorn_final.log 2>&1 &
echo "PID=$!"
sleep 15
curl -s http://localhost:8000/api/health
echo ""
echo "BACKEND_READY"
