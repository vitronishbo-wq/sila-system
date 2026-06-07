Policy registry and management

This folder contains the central `policy_engine` used across the system.

Tools:
- `cli.py` — small CLI to list/get/set policies (uses `policy_engine.update_policy`, which persists to `data/policies.json` by default).
- `tools/policies/scan_hardcoded.py` — conservative scanner that finds candidate hard-coded values for migration and writes `data/policy_scan_report.json`.

Policy semantics:
- `TRANSFER_WINDOWS` may use boolean values or period objects with `enabled`, `start_date`, and `end_date`.
- `GRADE_COMPATIBILITY` now includes series `1` through `12`.

Example period-specific windows:
```json
{
  "TRANSFER_WINDOWS": {
    "default": true,
    "2026": {
      "enabled": true,
      "start_date": "2026-03-01",
      "end_date": "2026-05-31",
      "semesters": {
        "1": {
          "enabled": true,
          "start_date": "2026-03-01",
          "end_date": "2026-04-15"
        },
        "2": {
          "enabled": true,
          "start_date": "2026-09-01",
          "end_date": "2026-10-15"
        }
      },
      "regions": {
        "north": {
          "enabled": true,
          "start_date": "2026-03-01",
          "end_date": "2026-05-31",
          "semesters": {
            "1": {
              "enabled": true,
              "start_date": "2026-03-01",
              "end_date": "2026-04-10"
            }
          }
        },
        "south": {
          "enabled": false,
          "start_date": "2026-03-01",
          "end_date": "2026-05-31"
        }
      }
    },
    "2027": {
      "enabled": true,
      "start_date": "2027-03-01",
      "end_date": "2027-05-31"
    },
    "2028": {
      "enabled": true,
      "start_date": "2028-03-01",
      "end_date": "2028-05-31"
    },
    "2029": {
      "enabled": true,
      "start_date": "2029-03-01",
      "end_date": "2029-05-31"
    },
    "2030": {
      "enabled": true,
      "start_date": "2030-03-01",
      "end_date": "2030-05-31"
    }
  }
}
```

When `context` includes `region` or `semester`, the engine selects the matching inner window before falling back to year-level defaults.

Example of a closed window:
```json
{
  "TRANSFER_WINDOWS": {
    "2031": {
      "enabled": false,
      "start_date": "2031-03-01",
      "end_date": "2031-05-31"
    }
  }
}
```

Quick usages:

List policies:
```
python -m foundation.policies.cli list
```

Set a policy:
```
python -m foundation.policies.cli set MAX_PENDING_DEBT 0
```

Run the scanner:
```
python tools/policies/scan_hardcoded.py
```
