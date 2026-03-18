#!/usr/bin/env bash
set -e

ROOT="apps/backend/app/modules/justice"

echo "=== JUSTICE AUTO MIGRATION ==="

cd $ROOT

echo "1️⃣ Criando estrutura se não existir"

mkdir -p bounded_contexts/vital_events/application/services
mkdir -p bounded_contexts/vital_events/domain/entities
mkdir -p bounded_contexts/vital_events/infrastructure/repositories
mkdir -p bounded_contexts/vital_events/infrastructure/models

mkdir -p bounded_contexts/civil_registry_core/application/services
mkdir -p bounded_contexts/identity_documents/application/services


echo "2️⃣ Movendo SERVICES"

mv -f civil_registry/application/services/birth_service.py \
bounded_contexts/vital_events/application/services/ 2>/dev/null || true

mv -f civil_registry/application/services/death_service.py \
bounded_contexts/vital_events/application/services/ 2>/dev/null || true

mv -f civil_registry/application/services/marriage_service.py \
bounded_contexts/vital_events/application/services/ 2>/dev/null || true

mv -f civil_registry/application/services/citizen_service.py \
bounded_contexts/civil_registry_core/application/services/ 2>/dev/null || true

mv -f civil_registry/application/services/profile_queries.py \
bounded_contexts/civil_registry_core/application/services/ 2>/dev/null || true

mv -f civil_registry/application/services/document_service.py \
bounded_contexts/identity_documents/application/services/ 2>/dev/null || true

mv -f civil_registry/application/services/certificate_service.py \
bounded_contexts/identity_documents/application/services/ 2>/dev/null || true

mv -f civil_registry/application/services/bi_emission_service.py \
bounded_contexts/identity_documents/application/services/ 2>/dev/null || true


echo "3️⃣ Movendo DOMAIN ENTITIES"

mv -f civil_registry/domain/models/birth_record.py \
bounded_contexts/vital_events/domain/entities/ 2>/dev/null || true

mv -f civil_registry/domain/models/death_record.py \
bounded_contexts/vital_events/domain/entities/ 2>/dev/null || true

mv -f civil_registry/domain/models/marriage_record.py \
bounded_contexts/vital_events/domain/entities/ 2>/dev/null || true


echo "4️⃣ Movendo REPOSITORIES"

mv -f civil_registry/infrastructure/repositories/birth_repository.py \
bounded_contexts/vital_events/infrastructure/repositories/ 2>/dev/null || true

mv -f civil_registry/infrastructure/repositories/death_repository.py \
bounded_contexts/vital_events/infrastructure/repositories/ 2>/dev/null || true

mv -f civil_registry/infrastructure/repositories/marriage_repository.py \
bounded_contexts/vital_events/infrastructure/repositories/ 2>/dev/null || true


echo "5️⃣ Movendo SQL MODELS"

mv -f civil_registry/infrastructure/models/birth_model.py \
bounded_contexts/vital_events/infrastructure/models/ 2>/dev/null || true

mv -f civil_registry/infrastructure/models/death_model.py \
bounded_contexts/vital_events/infrastructure/models/ 2>/dev/null || true

mv -f civil_registry/infrastructure/models/marriage_model.py \
bounded_contexts/vital_events/infrastructure/models/ 2>/dev/null || true


echo "6️⃣ Atualizando imports automaticamente"

find . -type f -name "*.py" -exec sed -i \
's/modules\.justice\.civil_registry/modules.justice.bounded_contexts/g' {} +


echo "7️⃣ Removendo código claramente obsoleto"

rm -f civil_registry/application/services/models.py
rm -f civil_registry/application/services/queries_frozen.py
rm -f civil_registry/application/services/rules.py
rm -f civil_registry/application/services/service.py


echo "8️⃣ Gerando relatório de arquivos restantes"

echo ""
echo "Arquivos ainda dentro de civil_registry:"
find civil_registry -type f | wc -l

echo ""
echo "Migração automática concluída (≈80%)."
echo "Execute testes antes de remover civil_registry completamente."
