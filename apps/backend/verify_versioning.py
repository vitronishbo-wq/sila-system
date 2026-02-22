from modules.documents.schemas.documents import DocumentCreate
from modules.documents.services.document_service import DocumentService
from modules.identity.models.user import User
from core.db.session import AsyncSessionLocal
from core.db import base  # Registra todos os modelos
import asyncio
import os
import sys
from uuid import uuid4, UUID
from fastapi import UploadFile
from io import BytesIO

# Adiciona o path do projeto
sys.path.append(os.path.join(os.getcwd(), "apps", "backend"))


async def verify_versioning():
    print("🚀 Verificando sistema de versionamento de documentos...")

    async with AsyncSessionLocal() as db:
        service = DocumentService(db)

        # 1. Criar utilizador de teste se não existir
        user = User(
            id=uuid4(),
            email=f"tester_{uuid4().hex[:6]}@sila.ao",
            full_name="Document Tester",
            hashed_password="hashed_fake_password",
            is_active=True
        )
        db.add(user)
        await db.commit()
        print(f"✅ Utilizador de teste criado: {user.email}")

        # 2. Upload inicial (Versão 1)
        print("\n--- Testando Upload Inicial (V1) ---")
        file_v1 = UploadFile(
            filename="contrato_v1.pdf",
            file=BytesIO(b"Conteudo da versao 1"),
            size=len(b"Conteudo da versao 1"),
            headers={"content-type": "application/pdf"}
        )
        metadata = DocumentCreate(
            title="Contrato de Prestação de Serviços",
            description="Contrato inicial",
            is_public=False
        )

        doc = await service.upload_document(file_v1, metadata, user.id)
        print(f"✅ Documento criado: {doc.title} (ID: {doc.id})")
        print(f"✅ Versão atual: {doc.current_version_id}")

        # 3. Criar nova versão (Versão 2)
        print("\n--- Testando Nova Versão (V2) ---")
        file_v2 = UploadFile(
            filename="contrato_v2_final.pdf",
            file=BytesIO(b"Conteudo da versao 2 atualizado"),
            size=len(b"Conteudo da versao 2 atualizado"),
            headers={"content-type": "application/pdf"}
        )

        new_v = await service.create_new_version(
            document_id=doc.id,
            file=file_v2,
            uploaded_by_id=user.id,
            changelog="Atualização das cláusulas financeiras"
        )
        print(f"✅ Nova versão criada: {new_v.version_number} (ID: {new_v.id})")

        # 4. Verificar histórico
        print("\n--- Verificando Histórico ---")
        versions = await service.list_versions(doc.id)
        print(f"✅ Encontradas {len(versions)} versões")
        for v in versions:
            print(f"  - V{v.version_number}: {v.changelog} (Data: {v.uploaded_at})")

        # 5. Verificar se o documento principal aponta para a V2
        await db.refresh(doc)
        if doc.current_version_id == new_v.id:
            print(
                f"✅ Documento aponta corretamente para a versão mais recente (V{new_v.version_number})")
        else:
            print("✗ Erro: current_version_id não atualizado corretamente")

if __name__ == "__main__":
    asyncio.run(verify_versioning())
