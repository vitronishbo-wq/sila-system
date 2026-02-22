#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Templates for SILA code generation.

This module contains all the templates used for generating modules and services.
Templates use Python string formatting with named parameters.
"""

# Module generation templates
MODULE_TEMPLATES = {
    "init": '''# {module_name} Module
# Sistema Integrado Local de Administração (SILA)

"""
Módulo {module_title}

Este módulo é responsável por {module_description}
"""

from fastapi import APIRouter

router = APIRouter()

# Import and include service routes here
# from .routes.service_name import router as service_router
# router.include_router(service_router)
''',
    "models": '''# {module_name} Models
# Sistema Integrado Local de Administração (SILA)

"""
Modelos de dados para o módulo {module_title}.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

# Defina seus modelos aqui
''',
    "schemas": '''# {module_name} Schemas
# Sistema Integrado Local de Administração (SILA)

"""
Esquemas de validação para o módulo {module_title}.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Defina seus esquemas aqui
''',
    "crud": '''# {module_name} CRUD Operations
# Sistema Integrado Local de Administração (SILA)

"""
Operações CRUD para o módulo {module_title}.
"""

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from . import models, schemas

# Implemente suas operações CRUD aqui
''',
    "services": '''# {module_name} Services
# Sistema Integrado Local de Administração (SILA)

"""
Serviços de negócio para o módulo {module_title}.
"""

from typing import List, Dict, Any, Optional

from app.modules.service_hub.services import register_service
from . import crud, models, schemas

# Implemente seus serviços aqui
''',
    "endpoints": '''# {module_name} Endpoints
# Sistema Integrado Local de Administração (SILA)

"""
Endpoints da API para o módulo {module_title}.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.db.session import get_db
from app.auth_utils import get_current_active_user
from . import crud, schemas, models, services

router = APIRouter()

# Implemente seus endpoints aqui
''',
    "readme": """# Módulo {module_title}

## Descrição
{module_description}

## Funcionalidades
- Funcionalidade 1
- Funcionalidade 2

## Estrutura
- `models.py`: Modelos de dados
- `schemas.py`: Esquemas de validação
- `crud.py`: Operações CRUD
- `services.py`: Serviços de negócio
- `endpoints.py`: Endpoints da API

## Como usar
```python
# Exemplo de uso
```
""",
    "tests": '''# {module_name} Tests
# Sistema Integrado Local de Administração (SILA)

"""
Testes para o módulo {module_title}.
"""

import pytest
from fastapi.testclient import TestClient

# Implemente seus testes aqui
''',
}

# Service generation templates
SERVICE_TEMPLATES = {
    "model": """# {model_name} Model
# Sistema Integrado Local de Administração (SILA)

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class {model_name}(Base):
    __tablename__ = "{table_name}"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    nome_en = Column(String(200), nullable=False)  # English name
    descricao = Column(String(500))
    descricao_en = Column(String(500))  # English description
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    dados_adicionais = Column(JSON)  # For flexible additional data
    # Conditional relationship based on service type
    municipe_id = Column(Integer, nullable={nullable_municipe})  # Only for citizen services
    status = Column(String(50), default="pendente")
""",
    "schema": """# {model_name} Schemas
# Sistema Integrado Local de Administração (SILA)

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class {model_name}Create(BaseModel):
    nome: str
    nome_en: str
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    dados_adicionais: Optional[Dict[str, Any]] = None

class {model_name}Update(BaseModel):
    nome: Optional[str] = None
    nome_en: Optional[str] = None
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    ativo: Optional[bool] = None
    status: Optional[str] = None
    dados_adicionais: Optional[Dict[str, Any]] = None

class {model_name}Read(BaseModel):
    id: int
    nome: str
    nome_en: str
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    status: str
    dados_adicionais: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
""",
    "route_citizen": '''# {model_name} Routes (Citizen Service)
# Sistema Integrado Local de Administração (SILA)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.{module_name}.models.{service_slug} import {model_name}
from app.modules.{module_name}.schemas.{service_slug} import {model_name}Create, {model_name}Read, {model_name}Update
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/{api_slug}", tags=["{display_name}"])

@router.post("/", response_model={model_name}Read)
def criar_{service_slug}(
    data: {model_name}Create,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new {display_name_en} / Criar novo {display_name_pt}"""
    db_item = {model_name}(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model={model_name}Read)
def obter_{service_slug}(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get {display_name_en} by ID / Obter {display_name_pt} por ID"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[{model_name}Read])
def listar_{service_slug}(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List {display_name_en} / Listar {display_name_pt}"""
    return db.query({model_name}).filter(
        {model_name}.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/{item_id}", response_model={model_name}Read)
def atualizar_{service_slug}(
    item_id: int,
    data: {model_name}Update,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update {display_name_en} / Atualizar {display_name_pt}"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def deletar_{service_slug}(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete {display_name_en} / Deletar {display_name_pt}"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para deletar este recurso")

    db.delete(item)
    db.commit()
    return {{"message": "{display_name_pt} deletado com sucesso"}}
''',
    "route_internal": '''# {model_name} Routes (Internal Service)
# Sistema Integrado Local de Administração (SILA)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.{module_name}.models.{service_slug} import {model_name}
from app.modules.{module_name}.schemas.{service_slug} import {model_name}Create, {model_name}Read, {model_name}Update

router = APIRouter(prefix="/internal/{api_slug}", tags=["{display_name}"])

@router.post("/", response_model={model_name}Read)
def criar_{service_slug}(data: {model_name}Create, db: Session = Depends(get_db)):
    """Create new {display_name_en} / Criar novo {display_name_pt}"""
    db_item = {model_name}(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model={model_name}Read)
def obter_{service_slug}(item_id: int, db: Session = Depends(get_db)):
    """Get {display_name_en} by ID / Obter {display_name_pt} por ID"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")
    return item

@router.get("/", response_model=List[{model_name}Read])
def listar_{service_slug}(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List {display_name_en} / Listar {display_name_pt}"""
    return db.query({model_name}).offset(skip).limit(limit).all()

@router.put("/{item_id}", response_model={model_name}Read)
def atualizar_{service_slug}(item_id: int, data: {model_name}Update, db: Session = Depends(get_db)):
    """Update {display_name_en} / Atualizar {display_name_pt}"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def deletar_{service_slug}(item_id: int, db: Session = Depends(get_db)):
    """Delete {display_name_en} / Deletar {display_name_pt}"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")

    db.delete(item)
    db.commit()
    return {{"message": "{display_name_pt} deletado com sucesso"}}
''',
    "service_registration": '''@register_service(
    slug="{service_slug}",
    nome="{display_name_pt}",
    nome_en="{display_name_en}",
    descricao="Serviço para {display_name_pt_lower}",
    descricao_en="Service for {display_name_en_lower}",
    departamento="{module_name}",
    categoria="{module_name}",
    tipo_servico="{service_type}"
)
def {service_slug}_handler(data):
    """
    Handler for {display_name_en} / Manipulador para {display_name_pt}
    """
    return {{"status": "success", "service": "{service_slug}"}}
''',
    "test": '''# {model_name} Tests
# Sistema Integrado Local de Administração (SILA)

"""
Testes para o serviço {display_name}.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_criar_{service_slug}(client: TestClient, db: Session):
    """Test creating a new {display_name_lower}"""
    # Implemente o teste aqui
    pass

def test_obter_{service_slug}(client: TestClient, db: Session):
    """Test getting a {display_name_lower} by ID"""
    # Implemente o teste aqui
    pass

def test_listar_{service_slug}(client: TestClient, db: Session):
    """Test listing {display_name_lower}"""
    # Implemente o teste aqui
    pass
''',
}
