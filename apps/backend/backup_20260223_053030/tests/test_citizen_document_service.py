import asyncio
import uuid
from datetime import datetime
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
import app.db.base

from app.citizen.core.services.document_service import CitizenDocumentService
from app.citizen.core.services.request_service import RequestService
from app.citizen.core.models import CitizenFUC
from app.core.workflow.models.request import Request
from app.core.constants import EntityStatus
from app.modules.identidade_civil.domain.models.document import Document

async def test_document_issuance_flow():
    """
    Teste de integração do CitizenDocumentService
    """
    print("\n[DOC SERVICE TEST] Iniciando teste de emissão...")
    
    citizen_id = uuid.uuid4()
    request_id = uuid.uuid4()
    
    async with AsyncSessionLocal() as session:
        # 1. Setup: Cidadão
        citizen = CitizenFUC(
            citizen_id=citizen_id,
            full_name="Document Service Tester",
            is_active=True
        )
        session.add(citizen)
        
        # 2. Setup: Pedido (PROCESSAMENTO - estado válido para emissão)
        request = Request(
            id=request_id,
            citizen_id=citizen_id,
            service_code="CERTIDAO_NASCIMENTO",
            status=EntityStatus.PROCESSING.value,
            created_at=datetime.utcnow()
        )
        session.add(request)
        await session.commit()

    async with AsyncSessionLocal() as session:
        # 3. Teste: Emitir Documento
        doc_svc = CitizenDocumentService(session)
        
        print("[DOC SERVICE TEST] Emitindo documento...")
        doc_file = await doc_svc.issue_document_from_request(request_id)
        
        assert doc_file is not None
        assert doc_file.owner_type == "document"
        print(f"✅ Ficheiro criado: {doc_file.file_name} (ID: {doc_file.id})")
        
        # 4. Verificar Registo de Documento Oficial
        doc_record = await session.execute(
            select(Document).where(Document.citizen_id == citizen_id)
        )
        doc = doc_record.scalars().first()
        
        assert doc is not None
        assert doc.status == EntityStatus.APPROVED.value
        assert doc.document_type == "CERTIDAO_NASCIMENTO"
        assert doc.document_number is not None
        print(f"✅ Registo Oficial criado: {doc.document_number}")
        
        # 5. Verificar owner_id do ficheiro bate com o Document ID
        assert doc_file.owner_id == doc.id
        print("✅ Link entre Ficheiro e Registo Oficial validado.")
        
        # 6. Testar Listagem
        docs = await doc_svc.get_citizen_documents(citizen_id)
        assert len(docs) >= 1
        print(f"✅ Listagem retornou {len(docs)} documentos.")

    print("\n✨ CitizenDocumentService Validado com Sucesso!")

if __name__ == "__main__":
    asyncio.run(test_document_issuance_flow())
