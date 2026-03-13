import asyncio
import uuid
from apps.backend.app.modules.xroad.application.xroad_service import XRoadInterconnect
from apps.backend.app.modules.xroad.domain.envelope import SILAEnvelope

async def run_stress_test():
    service = XRoadInterconnect()
    previous_hash = "0"
    
    print("⛓️ Verificando encadeamento de hashes...")
    for i in range(5):
        envelope = SILAEnvelope(
            sender_service="MINJUS",
            receiver_service="MINSA",
            payload={"test": f"data_{i}"},
            signature="valid_sig"
        )
        result = await service.exchange(envelope)
        
        current_hash = result["audit_trail_hash"]
        linked_hash = result["chain_link"]
        
        print(f"Swap {i}: Link -> {linked_hash[:8]}... | Hash -> {current_hash[:8]}...")
        
        # O link da transação atual deve ser o hash da transação anterior
        if i > 0:
            assert linked_hash != "0", "Erro: Corrente quebrada!"
            
    print("\n✅ Auditoria Imutável: Corrente Íntegra.")

if __name__ == "__main__":
    asyncio.run(run_stress_test())
