# 🏗️ Integration Validator - Arquitetura & Fluxo

## 📊 Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────┐
│         Integration Validator Framework                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐     ┌────────────┐  │
│  │  Config      │      │  Endpoints   │     │   Auth     │  │
│  │  (YAML)      │      │  (YAML)      │     │  (Script)  │  │
│  └──────┬───────┘      └──────┬───────┘     └────┬───────┘  │
│         │                     │                   │          │
│         └─────────────────────┼───────────────────┘          │
│                               ▼                              │
│         ┌─────────────────────────────────────┐              │
│         │  validate_frontend_backend_          │              │
│         │  integration.py (1,007 lines)        │              │
│         ├─────────────────────────────────────┤              │
│         │  • CircuitManager                    │              │
│         │  • RetryLogic                        │              │
│         │  • ParallelExecutor                  │              │
│         │  • CORSValidator                     │              │
│         │  • AuthInjector                      │              │
│         │  • LatencyAnalyzer                   │              │
│         │  • ReportGenerator                   │              │
│         └────────────┬────────────────────────┘              │
│                      │                                        │
│  ┌───────┬──────────┼──────────┬───────┬────────────┐       │
│  ▼       ▼          ▼          ▼       ▼            ▼       │
│ JSON   Markdown    HTML      Plots  STDOUT     Exit Code    │
│Report  Report     Report   (chart)  (logs)     (CI/CD)      │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Fluxo de Execução

```
START
  │
  ├─> Load Configuration (context.yaml)
  ├─> Load Endpoints (endpoints.yaml)
  ├─> Get Auth Token (script ou static)
  │
  ├─> FOR EACH Endpoint (Parallel)
  │   │
  │   ├─> Check Circuit Breaker
  │   │   ├─ If TRIPPED? → SKIP (record as WARN)
  │   │   └─ If OK? → Continue
  │   │
  │   ├─> Attempt Request (max 3 retries)
  │   │   │
  │   │   ├─> Build Request
  │   │   │   ├─ URL: base_url + endpoint.url
  │   │   │   ├─ Method: GET/POST/OPTIONS
  │   │   │   ├─ Headers: Auth token, CORS headers
  │   │   │   ├─ Body: endpoint.body (if POST)
  │   │   │   └─ Timeout: endpoint.timeout (default 8s)
  │   │   │
  │   │   ├─> Send Request (with timeout)
  │   │   │
  │   │   ├─> Check Response
  │   │   │   ├─ Status Code Match? (expect_status)
  │   │   │   ├─ Latency < Threshold?
  │   │   │   └─ Auth working (if required)?
  │   │   │
  │   │   ├─> Success?
  │   │   │   ├─ YES → Record PASS, Reset circuit, Return
  │   │   │   └─ NO → Increment attempt counter
  │   │   │
  │   │   ├─> Max Retries Exceeded?
  │   │   │   ├─ NO → Sleep (backoff), Try again
  │   │   │   └─ YES → Record FAIL, Trip circuit, Return
  │   │
  │   ├─> For CORS Preflight (OPTIONS endpoint)
  │   │   └─> Check headers:
  │   │       ├─ Access-Control-Allow-Origin
  │   │       ├─ Access-Control-Allow-Methods
  │   │       ├─ Access-Control-Allow-Headers
  │   │       └─ Access-Control-Max-Age
  │
  ├─> Analyze Results
  │   ├─ Count: PASS / FAIL / WARN / SKIP
  │   ├─ Calculate latency: P50, P95, P99
  │   ├─ Detect bottlenecks (slow endpoints)
  │   ├─ Circuit breaker status
  │   └─ Total duration
  │
  ├─> Generate Reports
  │   ├─> JSON Report (structured data)
  │   ├─> Markdown Report (human readable)
  │   ├─> HTML Report (visual with tables)
  │   ├─> Matplotlib Plots (latency chart)
  │   └─> STDOUT Log (console output)
  │
  ├─> Determine Exit Code
  │   ├─ If critical_failed > 0? → Exit 2 (FAIL)
  │   ├─ If any_failed > 0? → Exit 1 (WARN)
  │   └─ If all passed? → Exit 0 (OK)
  │
  └─> END
```

## 🔌 Ciclo de Retry com Backoff

```
Request to /api/auth/login
    │
    ├─→ Attempt 1: Send immediately
    │       │
    │       ├─→ HTTP 500? → FAIL
    │       │
    │       └─→ Sleep: 0.5s (BACKOFF_FACTOR * 2^(1-1)) + jitter
    │
    ├─→ Attempt 2: Send after 0.5s
    │       │
    │       ├─→ HTTP 500? → FAIL
    │       │
    │       └─→ Sleep: 1.0s (BACKOFF_FACTOR * 2^(2-1)) + jitter
    │
    ├─→ Attempt 3: Send after 1.0s
    │       │
    │       ├─→ HTTP 500? → FAIL
    │       │
    │       └─→ Check max_retries
    │
    ├─→ Max retries exceeded?
    │       │
    │       ├─→ YES: Record FAIL, Trip circuit (record_failure)
    │       │
    │       └─→ NO: Continue to next attempt (max backoff 10s)
    │
    └─→ Success (HTTP 200)? → Record PASS, Reset circuit
```

## 🔴 Circuit Breaker Pattern

```
Normal State
    │
    ├─→ Request to endpoint
    │   │
    │   ├─→ Success? → Count: 0
    │   │
    │   └─→ Failure? → Count: 1
    │
    └─→ Count < 3?
        ├─→ YES → Continue to NORMAL
        └─→ NO → TRIP CIRCUIT

Tripped State (30s lockout)
    │
    ├─→ Block all requests
    ├─→ Record: WARN (skipped due to circuit trip)
    ├─→ Wait 30 seconds
    │
    └─→ 30s elapsed?
        ├─→ YES → Reset failures, back to NORMAL
        └─→ NO → Continue TRIPPED

Timeline:
    0s   ├─ Failure 1 (count: 1)
    0.1s ├─ Failure 2 (count: 2)
    0.2s ├─ Failure 3 (count: 3) → CIRCUIT TRIPS
    0.2s ├─ Future requests: SKIP (circuit tripped)
    30s  ├─ 30s elapsed → Reset (count: 0)
    30s  └─ Resume requests
```

## 🔐 Auth Token Injection Flow

### Option 1: Static Token

```
Config:
    auth:
        method: "static"
        token: "eyJ0eXAi..."
    │
    ├─> Load token from config
    ├─> Inject in Authorization header
    │   └─> "Authorization: Bearer eyJ0eXAi..."
    │
    └─> Use for all endpoints
```

### Option 2: Dynamic Token (Command)

```
Config:
    auth:
        method: "command"
        command: "./scripts/get_dev_token.sh"
    │
    ├─> Execute command: ./scripts/get_dev_token.sh
    │   │
    │   ├─> Script logs in: POST /api/auth/login
    │   │   └─> {"username": "...", "password": "..."}
    │   │
    │   ├─> Backend returns: {"access_token": "eyJ0eXAi..."}
    │   │
    │   └─> Script extracts token and outputs
    │
    ├─> Capture token from stdout
    ├─> Mask token in logs: "Bearer ***MASKED***"
    ├─> Inject in Authorization header
    │   └─> "Authorization: Bearer eyJ0eXAi..."
    │
    └─> Use for authenticated endpoints
```

## 🌐 CORS Validation Flow

```
FOR EACH endpoint with CORS:
    │
    ├─> Build CORS Preflight Request
    │   │
    │   ├─ Method: OPTIONS
    │   ├─ Headers:
    │   │   ├─ Origin: http://localhost:5173
    │   │   ├─ Access-Control-Request-Method: GET/POST/etc
    │   │   └─ Access-Control-Request-Headers: Content-Type, Authorization
    │   │
    │   └─> Send to endpoint
    │
    ├─> Check Response
    │   │
    │   ├─ Status 2xx?
    │   │   └─> Check headers:
    │   │       ├─ Access-Control-Allow-Origin: * or specific origin ✓
    │   │       ├─ Access-Control-Allow-Methods: includes GET, POST ✓
    │   │       ├─ Access-Control-Allow-Headers: includes Content-Type, Auth ✓
    │   │       └─ Access-Control-Max-Age: set (e.g., 86400) ✓
    │   │
    │   └─ Status 4xx/5xx?
    │       └─> FAIL: CORS not configured
    │
    └─> Record: PASS (CORS OK) or FAIL (CORS error)
```

## 📊 Latency Analysis

```
Collect all latencies:
    [12.5ms, 34.2ms, 45.1ms, 89.5ms, 145.3ms, 230.1ms, ...]
    │
    ├─> Sort: [12.5, 34.2, 45.1, 89.5, 145.3, 230.1, ...]
    │
    ├─> Calculate P50 (50th percentile)
    │   │
    │   ├─ Index: 50% * length = 50% * 10 = 5
    │   └─ Value: sorted_list[5] = 145.3ms ← MEDIAN
    │
    ├─> Calculate P95 (95th percentile)
    │   │
    │   ├─ Index: 95% * length = 95% * 10 = 9.5
    │   └─ Value: sorted_list[9] = 230.1ms (interpolated)
    │
    ├─> Calculate P99 (99th percentile)
    │   │
    │   ├─ Index: 99% * length = 99% * 10 = 9.9
    │   └─ Value: sorted_list[9] + = 450.5ms (extrapolated)
    │
    ├─> Detect Bottlenecks
    │   │
    │   └─ If P95 > SLA_THRESHOLD (e.g., 250ms)?
    │       ├─> YES: Warn "Performance Bottleneck"
    │       └─> Suggest slowest endpoint
    │
    └─> Generate Chart
        ├─ Endpoints on X-axis
        ├─ Latency on Y-axis
        ├─ Bar chart with colors: green < 100ms, yellow 100-250ms, red > 250ms
        └─ Save as integration_results.png
```

## 📄 Report Generation

```
Results Dict
    {
        "endpoints": [
            {
                "name": "Health Check",
                "status": "PASS",
                "latency_ms": 12.5,
                "http_code": 200,
                ...
            },
            ...
        ],
        "summary": {
            "total": 17,
            "passed": 16,
            "failed": 1,
            ...
        },
        "performance": {
            "p50_latency_ms": 45.2,
            "p95_latency_ms": 230.1,
            ...
        }
    }
    │
    ├─→ write_json_report() → integration_results.json
    │   └─ Serialized dict to JSON (pretty-printed)
    │
    ├─→ write_md_report() → integration_results.md
    │   ├─ Markdown tables
    │   ├─ Inline metrics
    │   ├─ Failure details
    │   └─ Performance summary
    │
    ├─→ write_html_report() → integration_results.html
    │   ├─ HTML page with CSS styling
    │   ├─ Bootstrap tables
    │   ├─ Color-coded status (green/yellow/red)
    │   └─ Responsive design
    │
    ├─→ plot_latency() → integration_results.png
    │   ├─ Matplotlib bar chart
    │   ├─ Color-coded by latency
    │   ├─ Threshold lines (SLA)
    │   └─ Legend and labels
    │
    └─→ STDOUT Log
        ├─ Summary line: "✅ All critical endpoints passed"
        ├─ Detailed logs with timestamps
        └─ Warnings/errors highlighted
```

## 🔄 Parallelization Strategy

```
ThreadPoolExecutor (workers=4)
    │
    ├─→ Task 1: Test /health (thread 1)
    ├─→ Task 2: Test /api/auth/login (thread 2)
    ├─→ Task 3: Test /api/user/me (thread 3)
    ├─→ Task 4: Test /api/items (thread 4)
    │
    └─ Tasks submitted to queue, workers execute in parallel
        │
        ├─→ Worker 1 finishes task 1 → Takes task 5
        ├─→ Worker 2 finishes task 2 → Takes task 6
        ├─→ Worker 3 finishes task 3 → Takes task 7
        └─→ Worker 4 finishes task 4 → Takes task 8

        As-you-go execution = Faster overall time
        (Instead of: tasks 1→2→3→4 sequentially)
```

## 🎯 Exit Code Semantics

```
Script Outcome:
    │
    ├─→ All critical endpoints PASSED
    │   └─> Exit Code: 0 ✅ (CI/CD continues)
    │
    ├─→ Some non-critical failed
    │   └─> Exit Code: 1 ⚠️ (CI/CD warning)
    │
    ├─→ Critical endpoint FAILED
    │   └─> Exit Code: 2 ❌ (CI/CD stops)
    │
    └─→ Exception/Error
        └─> Exit Code: 1 (error)
```

## 🌊 Concurrency Control

```
Request Concurrency:

    Sequential (old):
        Request 1: 100ms
        Request 2: 100ms
        Request 3: 100ms
        Total: 300ms ❌

    Parallel (new):
        Request 1: 100ms ───┐
        Request 2: 100ms ───┤ PARALLEL
        Request 3: 100ms ───┘
        Total: 100ms ✅ (3x faster!)
```

## 📈 Performance Metrics Tracked

```
Per Endpoint:
    ├─ method (GET, POST, OPTIONS)
    ├─ url (full URL)
    ├─ status (PASS, FAIL, WARN, SKIP)
    ├─ http_code (200, 500, etc.)
    ├─ latency_ms (response time)
    ├─ attempts (1-3)
    ├─ error (if failed)
    └─ timestamp (when tested)

Aggregated:
    ├─ total_endpoints (17)
    ├─ passed_count (16)
    ├─ failed_count (1)
    ├─ skipped_count (0)
    ├─ p50_latency_ms (45.2)
    ├─ p95_latency_ms (230.1)
    ├─ p99_latency_ms (450.5)
    ├─ total_duration_ms (2847)
    ├─ circuit_trips (1)
    ├─ total_retries (3)
    └─ critical_failed (0)
```

---

**Diagrama Texto Summary:**

```
CONFIG → ENDPOINTS → AUTH → VALIDATOR → TESTS (Parallel)
                                           ↓
                                    RESULTS ANALYSIS
                                           ↓
                    ┌──────────────────────┼──────────────────────┐
                    ↓                      ↓                      ↓
                  JSON               MARKDOWN                  HTML
              (structured)         (readable)              (visual)
                    │                      │                      │
                    └──────────────────────┼──────────────────────┘
                                           ↓
                                    EXIT CODE + LOGS
```
