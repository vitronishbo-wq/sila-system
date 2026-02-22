#!/bin/bash

# Monitor NGINX server status

# Ensure the script stops on errors
set -e

# Check NGINX status
NGINX_STATUS_CMD="systemctl status nginx"

echo "Checking NGINX server status..."

$NGINX_STATUS_CMD

# Tail NGINX logs
LOG_FILE="/var/log/nginx/access.log"
echo "Tailing NGINX access logs..."

tail -f "$LOG_FILE"
