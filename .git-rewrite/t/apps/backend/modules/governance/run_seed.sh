#!/bin/bash
# Seed data script for Governance module

cd "$(dirname "$0")/../.." || exit 1

echo "🌱 Executando seed de governance..."
python -m modules.governance.seed_data

echo "✅ Seed concluído!"
