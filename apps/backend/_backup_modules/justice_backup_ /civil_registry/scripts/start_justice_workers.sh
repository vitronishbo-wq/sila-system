#!/bin/bash
set -euo pipefail

echo "Starting Civil Registry Projection Worker"
python workers/civil_registry_projection_worker.py
