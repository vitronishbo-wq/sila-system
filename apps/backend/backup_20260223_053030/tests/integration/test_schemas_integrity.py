from datetime import datetime

import pytest

from app import schemas


@pytest.mark.parametrize(
    "schema_class, init_kwargs",
    [
        # user
        (
            schemas.UserCreate,
            {"username": "john", "email": "john@example.com", "password": "secret123"},
        ),
        (schemas.UserUpdate, {"username": "doe"}),
        (schemas.UserRead, {"id": 1, "username": "john", "email": "john@example.com"}),
        # token
        (schemas.Token, {"access_token": "abc123", "token_type": "bearer"}),
        (schemas.TokenData, {"username": "john"}),
        # services
        (schemas.ServiceCreate, {"nome": "Serviço X", "nome_en": "Service X"}),
        (schemas.ServiceUpdate, {"descricao": "atualizado"}),
        (
            schemas.ServiceRead,
            {
                "id": 1,
                "nome": "Serviço X",
                "nome_en": "Service X",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "ativo",
            },
        ),
        # notifications
        (schemas.NotificationCreate, {"titulo": "Notificação", "mensagem": "Teste"}),
        (schemas.NotificationUpdate, {"mensagem": "Atualizado"}),
        (
            schemas.NotificationRead,
            {
                "id": 1,
                "titulo": "Notificação",
                "mensagem": "Teste",
                "lida": False,
                "data_criacao": datetime.now(),
            },
        ),
        # adocao_menor
        (schemas.AdocaoMenorCreate, {"nome": "Adoção", "nome_en": "Adoption"}),
        (schemas.AdocaoMenorUpdate, {"status": "pendente"}),
        (
            schemas.AdocaoMenorRead,
            {
                "id": 1,
                "nome": "Adoção",
                "nome_en": "Adoption",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "ativo",
            },
        ),
        # certidao_negativa
        (
            schemas.CertidaoNegativaCreate,
            {"nome": "Certidão", "nome_en": "Certificate"},
        ),
        (schemas.CertidaoNegativaUpdate, {"descricao": "alterado"}),
        (
            schemas.CertidaoNegativaRead,
            {
                "id": 1,
                "nome": "Certidão",
                "nome_en": "Certificate",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "emitido",
            },
        ),
        # reconhecimento_paternidade
        (
            schemas.ReconhecimentoPaternidadeCreate,
            {"nome": "Reconhecimento", "nome_en": "Recognition"},
        ),
        (schemas.ReconhecimentoPaternidadeUpdate, {"status": "em análise"}),
        (
            schemas.ReconhecimentoPaternidadeRead,
            {
                "id": 1,
                "nome": "Reconhecimento",
                "nome_en": "Recognition",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "ativo",
            },
        ),
        # registo_casamento
        (schemas.RegistoCasamentoCreate, {"nome": "Casamento", "nome_en": "Marriage"}),
        (schemas.RegistoCasamentoUpdate, {"status": "confirmado"}),
        (
            schemas.RegistoCasamentoRead,
            {
                "id": 1,
                "nome": "Casamento",
                "nome_en": "Marriage",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "ativo",
            },
        ),
        # registo_civil
        (schemas.RegistoCivilCreate, {"nome": "Civil", "nome_en": "Civil"}),
        (schemas.RegistoCivilUpdate, {"descricao": "dados extras"}),
        (
            schemas.RegistoCivilRead,
            {
                "id": 1,
                "nome": "Civil",
                "nome_en": "Civil",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "válido",
            },
        ),
        # registo_imovel
        (schemas.RegistoImovelCreate, {"nome": "Imóvel", "nome_en": "Property"}),
        (schemas.RegistoImovelUpdate, {"status": "verificado"}),
        (
            schemas.RegistoImovelRead,
            {
                "id": 1,
                "nome": "Imóvel",
                "nome_en": "Property",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "ativo",
            },
        ),
        # registo_nascimento
        (schemas.RegistoNascimentoCreate, {"nome": "Nascimento", "nome_en": "Birth"}),
        (schemas.RegistoNascimentoUpdate, {"descricao": "atualizado"}),
        (
            schemas.RegistoNascimentoRead,
            {
                "id": 1,
                "nome": "Nascimento",
                "nome_en": "Birth",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "ativo",
            },
        ),
        # registo_obito
        (schemas.RegistoObitoCreate, {"nome": "Óbito", "nome_en": "Death"}),
        (schemas.RegistoObitoUpdate, {"status": "confirmado"}),
        (
            schemas.RegistoObitoRead,
            {
                "id": 1,
                "nome": "Óbito",
                "nome_en": "Death",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "registrado",
            },
        ),
        # retificacao_registro
        (
            schemas.ReticacaoRegistroCreate,
            {"nome": "Retificação", "nome_en": "Rectification"},
        ),
        (schemas.ReticacaoRegistroUpdate, {"descricao": "corrigido"}),
        (
            schemas.ReticacaoRegistroRead,
            {
                "id": 1,
                "nome": "Retificação",
                "nome_en": "Rectification",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "ativo",
            },
        ),
        # tutela_menor
        (schemas.TutelaMenorCreate, {"nome": "Tutela", "nome_en": "Guardianship"}),
        (
            schemas.TutelaMenorRead,
            {
                "id": 1,
                "nome": "Tutela",
                "nome_en": "Guardianship",
                "ativo": True,
                "data_criacao": datetime.now(),
                "status": "ativo",
            },
        ),
    ],
)
def test_schema_instantiation(schema_class, init_kwargs):
    """Test that schemas can be instantiated without errors."""
    instance = schema_class(**init_kwargs)
    assert instance is not None
