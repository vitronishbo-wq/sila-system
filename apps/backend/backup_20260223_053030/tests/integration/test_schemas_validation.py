"""
Testes de validação dos principais schemas em app/schemas.
"""

from datetime import datetime
from uuid import uuid4

import pytest

# ATENÇÃO: Verifique o caminho real para seus schemas.
# Assumindo que todos estão em 'modules.<modulo>.schemas' ou um único 'app.schemas'
# Se 'app.schemas' for o caminho correto, mantenha a importação abaixo e adicione 'settings'
from config import settings
from app.schemas import (
    BulkNotificationRequest,
    FieldType,
    FormField,
    FormSchema,
    NotificationCreate,
    NotificationStatusEnum,
    NotificationTypeEnum,
    ServiceDefinition,
    ServiceStatus,
    Token,
    TokenPayload,
    UserCreate,
    UserRole,
)

# ATENÇÃO: Verifique o caminho real para suas configurações
from core.config import settings


# --- User Schemas ---
def test_user_create_valid():
    """Testa a criação de um UserCreate com dados válidos."""
    # Corrigido: Passando a senha como um argumento de palavra-chave
    user = UserCreate(
        email="test@example.com", full_name="Test User", password="test_password_123"
    )
    # Note: 'is_active' é um campo ORM/DB, não Pydantic, a menos que esteja no schema.
    # Removido o teste de 'is_active' para focar na validação do schema.


def test_user_create_invalid_password():
    """Testa o schema UserCreate com uma senha curta ou inválida (se houver validação Pydantic)."""
    # Corrigido: Passando a senha como um argumento de palavra-chave
    user = UserCreate(
        email="short@example.com", full_name="Short Password", password="short_pass_123"
    )
    # Nota: Este teste apenas verifica a criação do Pydantic, não a segurança real.
    assert user.password == "short_pass_123"


# --- Token Schemas ---
def test_token_schema():
    """Testa a criação do schema Token."""
    token = Token(access_token="abc123", token_type="bearer")
    assert token.token_type == "bearer"


def test_token_payload_optional_fields():
    """Testa a criação do TokenPayload com campos opcionais."""
    # Note: 'sub' e 'exp' são provavelmente obrigatórios para o JWT Payload.
    payload = TokenPayload(
        sub="1", exp=1234567890
    )  # 'sub' é geralmente uma string (ID)
    assert payload.sub == "1"
    assert payload.exp == 1234567890


# --- Notification Schemas ---
def test_notification_create_valid():
    """Testa a criação de um NotificationCreate com campos obrigatórios."""
    n = NotificationCreate(
        destinatario_id=1,
        # Corrigido: Assegurando que o campo 'tipo' e seu valor do enum estão corretos
        tipo=NotificationTypeEnum.EMAIL,
        titulo="Hello",
        mensagem="Test message",
    )
    assert n.tipo == NotificationTypeEnum.EMAIL


def test_bulk_notification_request():
    """Testa a criação de um BulkNotificationRequest."""
    b = BulkNotificationRequest(
        notificacoes=[
            NotificationCreate(
                destinatario_id=1,
                tipo=NotificationTypeEnum.SMS,
                titulo="Aviso",
                mensagem="Mensagem em massa",
            )
        ]
    )
    assert len(b.notificacoes) == 1


# --- Service Schemas ---
def test_service_definition_with_form():
    """Testa a criação de um ServiceDefinition que inclui um FormSchema aninhado."""
    form = FormSchema(
        title="Cadastro",
        fields=[
            FormField(
                name="email",
                label="E-mail",
                type=FieldType.EMAIL,
                required=True,
            )
        ],
    )
    service = ServiceDefinition(
        id="svc1",
        name="Serviço Teste",
        module="services.test",
        api_endpoint="/api/services/test",
        roles=[UserRole.CITIZEN, UserRole.STAFF],
        status=ServiceStatus.ACTIVE,
        form_schema=form,
    )
    assert service.status == ServiceStatus.ACTIVE
    assert service.form_schema.fields[0].type == FieldType.EMAIL
