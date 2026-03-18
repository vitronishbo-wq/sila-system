#!/bin/bash

# Monitor database migration progress

# Ensure the script stops on errors
set -e

# Check migration logs
LOG_FILE="/var/log/migration.log"

echo "Monitoring migration progress..."

tail -f "$LOG_FILE"
