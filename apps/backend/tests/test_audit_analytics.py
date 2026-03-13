import asyncio
from datetime import datetime
import pytest
from app.core.db import AsyncSessionLocal
from app.core.audit.analytics import AuditAnalytics
from app.core.audit import audit_log

@pytest.mark.asyncio
async def test_audit_analytics():
    print("\n[ANALYTICS] Starting test...")
    
    start_time = datetime.utcnow()
    
    async with AsyncSessionLocal() as session:
        analytics = AuditAnalytics(session)
        
        # 1. Gerar dados de teste (Simular fluxo)
        # Request Created
        req_id = "req-analytics-001"
        await audit_log("REQUEST_CREATED", resource_id=req_id, db=session)
        
        # Simulate processing time
        await asyncio.sleep(0.1) 
        
        # Document Issued
        await audit_log("DOCUMENT_ISSUED", resource_id="doc-analytics-001", new_value={"request_id": req_id}, db=session)
        
        # Anomaly simulation
        for i in range(15):
            await audit_log("FILE_DELETED", resource_id=f"file-{i}", db=session)
            
        await session.commit()
    
    # 2. Test SLA Metrics
    async with AsyncSessionLocal() as session:
        analytics = AuditAnalytics(session)
        metrics = await analytics.get_sla_metrics(start_time, datetime.utcnow())
        
        print(f"[METRICS] {metrics}")
        assert metrics["total_processed"] >= 1
        assert metrics["avg_issuance_time_seconds"] > 0
        
    # 3. Test Anomaly Detection
    async with AsyncSessionLocal() as session:
        analytics = AuditAnalytics(session)
        anomalies = await analytics.detect_anomalies(lookback_minutes=5, threshold=10)
        
        print(f"[ANOMALIES] {anomalies}")
        # Deve detectar FILE_DELETED
        found = False
        for a in anomalies:
            if a["action"] == "FILE_DELETED":
                found = True
                assert a["severity"] == "MEDIUM" or a["severity"] == "HIGH"
        
        assert found, "Anomaly FILE_DELETED not detected"

    print("✨ AuditAnalytics Validated Successfully!")

if __name__ == "__main__":
    asyncio.run(test_audit_analytics())
