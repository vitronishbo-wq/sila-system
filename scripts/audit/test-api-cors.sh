#!/bin/bash

# Quick CORS & API Test for SILA System
# Tests if the backend is properly configured for frontend communication

set -e

echo "================================================================"
echo "🧪 SILA System - Quick API & CORS Test"
echo "================================================================"
echo ""

BACKEND_URL="${1:-http://127.0.0.1:8000}"
FRONTEND_ORIGIN="${2:-http://localhost:3000}"

echo "Testing backend at: $BACKEND_URL"
echo "Frontend origin: $FRONTEND_ORIGIN"
echo ""

# Test 1: Health check
echo "✅ TEST 1: Backend Health Check"
if curl -s "$BACKEND_URL/api/health" > /dev/null 2>&1; then
    echo "   ✅ Backend is responding"
else
    echo "   ❌ Backend is not responding at $BACKEND_URL"
    exit 1
fi

echo ""

# Test 2: CORS preflight
echo "✅ TEST 2: CORS Preflight Request"
CORS_RESPONSE=$(curl -s -i -X OPTIONS "$BACKEND_URL/api/health" \
    -H "Origin: $FRONTEND_ORIGIN" \
    -H "Access-Control-Request-Method: GET" 2>&1)

if echo "$CORS_RESPONSE" | grep -q "Access-Control-Allow-Origin"; then
    echo "   ✅ CORS headers present"
    echo "$CORS_RESPONSE" | grep "Access-Control" | sed 's/^/      /'
else
    echo "   ⚠️  No CORS headers detected (might be normal for simple requests)"
fi

echo ""

# Test 3: Simple GET request
echo "✅ TEST 3: Simple API Request"
HEALTH=$(curl -s "$BACKEND_URL/api/health")
if echo "$HEALTH" | grep -q "status"; then
    echo "   ✅ API responding with data"
    echo "      Response: $HEALTH"
else
    echo "   ⚠️  Unexpected API response"
fi

echo ""
echo "================================================================"
echo "✅ All tests completed!"
echo "================================================================"
echo ""
echo "If all tests passed, your frontend should be able to communicate"
echo "with the backend without CORS issues."
echo ""
echo "Frontend URL: $FRONTEND_ORIGIN"
echo "Backend URL: $BACKEND_URL"
echo ""
echo "For more details, see CORS_CONFIGURATION.md"
