#!/usr/bin/env bash
#set -euo pipefail
BRANCH=${1:-feature/admin-bootstrap}

echo "This script prepares a branch and commits the admin automation changes."

echo "Run the following commands in your repo to create the branch and commit:"

echo "git checkout -b $BRANCH"
echo "git add scripts/auto_create_admin.sh scripts/force_delete_users.py scripts/list_users.py scripts/AUTO_CREATE_ADMIN.md Makefile"
echo "git commit -m 'feat(admin): add automation for admin bootstrap and docs'"
echo "git push -u origin $BRANCH"
