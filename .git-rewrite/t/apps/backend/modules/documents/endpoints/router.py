"""
Router principal para o módulo de Documentos.

Este módulo define as rotas da API para operações relacionadas a documentos,
incluindo upload, download, listagem e gerenciamento de permissões.
"""

from fastapi import APIRouter, status

# Cria o router principal do módulo de documentos
router = APIRouter(tags=["Documents"])


@router.get("/ping")
async def ping():
    """Endpoint de verificação de saúde do módulo."""
    return {"status": "ok"}


@router.get("/user")
async def get_user():
    """Retorna informações do usuário autenticado."""
    return {"user": "test"}


@router.post("/upload")
async def upload():
    """Faz upload de um novo documento."""
    return {"upload": "ok"}


@router.get("/{document_id}")
async def get_document(document_id: int):
    """Obtém detalhes de um documento específico."""
    return {"id": document_id}


@router.get("/{document_id}/download")
async def download_document(document_id: int):
    """Faz download de um documento."""
    return {"download": f"{document_id}"}


@router.get("/{document_id}/preview")
async def preview_document(document_id: int):
    """Visualiza preview de um documento."""
    return {"preview": f"{document_id}"}


@router.get("/folders")
async def list_folders():
    """Lista pastas do usuário."""
    return {"folders": []}


@router.post("/{document_id}/share")
async def share_document(document_id: int):
    """Compartilha um documento."""
    return {"shared": f"{document_id}"}


@router.get("/statistics/me")
async def my_statistics():
    """Retorna estatísticas do usuário."""
    return {"total": 0}


@router.get("/shared/{share_token}")
async def get_shared_document(share_token: str):
    """Obtém documento compartilhado."""
    return {"token": share_token}


@router.get("/shared/{share_token}/download")
async def download_shared_document(share_token: str):
    """Faz download de documento compartilhado."""
    return {"download": share_token}
