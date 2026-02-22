from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from ...domain.models.citizen_ref import CitizenRef
from ...domain.value_objects import NIF, BINumber, FullName
from ...domain.enums import Gender, MaritalStatus
from ..models.citizen_model import CitizenModel
from .base_repository import BaseRepository
from ...application.ports.citizen_repository_port import CitizenRepositoryPort


class CitizenRepository(BaseRepository[CitizenModel], CitizenRepositoryPort):
    """Implementação do repositório de cidadãos"""
    
    def __init__(self, db: Session):
        super().__init__(db, CitizenModel)
    
    def save(self, citizen: CitizenRef) -> CitizenRef:
        """Salva ou atualiza cidadão"""
        # Converte domain para model
        model_data = {
            "id": citizen.id,
            "nif": str(citizen.nif) if citizen.nif else None,
            "bi_number": str(citizen.bi_number) if citizen.bi_number else None,
            "full_name": str(citizen.full_name) if citizen.full_name else None,
            "first_names": citizen.full_name.first_names if citizen.full_name else None,
            "last_names": citizen.full_name.last_names if citizen.full_name else None,
            "birth_date": citizen.birth_date,
            "gender": citizen.gender.value if citizen.gender else None,
            "mother_name": citizen.mother_name,
            "father_name": citizen.father_name,
            "marital_status": citizen.marital_status.value if citizen.marital_status else None,
            "profession": citizen.profession,
            "phone": citizen.phone,
            "email": citizen.email,
            "address": citizen.address
        }
        
        # Verifica se já existe
        existing = super().get_by_id(citizen.id)
        if existing:
            # Atualiza
            for key, value in model_data.items():
                if value is not None:
                    setattr(existing, key, value)
            self.db.flush()
            return self._to_domain(existing)
        else:
            # Cria novo
            model = self.create(**model_data)
            self.db.flush()
            return self._to_domain(model)
    
    def get_by_id(self, citizen_id: str) -> Optional[CitizenRef]:
        """Busca cidadão por ID"""
        model = super().get_by_id(citizen_id)
        return self._to_domain(model) if model else None
    
    def get_by_nif(self, nif: NIF) -> Optional[CitizenRef]:
        """Busca cidadão por NIF"""
        model = self.db.query(CitizenModel).filter(
            CitizenModel.nif == str(nif),
            CitizenModel.is_active == True
        ).first()
        return self._to_domain(model) if model else None
    
    def get_by_bi(self, bi_number: BINumber) -> Optional[CitizenRef]:
        """Busca cidadão por número do BI"""
        model = self.db.query(CitizenModel).filter(
            CitizenModel.bi_number == str(bi_number),
            CitizenModel.is_active == True
        ).first()
        return self._to_domain(model) if model else None
    
    def get_by_name(self, name: str, limit: int = 10) -> List[CitizenRef]:
        """Busca cidadãos por nome (aproximado)"""
        models = self.db.query(CitizenModel).filter(
            CitizenModel.full_name.ilike(f"%{name}%"),
            CitizenModel.is_active == True
        ).limit(limit).all()
        return [self._to_domain(m) for m in models]
    
    def update_from_fuc(self, citizen_id: str, fuc_data: dict) -> Optional[CitizenRef]:
        """Atualiza dados do cidadão a partir do FUC"""
        model = super().get_by_id(citizen_id)
        if not model:
            return None
        
        # Mapeia campos do FUC
        if fuc_data.get("name"):
            model.full_name = fuc_data["name"]
        if fuc_data.get("first_names"):
            model.first_names = fuc_data["first_names"]
        if fuc_data.get("last_names"):
            model.last_names = fuc_data["last_names"]
        if fuc_data.get("birth_date"):
            model.birth_date = fuc_data["birth_date"]
        if fuc_data.get("gender"):
            model.gender = fuc_data["gender"]
        if fuc_data.get("mother"):
            model.mother_name = fuc_data["mother"]
        if fuc_data.get("father"):
            model.father_name = fuc_data["father"]
        
        model.fuc_synced_at = func.now()
        model.fuc_data = fuc_data
        
        self.db.flush()
        return self._to_domain(model)
    
    def delete(self, citizen_id: str) -> bool:
        """Remove cidadão da projeção local"""
        return super().delete(citizen_id, soft_delete=True)
    
    def _to_domain(self, model: CitizenModel) -> Optional[CitizenRef]:
        """Converte model para domain object"""
        if not model:
            return None
        
        return CitizenRef(
            id=model.id,
            nif=NIF(model.nif) if model.nif else None,
            bi_number=BINumber(model.bi_number) if model.bi_number else None,
            full_name=FullName(model.first_names, model.last_names) if model.first_names and model.last_names else None,
            birth_date=model.birth_date,
            gender=Gender(model.gender) if model.gender else None,
            mother_name=model.mother_name,
            father_name=model.father_name,
            marital_status=MaritalStatus(model.marital_status) if model.marital_status else None,
            profession=model.profession,
            phone=model.phone,
            email=model.email,
            address=model.address
        )
