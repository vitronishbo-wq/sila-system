import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.audit import audit_log
from app.core.constants import EntityStatus
from app.citizen.core.services.request_service import RequestService
from app.core.document.services.document_service import DocumentService as CoreDocumentService
from app.core.document.models.document_file import DocumentFile
from app.core.workflow.models.request import Request
from app.citizen.core.models import CitizenFUC
from app.modules.identidade_civil.domain.models.document import Document

class CitizenDocumentService:
    """
    Serviço de Emissão de Documentos do Cidadão (Orquestrador).
    Responsável por validar pedidos e gerar/persistir documentos oficiais.
    """

    def __init__(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db
        self.request_svc = RequestService(db)
        self.core_doc_svc = CoreDocumentService(db)

    async def issue_document_from_request(
        self,
        request_id: uuid.UUID,
        actor_id: str = "SYSTEM"
    ) -> DocumentFile:
        """
        Emite um documento oficial a partir de um pedido (Request) aprovado.
        """
        # 1. Obter e Validar Pedido
        request = await self.request_svc.get_request(request_id)
        if not request:
            raise ValueError(f"Request {request_id} não encontrado.")

        # Validação de Estado
        valid_states = [EntityStatus.PROCESSING.value, EntityStatus.APPROVED.value, "PAID"]
        if request.status not in valid_states:
             if request.status != EntityStatus.PROCESSING.value and request.status != EntityStatus.APPROVED.value:
                raise ValueError(f"Request {request_id} em estado inválido ({request.status}) para emissão de documento.")

        # 2. Validar Cidadão
        citizen = await self.db.get(CitizenFUC, request.citizen_id)
        if not citizen:
            raise ValueError(f"Cidadão {request.citizen_id} não encontrado.")

        # 3. Gerar Conteúdo do Documento (Simulado - PDF/Blob)
        doc_type = request.service_code
        content = f"SILA OFFICIAL DOCUMENT\nType: {doc_type}\nCitizen: {citizen.full_name}\nIssued At: {datetime.utcnow()}".encode('utf-8')
        filename = f"{doc_type}_{request.citizen_id}_{uuid.uuid4().hex[:8]}.txt"

        # 4. Criar Registo de Documento Oficial (Business Entity)
        # Tenta mapear o service_code para um tipo de documento conhecido ou usa 'OTHER'
        # Ex: BI_EMISSAO -> ID_CARD
        document_record = Document(
            id=uuid.uuid4(),
            citizen_id=request.citizen_id,
            service_id=request.service_id,
            document_type=doc_type, # Pode precisar de mapping se usar Enum estrito
            status=EntityStatus.APPROVED.value, # Emitido/Válido
            document_number=f"DOC-{uuid.uuid4().hex[:8].upper()}",
            request_date=request.created_at,
            processing_date=None,
            completion_date=datetime.utcnow(),
            expiry_date=None, # TBD based on rules
            notes=f"Issued from Request {request_id}"
        )
        self.db.add(document_record)
        await self.db.flush()

        # 5. Persistir Ficheiro do Documento (Core Document Service)
        # O dono do ficheiro é o Próprio Documento Oficial (para manter histórico de versões se necessário)
        # ou o Cidadão directamente. Vamos vincular ao Documento para encapsulamento.
        category = "OFFICIAL_DOCUMENT"
        
        doc_file = await self.core_doc_svc.upload_document(
            owner_id=document_record.id, 
            owner_type="document",
            category=category,
            file_name=filename,
            content=content,
            content_type="text/plain",
            meta_data={
                "request_id": str(request_id),
                "service_code": doc_type,
                "citizen_id": str(request.citizen_id),
                "issued_at": datetime.utcnow().isoformat()
            }
        )
        
        # 6. Auditoria e Eventos
        await audit_log(
            action="DOCUMENT_ISSUED",
            actor_id=actor_id,
            resource_id=str(document_record.id),
            resource_type="Document",
            new_value={
                "file_id": str(doc_file.id),
                "document_number": document_record.document_number,
                "request_id": str(request_id)
            },
            db=self.db
        )
        
        # Opcional: Evoluir estado do pedido para COMPLETED
        if request.status == EntityStatus.PROCESSING.value:
             await self.request_svc.update_state(
                 request_id=request_id,
                 new_status=EntityStatus.APPROVED,
                 actor_id=actor_id
             )

        return doc_file

    async def get_citizen_documents(
        self,
        citizen_id: uuid.UUID,
        category: Optional[str] = None
    ) -> List[DocumentFile]:
        """
        Lista documentos de um cidadão.
        """
        # Como mudamos o owner_type para 'document', precisamos buscar 
        # primeiro os Documents do cidadão e depois os files deles.
        # OU (mais simples para esta interface): Buscar files onde metadata.citizen_id == citizen_id
        # ou manter owner_id = citizen_id e owner_type = citizen para facilitar busca direta.
        
        # DECISÃO: Para manter conformidade com 'get_owner_documents', 
        # vamos buscar os Documents do cidadão e depois os arquivos.
        
        # 1. Buscar Documents do cidadão
        result_docs = await self.db.execute(
            select(Document).where(Document.citizen_id == citizen_id)
        )
        documents = result_docs.scalars().all()
        doc_ids = [d.id for d in documents]
        
        if not doc_ids:
            return []

        # 2. Buscar Files desses Documents
        result_files = await self.db.execute(
            select(DocumentFile).where(DocumentFile.owner_id.in_(doc_ids))
        )
        files = result_files.scalars().all()
        
        if category:
             files = [f for f in files if f.category == category]
             
        return files
