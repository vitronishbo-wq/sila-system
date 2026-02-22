#!/bin/bash
# Gera changelog automático entre os dois últimos commits

git log -2 --pretty=format:"%h %s" > last_commits.txt
LAST_COMMIT=$(head -n1 last_commits.txt | awk '{print $1}')
PREV_COMMIT=$(tail -n1 last_commits.txt | awk '{print $1}')

git diff --name-status $PREV_COMMIT $LAST_COMMIT > changelog.txt

echo "Changelog gerado em changelog.txt"
