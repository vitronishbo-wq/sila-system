#!/bin/bash
# Seed data script for Health module

cd "$(dirname "$0")/../.." || exit 1

echo "🌱 Executando seed de health_services..."
python -m modules.health.seed_data

echo "✅ Seed concluído!"
