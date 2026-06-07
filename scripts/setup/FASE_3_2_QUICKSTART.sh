#!/usr/bin/env bash
# FASE 3.2 - Quick Start Guide for Search & Matching Engine

set -e

echo "================================"
echo "FASE 3.2 Quick Start"
echo "Search Engine + Matching Engine"
echo "================================"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Database Migration
echo -e "${BLUE}Step 1: Running database migration...${NC}"
cd apps/backend
alembic upgrade head
echo -e "${GREEN}✓ Database migration complete${NC}"
echo ""

# 2. Populate test data (if needed)
echo -e "${BLUE}Step 2: Creating sample institution data...${NC}"
python << 'EOF'
import asyncio
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.session import AsyncSessionLocal
from app.modules.educacao.infrastructure.models.institution_marketplace_projection_model import InstitutionMarketplaceProjectionModel

async def populate_sample_data():
    async with AsyncSessionLocal() as session:
        # Sample institution
        institution = InstitutionMarketplaceProjectionModel(
            institution_id=uuid.uuid4(),
            name="Liceu 1 de Agosto",
            type="publica",
            description="Liceu histórico no centro de Luanda",
            province="Luanda",
            municipality="Luanda",
            district="Maianga",
            rating=4.5,
            review_count=128,
            available_slots=45,
            total_capacity=500,
            occupancy_rate=0.91,
            monthly_fee_min=0.0,
            monthly_fee_max=0.0,
            monthly_fee_avg=0.0,
            approval_rate=0.92,
            transfer_acceptance_rate=0.85,
            retention_rate=0.88,
            average_academic_performance=78.0,
            student_satisfaction=4.3,
            specializations=["geral", "tecnico"],
            teaching_modalities=["presencial"],
            educational_levels=["secundario_1", "secundario_2"],
            supports_special_needs=True,
            special_needs_types=["dyslexia", "visual_impairment"],
            accreditation_status="accredited",
            quality_index=85.0,
            is_active=True,
        )
        
        session.add(institution)
        await session.commit()
        print("✓ Sample institution created")

asyncio.run(populate_sample_data())
EOF
echo -e "${GREEN}✓ Sample data created${NC}"
echo ""

# 3. Start the server
echo -e "${BLUE}Step 3: Starting the server...${NC}"
echo -e "${YELLOW}Run this command in a separate terminal:${NC}"
echo ""
echo "    cd apps/backend"
echo "    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""

# 4. Test the endpoints
echo -e "${BLUE}Step 4: Testing the endpoints...${NC}"
echo ""
echo -e "${YELLOW}Test Search Endpoint:${NC}"
echo "    curl 'http://localhost:8000/educacao/marketplace/search?q=liceu&page=1&page_size=20'"
echo ""

echo -e "${YELLOW}Test Matching Endpoint:${NC}"
echo "    curl -X POST http://localhost:8000/marketplace/matching/find-matches \\"
echo "      -H 'Content-Type: application/json' \\"
echo "      -d '{
        \"student_id\": \"STU-001\",
        \"age\": 16,
        \"academic_performance\": 75.5,
        \"special_needs\": [],
        \"location\": {
          \"province\": \"Luanda\",
          \"municipality\": \"Luanda\",
          \"district\": \"Maianga\"
        },
        \"available_budget\": 30000,
        \"preferred_modalities\": [\"presencial\"],
        \"educational_level\": \"secundario\",
        \"previous_transfers\": 0
      }'"
echo ""

echo -e "${BLUE}Step 5: View documentation${NC}"
echo "    cat docs/FASE_3_2_SEARCH_MATCHING_IMPLEMENTATION.md"
echo ""

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Start the server (in separate terminal)"
echo "  2. Test the endpoints with curl or Postman"
echo "  3. Review the documentation for advanced usage"
echo "  4. Integrate into your application"
echo ""
