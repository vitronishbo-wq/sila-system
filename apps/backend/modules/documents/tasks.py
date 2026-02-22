# apps/backend/modules/documents/tasks.py

import os
import uuid
import datetime
from pathlib import Path
from typing import Optional
import asyncio

from celery import shared_task
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.session import AsyncSessionLocal
from modules.documents.models.documents import Document, DocumentStatus
from config.settings import settings

# === Configurações ===
# Ensure UPLOAD_DIR is mapped in settings
UPLOAD_DIR_SETTING = getattr(settings, "UPLOAD_DIR", "/app/uploads")
BASE_UPLOADS_DIR = Path(UPLOAD_DIR_SETTING)
THUMBNAIL_SIZE = (800, 800)
PDF_DPI = 300
OCR_LANG = "por"

# === Funções Auxiliares ===


def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    # No permissive chmod 777 in production, but following user's hint for dev
    try:
        path.chmod(0o777)
    except Exception:
        pass


def _derive_storage_paths(document_uuid: str) -> tuple[Path, Path, Path]:
    today = datetime.date.today()
    date_path = f"{today.year}/{today.month:02d}/{today.day:02d}"
    date_dir = BASE_UPLOADS_DIR / date_path
    _ensure_dir(date_dir)

    pdf_path = date_dir / f"{document_uuid}.pdf"
    ocr_path = date_dir / f"{document_uuid}.txt"
    thumb_path = date_dir / f"{document_uuid}_thumb.png"

    return pdf_path, ocr_path, thumb_path


def _generate_thumbnail(pdf_path: Path, thumb_path: Path):
    try:
        pages = convert_from_path(str(pdf_path), dpi=PDF_DPI, first_page=1, last_page=1, fmt="png")
        if not pages:
            raise RuntimeError("PDF vazio ou corrompido")
        img = pages[0].convert("RGB")
        img.thumbnail(THUMBNAIL_SIZE)
        img.save(thumb_path, "PNG", optimize=True, quality=85)
        try:
            thumb_path.chmod(0o666)
        except Exception:
            pass
    except PDFPageCountError as e:
        raise RuntimeError("Falha ao converter PDF para imagem") from e


def _perform_ocr(pdf_path: Path) -> str:
    try:
        pages = convert_from_path(str(pdf_path), dpi=PDF_DPI,
                                  first_page=1, last_page=1, grayscale=True)
        if not pages:
            return ""
        img = pages[0]
        text = pytesseract.image_to_string(img, lang=OCR_LANG, config='--psm 3')
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""  # Don't crash the whole task if OCR fails, but record error


async def _update_document_async(
    document_id: uuid.UUID,
    status: DocumentStatus,
    ocr_text_path: Optional[str] = None,
    thumbnail_path: Optional[str] = None,
    ocr_text: Optional[str] = None,
):
    async with AsyncSessionLocal() as session:
        stmt = (
            update(Document)
            .where(Document.id == document_id)
            .values(
                status=status,
                ocr_text_path=ocr_text_path,
                thumbnail_path=thumbnail_path,
                ocr_text=ocr_text,
                processed_at=datetime.datetime.utcnow() if status == DocumentStatus.COMPLETED else None,
            )
        )
        await session.execute(stmt)
        await session.commit()

# === Task Principal ===


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    acks_late=True,
)
def process_document_ocr_task(self, document_id: str, original_file_path: str):
    """
    Task robusta para processamento de documentos.
    Note: document_id comes as string from Celery.
    """
    doc_id_uuid = uuid.UUID(document_id)
    # Use a separate UUID for the filename to avoid simple enumeration
    storage_uuid = uuid.uuid4().hex

    try:
        # Move para /processing
        asyncio.run(_update_document_async(doc_id_uuid, DocumentStatus.PROCESSING))

        # Deriva caminhos finais
        final_pdf_path, ocr_path, thumb_path = _derive_storage_paths(storage_uuid)

        # Move arquivo
        temp_path = Path(original_file_path)
        if not temp_path.exists():
            raise FileNotFoundError(f"Arquivo original não encontrado: {original_file_path}")

        final_pdf_path.write_bytes(temp_path.read_bytes())
        temp_path.unlink(missing_ok=True)
        try:
            final_pdf_path.chmod(0o666)
        except Exception:
            pass

        # Processamento
        _generate_thumbnail(final_pdf_path, thumb_path)
        ocr_text = _perform_ocr(final_pdf_path)
        if ocr_text:
            ocr_path.write_text(ocr_text, encoding="utf-8")
            try:
                ocr_path.chmod(0o666)
            except Exception:
                pass
            ocr_text_path_str = str(ocr_path)
        else:
            ocr_text_path_str = None

        # Finaliza com sucesso
        asyncio.run(
            _update_document_async(
                doc_id_uuid,
                DocumentStatus.COMPLETED,
                ocr_text_path=ocr_text_path_str,
                thumbnail_path=str(thumb_path),
                ocr_text=ocr_text,
            )
        )

    except Exception as exc:
        asyncio.run(_update_document_async(doc_id_uuid, DocumentStatus.FAILED))
        raise self.retry(exc=exc)
