#!/bin/bash

# Cleanup temporary files

# Ensure the script stops on errors
set -e

TEMP_DIR="/tmp"

echo "Cleaning up temporary files in $TEMP_DIR..."

rm -rf "$TEMP_DIR"/*

echo "Temporary files cleaned up."
