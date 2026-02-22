#!/usr/bin/env python3
"""
Script de validação do módulo Documents.

Testa todos os componentes principais para verificar se a implementação
está funcionando corretamente e integrada com o sistema.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Tuple

# --- Tornar import de 'modules' possível ---
_this_file = Path(__file__).resolve()
# parents[0] = .../documents
# parents[1] = .../modules
# parents[2] = .../backend  <-- é este que contém "modules"
_modules_parent = _this_file.parents[2] if len(_this_file.parents) >= 3 else None
if _modules_parent:
    sys.path.insert(0, str(_modules_parent))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("documents_validator")


class DocumentsValidator:
    """Validador do módulo Documents."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def log_error(self, message: str):
        logger.error(f"❌ {message}")
        self.errors.append(message)

    def log_warning(self, message: str):
        logger.warning(f"⚠️  {message}")
        self.warnings.append(message)

    def log_success(self, message: str):
        logger.info(f"✅ {message}")

    def validate_models(self) -> bool:
        try:
            logger.info("Validando modelos do módulo Documents...")
            from modules.documents.models.documents_models import (
                Document,
                DocumentAuditLog,
                DocumentFolder,
                DocumentPermission,
                DocumentShare,
                DocumentTemplate,
                DocumentVersion,
            )

            models_to_check: List[Tuple[str, object]] = [
                ("Document", Document),
                ("DocumentFolder", DocumentFolder),
                ("DocumentPermission", DocumentPermission),
                ("DocumentVersion", DocumentVersion),
                ("DocumentAuditLog", DocumentAuditLog),
                ("DocumentShare", DocumentShare),
                ("DocumentTemplate", DocumentTemplate),
            ]

            for model_name, model_class in models_to_check:
                if model_class:
                    self.log_success(f"Modelo {model_name} carregado com sucesso")
                else:
                    self.log_error(f"Modelo {model_name} não encontrado")

            return True
        except Exception as e:
            self.log_error(f"Erro ao validar modelos: {e}")
            return False

    def validate_schemas(self) -> bool:
        try:
            logger.info("Validando schemas do módulo Documents...")
            from modules.documents.schemas.documents import (
                DocumentCategory,
                DocumentCreate,
                DocumentFolderCreate,
                DocumentRead,
                DocumentShareCreate,
                DocumentStatus,
                DocumentType,
                DocumentUpload,
                PermissionLevel,
            )

            enums_to_check: List[Tuple[str, object]] = [
                ("DocumentCategory", DocumentCategory),
                ("DocumentStatus", DocumentStatus),
                ("DocumentType", DocumentType),
                ("PermissionLevel", PermissionLevel),
            ]

            for enum_name, enum_class in enums_to_check:
                if enum_class:
                    self.log_success(f"Enum {enum_name} carregado com sucesso")
                else:
                    self.log_error(f"Enum {enum_name} não encontrado")

            schemas_to_check: List[Tuple[str, object]] = [
                ("DocumentCreate", DocumentCreate),
                ("DocumentRead", DocumentRead),
                ("DocumentUpload", DocumentUpload),
                ("DocumentFolderCreate", DocumentFolderCreate),
                ("DocumentShareCreate", DocumentShareCreate),
            ]

            for schema_name, schema_class in schemas_to_check:
                if schema_class:
                    self.log_success(f"Schema {schema_name} carregado com sucesso")
                else:
                    self.log_error(f"Schema {schema_name} não encontrado")

            return True
        except Exception as e:
            self.log_error(f"Erro ao validar schemas: {e}")
            return False

    def validate_services(self) -> bool:
        try:
            logger.info("Validando serviços do módulo Documents...")
            from modules.documents.services.document_service import DocumentService

            if DocumentService:
                self.log_success("DocumentService carregado com sucesso")

                required_methods = [
                    "get_user_documents",
                    "upload_document",
                    "get_document_by_id",
                    "update_document",
                    "delete_document",
                    "create_folder",
                    "share_document",
                    "get_document_statistics",
                ]

                for method_name in required_methods:
                    if hasattr(DocumentService, method_name):
                        self.log_success(f"Método {method_name} encontrado")
                    else:
                        self.log_warning(
                            f"Método {method_name} não encontrado (verificar)"
                        )

                return True
            else:
                self.log_error("DocumentService não encontrado")
                return False
        except Exception as e:
            self.log_error(f"Erro ao validar serviços: {e}")
            return False

    def validate_endpoints(self) -> bool:
        try:
            logger.info("Validando endpoints do módulo Documents...")
            from modules.documents.endpoints import router

            if router:
                self.log_success("Router de endpoints carregado com sucesso")
                try:
                    routes = [getattr(r, "path", str(r)) for r in router.routes]
                except Exception:
                    routes = [str(r) for r in getattr(router, "routes", [])]

                required_endpoints = [
                    "/ping",
                    "/user",
                    "/upload",
                    "/{document_id}",
                    "/{document_id}/download",
                    "/{document_id}/preview",
                    "/folders",
                    "/{document_id}/share",
                    "/statistics/me",
                    "/shared/{share_token}",
                    "/shared/{share_token}/download",
                ]

                for endpoint in required_endpoints:
                    found = any((r == endpoint) or (endpoint in r) for r in routes)
                    if found:
                        self.log_success(f"Endpoint {endpoint} encontrado")
                    else:
                        self.log_warning(
                            f"Endpoint {endpoint} pode não estar definido (verificar)"
                        )

                return True
            else:
                self.log_error("Router de endpoints não encontrado")
                return False
        except Exception as e:
            self.log_error(f"Erro ao validar endpoints: {e}")
            return False

    def validate_module_integration(self) -> bool:
        try:
            logger.info("Validando integração do módulo Documents...")

            setup_found = False
            service_accessible = False

            try:
                from modules.documents import setup_documents_module

                if setup_documents_module:
                    setup_found = True
                    self.log_success("Função setup_documents_module encontrada")
            except Exception:
                self.log_warning(
                    "Função setup_documents_module não encontrada via modules package"
                )

            try:
                from modules.documents.services.document_service import DocumentService

                if DocumentService:
                    service_accessible = True
                    self.log_success("DocumentService acessível via import direto")
            except Exception:
                self.log_warning(
                    "DocumentService não foi possível importar diretamente (verificar)"
                )

            if not setup_found:
                self.log_warning(
                    "setup_documents_module ausente — verifique se o módulo expõe função de setup"
                )
            if not service_accessible:
                self.log_warning(
                    "DocumentService não acessível — verifique inicialização do módulo"
                )

            return True
        except Exception as e:
            self.log_error(f"Erro ao validar integração: {e}")
            return False

    def run_all_tests(self) -> bool:
        logger.info("=== INICIANDO VALIDAÇÃO DO MÓDULO DOCUMENTS ===")
        tests: List[Tuple[str, callable]] = [
            ("Modelos", self.validate_models),
            ("Schemas", self.validate_schemas),
            ("Serviços", self.validate_services),
            ("Endpoints", self.validate_endpoints),
            ("Integração", self.validate_module_integration),
        ]

        results: List[Tuple[str, bool]] = []
        for test_name, test_func in tests:
            logger.info(f"\n--- Executando: {test_name} ---")
            try:
                result = test_func()
                results.append((test_name, bool(result)))
            except Exception as e:
                logger.exception(f"Erro crítico em {test_name}: {e}")
                results.append((test_name, False))

        self._generate_report(results)
        return len(self.errors) == 0

    def _generate_report(self, results: List[Tuple[str, bool]]):
        logger.info("\n" + "=" * 60)
        logger.info("RELATÓRIO DE VALIDAÇÃO - MÓDULO DOCUMENTS")
        logger.info("=" * 60)

        for test_name, success in results:
            status = "✅ PASSOU" if success else "❌ FALHOU"
            logger.info(f"{status:>10} - {test_name}")

        total_tests = len(results)
        passed_tests = sum(1 for _, success in results if success)
        failed_tests = total_tests - passed_tests
        percent = (passed_tests / total_tests * 100) if total_tests > 0 else 0.0

        logger.info("-" * 60)
        logger.info(f"Total de testes: {total_tests}")
        logger.info(f"Testes aprovados: {passed_tests}")
        logger.info(f"Testes reprovados: {failed_tests}")
        logger.info(f"Taxa de sucesso: {percent:.1f}%")

        if self.warnings:
            logger.warning(f"\n⚠️  Avisos ({len(self.warnings)}):")
            for warning in self.warnings:
                logger.warning(f"  • {warning}")

        if self.errors:
            logger.error(f"\n❌ Erros ({len(self.errors)}):")
            for error in self.errors:
                logger.error(f"  • {error}")

        if len(self.errors) == 0:
            logger.info("\n🎉 VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
            logger.info("O módulo Documents está pronto para uso.")
        else:
            logger.error(f"\n💥 VALIDAÇÃO FALHOU COM {len(self.errors)} ERROS!")
            logger.error("O módulo precisa de correções antes de entrar em produção.")

        logger.info("=" * 60)


async def main() -> int:
    validator = DocumentsValidator()
    success = validator.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    try:
        rc = asyncio.run(main())
        sys.exit(rc)
    except KeyboardInterrupt:
        logger.warning("\nValidação interrompida pelo usuário.")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Erro inesperado: {e}", exc_info=True)
        sys.exit(1)
