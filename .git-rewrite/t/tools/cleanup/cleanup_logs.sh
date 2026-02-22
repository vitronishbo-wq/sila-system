#!/bin/bash

# Cleanup old log files

# Ensure the script stops on errors
set -e

LOG_DIR="/var/log"
LOG_RETENTION_DAYS=30

echo "Cleaning up log files older than $LOG_RETENTION_DAYS days in $LOG_DIR..."

find "$LOG_DIR" -type f -name '*.log' -mtime +$LOG_RETENTION_DAYS -exec rm -f {} \;

echo "Old log files cleaned up."
