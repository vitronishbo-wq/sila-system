#!/usr/bin/env bash
set -euo pipefail

HOST=${HOST:-http://localhost:8000}
EMAIL=${EMAIL:-truman0@sila.co.ao}
PASS=${PASS:-Truman1}

# Wait for backend
until curl -sSf "$HOST/docs" >/dev/null; do sleep 1; done

echo "[Smoke] JSON login"
curl -sS -i -X POST "$HOST/auth/login" \
  -H 'Content-Type: application/json' \
  --data '{"email":"'"$EMAIL"'","password":"'"$PASS"'"}'

echo "\n[Smoke] Form login"
curl -sS -i -X POST "$HOST/auth/login" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "email=$EMAIL" \
  --data-urlencode "Truman1*Marcelo1*

echo "\n[Smoke] Querystring login"
curl -sS -i -X POST "$HOST/auth/login?email=$EMAIL&Truman1*Marcelo1*

echo "\n[Smoke] Done"
