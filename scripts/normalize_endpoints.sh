#!/bin/bash
###############################################################################
# SILA 3.0 - Configuration Normalization (Phase 18.3)
# Convert Docker DNS names to localhost endpoints for bare-metal execution
###############################################################################

set -euo pipefail

cd /home/dev03wsl/sila-system

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔄 SILA 3.0 - Configuration Normalization${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# File 1: prometheus.yml (root)
echo -e "${GREEN}✓${NC} Normalizing prometheus.yml (root)..."
sed -i "s|alertmanager:9093|localhost:9093|g" prometheus.yml
sed -i "s|elasticsearch:9200|localhost:9200|g" prometheus.yml
sed -i "s|alert-handler:8080|localhost:8080|g" prometheus.yml
sed -i "s|logstash:9600|localhost:9600|g" prometheus.yml

# File 2: alertmanager.yml (root)
echo -e "${GREEN}✓${NC} Normalizing alertmanager.yml (root)..."
sed -i "s|http://alert-handler:8080|http://127.0.0.1:8080|g" alertmanager.yml

# File 3: platform/devops/monitoring/prometheus/prometheus.yml
echo -e "${GREEN}✓${NC} Normalizing prometheus.yml (devops)..."
sed -i "s|alertmanager:9093|localhost:9093|g" platform/devops/monitoring/prometheus/prometheus.yml
sed -i "s|node-exporter:9100|localhost:9100|g" platform/devops/monitoring/prometheus/prometheus.yml

# File 4: platform/devops/monitoring/grafana/provisioning/alerting/alertmanager.yml
echo -e "${GREEN}✓${NC} Normalizing alertmanager.yml (devops/grafana)..."
sed -i "s|alertmanager:9093|localhost:9093|g" platform/devops/monitoring/grafana/provisioning/alerting/alertmanager.yml

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ NORMALIZATION COMPLETE${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Verification
echo -e "${BLUE}🔍 VERIFICATION OF ENDPOINTS${NC}"
echo ""
echo "prometheus.yml (root) - alertmanager:"
grep "alertmanager" prometheus.yml | head -2
echo ""
echo "prometheus.yml (root) - alert-handler:"
grep "alert-handler" prometheus.yml | head -2
echo ""
echo "alertmanager.yml (root) - alert-handler:"
grep "alert-handler" alertmanager.yml | head -2
echo ""

echo -e "${GREEN}✅ All endpoints normalized to localhost${NC}"
echo ""
