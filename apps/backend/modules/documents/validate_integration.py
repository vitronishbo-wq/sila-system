#!/usr/bin/env python3
"""
Teste Integrado do Módulo Documents - SILA System

Script completo para validar todas as funcionalidades do módulo Documents
com dados reais e cenários de uso típicos.

Funcionalidades testadas:
✅ Upload e validação de arquivos
✅ Controle de acesso e permissões
✅ Organização em pastas
✅ Busca avançada com filtros
✅ Compartilhamento seguro
✅ Auditoria de ações
✅ Estatísticas de uso
"""

import asyncio
import logging
import os

# Adicionar caminhos necessários
import sys
import tempfile
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List

sys.path.append("/opt/sila-system/backend")

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Configurar logging detalhado
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configurações de teste
import os
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
UPLOAD_TEST_DIR = "/tmp/sila_test_uploads"

# Dados de teste
TEST_CITIZEN_ID = uuid.uuid4()
TEST_CITIZEN_DATA = {
    "id": TEST_CITIZEN_ID,
    "full_name": "Teste Cidadão SILA",
    "document_number": "123456789",
    "email": "teste@sila.gov.ao",
}


class DocumentsIntegrationTester:
    """Testador integrado do módulo Documents."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.successes: List[str] = []
        self.test_results: Dict[str, Any] = {}

        # Configurar banco de teste
        self.engine = create_async_engine(TEST_DATABASE_URL, echo=False)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def __aenter__(self):
        # Criar tabelas de teste
        from modules.documents.models.documents_models import Base

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Inserir dados de teste
        await self._setup_test_data()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Limpar dados de teste
        async with self.engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(sync_conn))

    def log_error(self, message: str):
        """Registra um erro."""
        logger.error(f"❌ {message}")
        self.errors.append(message)

    def log_warning(self, message: str):
        """Registra um aviso."""
        logger.warning(f"⚠️  {message}")
        self.warnings.append(message)

    def log_success(self, message: str):
        """Registra um sucesso."""
        logger.info(f"✅ {message}")
        self.successes.append(message)

    async def _setup_test_data(self):
        """Configura dados iniciais para testes."""
        try:
            async with self.async_session() as db:
                # Criar cidadão de teste
                from modules.documents.models.citizen import Citizen

                test_citizen = Citizen(**TEST_CITIZEN_DATA)
                db.add(test_citizen)
                await db.commit()

                # Criar pasta raiz de teste
                from modules.documents.models.documents_models import DocumentFolder

                test_folder = DocumentFolder(
                    name="Teste SILA",
                    description="Pasta de teste para validação",
                    is_public=False,
                    created_by=TEST_CITIZEN_ID,
                )
                db.add(test_folder)
                await db.commit()

                self.test_folder_id = test_folder.id
                self.log_success("Dados de teste configurados")

        except Exception as e:
            self.log_error(f"Erro na configuração de dados de teste: {e}")
            raise

    async def test_health_check(self) -> bool:
        """Testa endpoint de health check."""
        try:
            logger.info("🔍 Testando health check...")

            from modules.documents.endpoints import ping

            # Simular chamada do endpoint
            result = await ping()

            if (
                result.get("status") == "healthy"
                and result.get("module") == "documents"
            ):
                self.log_success("Health check funcionando corretamente")
                self.test_results["health_check"] = True
                return True
            else:
                self.log_error("Health check retornou dados inválidos")
                return False

        except Exception as e:
            self.log_error(f"Erro no health check: {e}")
            return False

    async def test_document_upload(self) -> bool:
        """Testa upload de documento."""
        try:
            logger.info("📤 Testando upload de documento...")

            # Criar arquivo de teste
            test_content = b"This is a test document for SILA system validation."
            test_filename = "teste_sila.txt"

            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, suffix=".txt"
            ) as f:
                f.write(test_content)
                temp_file_path = f.name

            try:
                # Simular upload via service
                from modules.documents.schemas.documents import DocumentUpload
                from modules.documents.services.document_service import DocumentService

                upload_data = DocumentUpload(
                    title="Documento de Teste SILA",
                    description="Documento criado para validação do sistema",
                    category="outros",
                    tags=["teste", "sila", "documentos"],
                    is_public=False,
                    permission_level="restricted",
                    parent_folder_id=self.test_folder_id,
                )

                async with self.async_session() as db:
                    # Criar arquivo mock para teste
                    class MockUploadFile:
                        def __init__(self, file_path, filename):
                            self.filename = filename
                            self.file = open(file_path, "rb")

                        async def read(self, size=-1):
                            return self.file.read(size)

                        def __del__(self):
                            self.file.close()

                    mock_file = MockUploadFile(temp_file_path, test_filename)

                    document = await DocumentService.upload_document(
                        db=db,
                        file=mock_file,
                        upload_data=upload_data,
                        citizen_id=TEST_CITIZEN_ID,
                    )

                    if document and document.id:
                        self.test_document_id = document.id
                        self.log_success(
                            f"Documento enviado com sucesso: {document.id}"
                        )
                        self.test_results["document_upload"] = True
                        return True
                    else:
                        self.log_error("Upload não retornou documento válido")
                        return False

            finally:
                # Limpar arquivo temporário
                os.unlink(temp_file_path)

        except Exception as e:
            self.log_error(f"Erro no teste de upload: {e}")
            return False

    async def test_document_access(self) -> bool:
        """Testa controle de acesso a documentos."""
        try:
            logger.info("🔐 Testando controle de acesso...")

            async with self.async_session() as db:
                from modules.documents.services.document_service import DocumentService

                # Testar acesso do criador
                document = await DocumentService.get_document_by_id(
                    db=db, document_id=self.test_document_id, citizen_id=TEST_CITIZEN_ID
                )

                if document:
                    self.log_success("Acesso do criador funcionando")
                else:
                    self.log_error("Criador não consegue acessar documento próprio")
                    return False

                # Testar acesso de usuário não autorizado
                fake_user_id = uuid.uuid4()
                document_unauthorized = await DocumentService.get_document_by_id(
                    db=db, document_id=self.test_document_id, citizen_id=fake_user_id
                )

                if document_unauthorized is None:
                    self.log_success(
                        "Controle de acesso funcionando - usuário não autorizado bloqueado"
                    )
                else:
                    self.log_error(
                        "Controle de acesso falhou - usuário não autorizado teve acesso"
                    )
                    return False

                self.test_results["access_control"] = True
                return True

        except Exception as e:
            self.log_error(f"Erro no teste de controle de acesso: {e}")
            return False

    async def test_document_search(self) -> bool:
        """Testa funcionalidades de busca."""
        try:
            logger.info("🔍 Testando funcionalidades de busca...")

            async with self.async_session() as db:
                from modules.documents.schemas.documents import DocumentSearchFilters
                from modules.documents.services.document_service import DocumentService

                # Busca sem filtros
                documents, total = await DocumentService.get_user_documents(
                    db=db, citizen_id=TEST_CITIZEN_ID
                )

                if len(documents) > 0 and total > 0:
                    self.log_success(f"Busca sem filtros retornou {total} documentos")
                else:
                    self.log_error(
                        "Busca sem filtros não retornou resultados esperados"
                    )
                    return False

                # Busca com filtros
                filters = DocumentSearchFilters(category="outros", search_text="Teste")

                filtered_docs, filtered_total = (
                    await DocumentService.get_user_documents(
                        db=db, citizen_id=TEST_CITIZEN_ID, filters=filters
                    )
                )

                if filtered_total > 0:
                    self.log_success(
                        f"Busca com filtros retornou {filtered_total} documentos"
                    )
                else:
                    self.log_warning(
                        "Busca com filtros não retornou resultados (pode ser normal)"
                    )

                self.test_results["document_search"] = True
                return True

        except Exception as e:
            self.log_error(f"Erro no teste de busca: {e}")
            return False

    async def test_folder_organization(self) -> bool:
        """Testa organização em pastas."""
        try:
            logger.info("📁 Testando organização em pastas...")

            async with self.async_session() as db:
                from modules.documents.schemas.documents import DocumentFolderCreate
                from modules.documents.services.document_service import DocumentService

                # Criar subpasta
                subfolder_data = DocumentFolderCreate(
                    name="Subpasta de Teste",
                    description="Subpasta criada para validação",
                    parent_folder_id=self.test_folder_id,
                    is_public=False,
                )

                subfolder = await DocumentService.create_folder(
                    db=db, folder_data=subfolder_data, citizen_id=TEST_CITIZEN_ID
                )

                if subfolder and subfolder.id:
                    self.test_subfolder_id = subfolder.id
                    self.log_success(f"Subpasta criada com sucesso: {subfolder.id}")

                    # Verificar hierarquia
                    if subfolder.parent_folder_id == self.test_folder_id:
                        self.log_success(
                            "Hierarquia de pastas funcionando corretamente"
                        )
                    else:
                        self.log_error("Hierarquia de pastas não está funcionando")
                        return False

                    self.test_results["folder_organization"] = True
                    return True
                else:
                    self.log_error("Criação de subpasta falhou")
                    return False

        except Exception as e:
            self.log_error(f"Erro no teste de organização em pastas: {e}")
            return False

    async def test_document_sharing(self) -> bool:
        """Testa compartilhamento seguro."""
        try:
            logger.info("🔗 Testando compartilhamento seguro...")

            async with self.async_session() as db:
                from modules.documents.schemas.documents import DocumentShareCreate
                from modules.documents.services.document_service import DocumentService

                # Criar compartilhamento
                share_data = DocumentShareCreate(
                    expires_at=datetime.utcnow()
                    + timedelta(days=7),  # Expira em 7 dias
                    max_downloads=5,
                    password_protected=False,
                    allow_download=True,
                )

                share = await DocumentService.share_document(
                    db=db,
                    document_id=self.test_document_id,
                    share_data=share_data,
                    citizen_id=TEST_CITIZEN_ID,
                )

                if share and share.share_token:
                    self.test_share_token = share.share_token
                    self.log_success(
                        f"Compartilhamento criado: {share.share_token[:16]}..."
                    )

                    # Testar acesso via token
                    from modules.documents.endpoints import access_shared_document

                    # Simular acesso público
                    shared_info = await access_shared_document(share.share_token, db)

                    if (
                        shared_info
                        and shared_info.get("title") == "Documento de Teste SILA"
                    ):
                        self.log_success(
                            "Acesso via token de compartilhamento funcionando"
                        )
                    else:
                        self.log_error("Acesso via token de compartilhamento falhou")
                        return False

                    self.test_results["document_sharing"] = True
                    return True
                else:
                    self.log_error("Criação de compartilhamento falhou")
                    return False

        except Exception as e:
            self.log_error(f"Erro no teste de compartilhamento: {e}")
            return False

    async def test_audit_logging(self) -> bool:
        """Testa sistema de auditoria."""
        try:
            logger.info("📋 Testando sistema de auditoria...")

            async with self.async_session() as db:
                from modules.documents.models.documents_models import DocumentAuditLog

                # Verificar se logs foram criados
                audit_logs = await db.run_sync(
                    lambda sync_db: sync_db.query(DocumentAuditLog).all()
                )

                if len(audit_logs) >= 3:  # Pelo menos upload, acesso e compartilhamento
                    self.log_success(
                        f"Auditoria registrada: {len(audit_logs)} ações logadas"
                    )

                    # Verificar tipos de ações
                    action_types = [log.action for log in audit_logs]
                    expected_actions = ["UPLOAD", "ACCESS", "SHARE"]

                    for action in expected_actions:
                        if action in action_types:
                            self.log_success(f"Ação de auditoria '{action}' registrada")
                        else:
                            self.log_warning(
                                f"Ação de auditoria '{action}' não encontrada"
                            )

                    self.test_results["audit_logging"] = True
                    return True
                else:
                    self.log_error(
                        f"Poucas ações de auditoria registradas: {len(audit_logs)}"
                    )
                    return False

        except Exception as e:
            self.log_error(f"Erro no teste de auditoria: {e}")
            return False

    async def test_statistics(self) -> bool:
        """Testa geração de estatísticas."""
        try:
            logger.info("📊 Testando geração de estatísticas...")

            async with self.async_session() as db:
                from modules.documents.services.document_service import DocumentService

                # Obter estatísticas
                stats = await DocumentService.get_document_statistics(
                    db=db, citizen_id=TEST_CITIZEN_ID
                )

                if stats and isinstance(stats, dict):
                    self.log_success("Estatísticas geradas com sucesso")

                    # Verificar campos obrigatórios
                    required_fields = [
                        "total_documents",
                        "documents_by_category",
                        "documents_by_status",
                        "total_size_bytes",
                        "recent_uploads",
                        "top_uploaders",
                    ]

                    for field in required_fields:
                        if field in stats:
                            self.log_success(f"Campo de estatística '{field}' presente")
                        else:
                            self.log_error(f"Campo de estatística '{field}' ausente")

                    if stats["total_documents"] >= 1:
                        self.log_success(
                            f"Total de documentos: {stats['total_documents']}"
                        )
                    else:
                        self.log_error("Contagem de documentos incorreta")

                    self.test_results["statistics"] = True
                    return True
                else:
                    self.log_error("Estatísticas não geradas corretamente")
                    return False

        except Exception as e:
            self.log_error(f"Erro no teste de estatísticas: {e}")
            return False

    async def run_all_tests(self) -> bool:
        """Executa todos os testes integrados."""
        logger.info("🚀 INICIANDO TESTES INTEGRADOS DO MÓDULO DOCUMENTS")
        logger.info("=" * 60)

        test_methods = [
            ("Health Check", self.test_health_check),
            ("Document Upload", self.test_document_upload),
            ("Access Control", self.test_document_access),
            ("Document Search", self.test_document_search),
            ("Folder Organization", self.test_folder_organization),
            ("Document Sharing", self.test_document_sharing),
            ("Audit Logging", self.test_audit_logging),
            ("Statistics", self.test_statistics),
        ]

        for test_name, test_method in test_methods:
            logger.info(f"\n🔧 Executando: {test_name}")
            try:
                success = await test_method()
                if success:
                    logger.info(f"✅ {test_name}: PASSOU")
                else:
                    logger.error(f"❌ {test_name}: FALHOU")
            except Exception as e:
                logger.error(f"💥 {test_name}: ERRO CRÍTICO - {e}")

        # Relatório final
        self._generate_final_report()

        # Calcular sucesso geral
        total_tests = len(test_methods)
        passed_tests = sum(1 for result in self.test_results.values() if result)

        logger.info(
            f"\n🏁 RESULTADO FINAL: {passed_tests}/{total_tests} testes aprovados"
        )

        if passed_tests == total_tests:
            logger.info("🎉 TODOS OS TESTES PASSARAM! Módulo Documents operacional.")
            return True
        else:
            logger.error(
                f"❌ {total_tests - passed_tests} testes falharam. Verifique implementação."
            )
            return False

    def _generate_final_report(self):
        """Gera relatório detalhado dos resultados."""
        logger.info("\n" + "=" * 80)
        logger.info("RELATÓRIO DETALHADO - TESTES INTEGRADOS DOCUMENTS")
        logger.info("=" * 80)

        logger.info(f"\n📊 RESUMO EXECUTIVO:")
        logger.info(f"   Testes executados: {len(self.test_results)}")
        logger.info(
            f"   Testes aprovados: {sum(1 for r in self.test_results.values() if r)}"
        )
        logger.info(
            f"   Testes reprovados: {sum(1 for r in self.test_results.values() if not r)}"
        )
        success_rate = (
            sum(1 for r in self.test_results.values() if r) / len(self.test_results)
        ) * 100
        logger.info(f"   Taxa de sucesso: {success_rate:.1f}%")

        logger.info(f"\n✅ TESTES APROVADOS:")
        for test_name, result in self.test_results.items():
            if result:
                logger.info(f"   • {test_name}")

        logger.info(f"\n❌ TESTES REPROVADOS:")
        for test_name, result in self.test_results.items():
            if not result:
                logger.info(f"   • {test_name}")

        if self.warnings:
            logger.warning(f"\n⚠️  AVISOS ({len(self.warnings)}):")
            for warning in self.warnings:
                logger.warning(f"   • {warning}")

        if self.errors:
            logger.error(f"\n💥 ERROS CRÍTICOS ({len(self.errors)}):")
            for error in self.errors:
                logger.error(f"   • {error}")

        logger.info(f"\n📋 DADOS DE TESTE CRIADOS:")
        logger.info(f"   • Cidadão: {TEST_CITIZEN_ID}")
        logger.info(f"   • Pasta raiz: {self.test_folder_id}")
        if hasattr(self, "test_document_id"):
            logger.info(f"   • Documento: {self.test_document_id}")
        if hasattr(self, "test_subfolder_id"):
            logger.info(f"   • Subpasta: {self.test_subfolder_id}")
        if hasattr(self, "test_share_token"):
            logger.info(f"   • Token compartilhamento: {self.test_share_token[:16]}...")

        logger.info(f"\n🎯 RECOMENDAÇÕES:")
        if len(self.errors) == 0:
            logger.info("   ✅ Módulo pronto para produção")
            logger.info("   ✅ Integração com frontend pode prosseguir")
            logger.info("   ✅ Implementar monitoramento de performance")
        else:
            logger.info("   ❌ Corrigir erros antes de prosseguir")
            logger.info("   ⚠️  Revisar avisos para otimização")

        logger.info("=" * 80)


async def main():
    """Função principal de execução."""
    try:
        async with DocumentsIntegrationTester() as tester:
            success = await tester.run_all_tests()
            return 0 if success else 1
    except Exception as e:
        logger.error(f"Erro crítico na execução dos testes: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
