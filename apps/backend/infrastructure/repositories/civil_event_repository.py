from typing import Optional, List, Union, Type
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from ...domain.models.civil_event import CivilEvent
from ...domain.models.birth_record import BirthRecord
from ...domain.models.death_record import DeathRecord
from ...domain.models.marriage_record import MarriageRecord
from ...domain.enums import CivilEventType, EventStatus, MaritalStatus
from ...domain.value_objects import EventNumber, Place, RegistryOffice
from ...domain.models.marriage_record import MarriagePropertyRegime
from ..models.civil_event_model import CivilEventModel, BirthModel, DeathModel, MarriageModel
from .base_repository import BaseRepository
from ...application.ports.civil_event_repository_port import CivilEventRepositoryPort


class CivilEventRepository(BaseRepository[CivilEventModel], CivilEventRepositoryPort):
    """Implementação do repositório de eventos civis"""
    
    def __init__(self, db: Session):
        super().__init__(db, CivilEventModel)
        self._model_map = {
            CivilEventType.BIRTH: BirthModel,
            CivilEventType.DEATH: DeathModel,
            CivilEventType.MARRIAGE: MarriageModel,
        }
        self._domain_map = {
            CivilEventType.BIRTH: BirthRecord,
            CivilEventType.DEATH: DeathRecord,
            CivilEventType.MARRIAGE: MarriageRecord,
        }
    
    def save(self, event: CivilEvent) -> CivilEvent:
        """Salva um evento (cria ou atualiza)"""
        # Converte domain para model
        if isinstance(event, BirthRecord):
            model = self._birth_to_model(event)
        elif isinstance(event, DeathRecord):
            model = self._death_to_model(event)
        elif isinstance(event, MarriageRecord):
            model = self._marriage_to_model(event)
        else:
            raise ValueError(f"Tipo de evento não suportado: {type(event)}")
        
        # Verifica se já existe
        existing = super().get_by_id(event.id)
        if existing:
            # Atualiza
            return self._update_existing(model, event.id)
        else:
            # Cria novo
            self.db.add(model)
            self.db.flush()
            return self._to_domain(model)
    
    def get_by_id(self, event_id: str) -> Optional[CivilEvent]:
        """Busca evento por ID"""
        model = super().get_by_id(event_id)
        return self._to_domain(model) if model else None
    
    def get_by_number(self, event_number: EventNumber) -> Optional[CivilEvent]:
        """Busca evento por número"""
        model = self.db.query(CivilEventModel).filter(
            CivilEventModel.event_number == str(event_number),
            CivilEventModel.is_active == True
        ).first()
        return self._to_domain(model) if model else None
    
    def get_by_citizen_id(self, citizen_id: str, 
                          event_type: Optional[CivilEventType] = None,
                          limit: int = 100) -> List[CivilEvent]:
        """Busca eventos por ID do cidadão"""
        # Busca em todas as tabelas de eventos
        birth_query = self.db.query(BirthModel).filter(
            or_(
                BirthModel.mother_id == citizen_id,
                BirthModel.father_id == citizen_id,
                BirthModel.declarant_id == citizen_id
            ),
            BirthModel.is_active == True
        )
        
        death_query = self.db.query(DeathModel).filter(
            or_(
                DeathModel.deceased_id == citizen_id,
                DeathModel.spouse_id == citizen_id,
                DeathModel.declarant_id == citizen_id
            ),
            DeathModel.is_active == True
        )
        
        marriage_query = self.db.query(MarriageModel).filter(
            or_(
                MarriageModel.spouse1_id == citizen_id,
                MarriageModel.spouse2_id == citizen_id
            ),
            MarriageModel.is_active == True
        )
        
        # Aplica filtro por tipo se especificado
        if event_type == CivilEventType.BIRTH:
            models = birth_query.limit(limit).all()
        elif event_type == CivilEventType.DEATH:
            models = death_query.limit(limit).all()
        elif event_type == CivilEventType.MARRIAGE:
            models = marriage_query.limit(limit).all()
        else:
            # Combina todos
            birth_models = birth_query.limit(limit).all()
            death_models = death_query.limit(limit).all()
            marriage_models = marriage_query.limit(limit).all()
            models = birth_models + death_models + marriage_models
        
        return [self._to_domain(m) for m in models]
    
    def get_by_date_range(self, start_date: date, end_date: date,
                          event_type: Optional[CivilEventType] = None) -> List[CivilEvent]:
        """Busca eventos por intervalo de datas"""
        query = self.db.query(CivilEventModel).filter(
            CivilEventModel.event_date.between(start_date, end_date),
            CivilEventModel.is_active == True
        )
        
        if event_type:
            query = query.filter(CivilEventModel.event_type == event_type)
        
        models = query.all()
        return [self._to_domain(m) for m in models]
    
    def get_by_status(self, status: EventStatus, limit: int = 100) -> List[CivilEvent]:
        """Busca eventos por status"""
        models = self.db.query(CivilEventModel).filter(
            CivilEventModel.status == status,
            CivilEventModel.is_active == True
        ).limit(limit).all()
        return [self._to_domain(m) for m in models]
    
    def get_birth_by_mother(self, mother_id: str, limit: int = 10) -> List[BirthRecord]:
        """Busca nascimentos por ID da mãe"""
        models = self.db.query(BirthModel).filter(
            BirthModel.mother_id == mother_id,
            BirthModel.is_active == True
        ).limit(limit).all()
        return [self._to_domain(m) for m in models]
    
    def get_death_by_spouse(self, spouse_id: str) -> List[DeathRecord]:
        """Busca óbitos por ID do cônjuge"""
        models = self.db.query(DeathModel).filter(
            DeathModel.spouse_id == spouse_id,
            DeathModel.is_active == True
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_marriage_by_spouse(self, spouse_id: str) -> List[MarriageRecord]:
        """Busca casamentos por ID do cônjuge"""
        models = self.db.query(MarriageModel).filter(
            or_(
                MarriageModel.spouse1_id == spouse_id,
                MarriageModel.spouse2_id == spouse_id
            ),
            MarriageModel.is_active == True
        ).all()
        return [self._to_domain(m) for m in models]
    
    def update_status(self, event_id: str, status: EventStatus, 
                     user_id: str, reason: Optional[str] = None) -> Optional[CivilEvent]:
        """Atualiza status do evento"""
        model = super().get_by_id(event_id)
        if not model:
            return None
        
        model.status = status.value if hasattr(status, 'value') else status
        model.updated_by = user_id
        if reason:
            model.notes = (model.notes or "") + f"\n[{datetime.now().isoformat()}] Status alterado para {status}: {reason}"
        
        self.db.flush()
        return self._to_domain(model)
    
    def get_next_sequence_number(self, year: int, event_type: str) -> int:
        """Obtém próximo número sequencial para evento"""
        type_prefix = {
            "NASCIMENTO": "NASC",
            "OBITO": "OBITO", 
            "CASAMENTO": "CASA"
        }.get(event_type.upper(), "EVT")
        
        pattern = f"{year}/{type_prefix}/%"
        
        count = self.db.query(CivilEventModel).filter(
            CivilEventModel.event_number.like(pattern)
        ).count()
        
        return count + 1
    
    def count_by_period(self, start_date: date, end_date: date,
                        event_type: Optional[CivilEventType] = None) -> int:
        """Conta eventos no período"""
        query = self.db.query(CivilEventModel).filter(
            CivilEventModel.event_date.between(start_date, end_date),
            CivilEventModel.is_active == True
        )
        
        if event_type:
            query = query.filter(CivilEventModel.event_type == event_type)
        
        return query.count()
    
    def exists_by_citizen_and_type(self, citizen_id: str, 
                                   event_type: CivilEventType) -> bool:
        """Verifica se já existe evento do tipo para o cidadão"""
        if event_type == CivilEventType.BIRTH:
            return self.db.query(BirthModel).filter(
                or_(
                    BirthModel.mother_id == citizen_id,
                    BirthModel.father_id == citizen_id
                )
            ).first() is not None
        elif event_type == CivilEventType.DEATH:
            return self.db.query(DeathModel).filter(
                DeathModel.deceased_id == citizen_id
            ).first() is not None
        elif event_type == CivilEventType.MARRIAGE:
            return self.db.query(MarriageModel).filter(
                or_(
                    MarriageModel.spouse1_id == citizen_id,
                    MarriageModel.spouse2_id == citizen_id
                )
            ).first() is not None
        return False
    
    def _to_domain(self, model: Union[CivilEventModel, BirthModel, DeathModel, MarriageModel]) -> Optional[CivilEvent]:
        """Converte model para domain object"""
        if not model:
            return None
        
        if isinstance(model, BirthModel):
            return self._model_to_birth(model)
        elif isinstance(model, DeathModel):
            return self._model_to_death(model)
        elif isinstance(model, MarriageModel):
            return self._model_to_marriage(model)
        return None
    
    def _model_to_birth(self, model: BirthModel) -> BirthRecord:
        """Converte BirthModel para BirthRecord"""
        return BirthRecord(
            id=model.id,
            event_number=EventNumber(model.event_number) if model.event_number else None,
            event_date=model.event_date,
            registry_office=RegistryOffice(
                name=model.registry_office_name,
                code=model.registry_office_code,
                province=model.registry_office_province,
                municipality=model.registry_office_municipality
            ) if model.registry_office_code else None,
            status=EventStatus(model.status) if isinstance(model.status, str) else model.status,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
            updated_by=model.updated_by,
            metadata=model.metadata,
            
            # Dados específicos
            child_first_names=model.child_first_names,
            child_last_names=model.child_last_names,
            child_gender=model.child_gender,
            child_birth_date=model.child_birth_date,
            child_birth_time=model.child_birth_time,
            child_birth_place=Place(
                province=model.birth_province,
                municipality=model.birth_municipality,
                commune=model.birth_commune,
                locality=model.birth_locality
            ) if model.birth_province else None,
            
            mother_id=model.mother_id,
            mother_name=model.mother_name,
            mother_age=model.mother_age,
            mother_nationality=model.mother_nationality,
            mother_profession=model.mother_profession,
            mother_marital_status=model.mother_marital_status,
            
            father_id=model.father_id,
            father_name=model.father_name,
            father_age=model.father_age,
            father_nationality=model.father_nationality,
            father_profession=model.father_profession,
            
            is_late_registration=model.is_late_registration,
            late_registration_years=model.late_registration_years,
            declarant_name=model.declarant_name,
            declarant_id=model.declarant_id,
            declarant_relationship=model.declarant_relationship,
            
            witness1_name=model.witness1_name,
            witness1_id=model.witness1_id,
            witness2_name=model.witness2_name,
            witness2_id=model.witness2_id,
            
            birth_institution=model.birth_institution,
            birth_institution_code=model.birth_institution_code,
            doctor_name=model.doctor_name,
            doctor_registry=model.doctor_registry
        )
    
    def _birth_to_model(self, birth: BirthRecord) -> BirthModel:
        """Converte BirthRecord para BirthModel"""
        model = BirthModel(
            id=birth.id,
            event_number=str(birth.event_number) if birth.event_number else None,
            event_type=CivilEventType.BIRTH.value,
            event_date=birth.event_date,
            status=birth.status.value if hasattr(birth.status, 'value') else birth.status,
            notes=birth.notes,
            created_at=birth.created_at,
            updated_at=birth.updated_at,
            created_by=birth.created_by,
            updated_by=birth.updated_by,
            metadata=birth.metadata,
            
            # Registry office
            registry_office_name=birth.registry_office.name if birth.registry_office else None,
            registry_office_code=birth.registry_office.code if birth.registry_office else None,
            registry_office_province=birth.registry_office.province if birth.registry_office else None,
            registry_office_municipality=birth.registry_office.municipality if birth.registry_office else None,
            
            # Dados específicos
            child_first_names=birth.child_first_names,
            child_last_names=birth.child_last_names,
            child_gender=birth.child_gender.value if birth.child_gender else None,
            child_birth_date=birth.child_birth_date,
            child_birth_time=birth.child_birth_time,
            
            birth_province=birth.child_birth_place.province if birth.child_birth_place else None,
            birth_municipality=birth.child_birth_place.municipality if birth.child_birth_place else None,
            birth_commune=birth.child_birth_place.commune if birth.child_birth_place else None,
            birth_locality=birth.child_birth_place.locality if birth.child_birth_place else None,
            
            mother_id=birth.mother_id,
            mother_name=birth.mother_name,
            mother_age=birth.mother_age,
            mother_nationality=birth.mother_nationality,
            mother_profession=birth.mother_profession,
            mother_marital_status=birth.mother_marital_status,
            
            father_id=birth.father_id,
            father_name=birth.father_name,
            father_age=birth.father_age,
            father_nationality=birth.father_nationality,
            father_profession=birth.father_profession,
            
            is_late_registration=birth.is_late_registration,
            late_registration_years=birth.late_registration_years,
            declarant_name=birth.declarant_name,
            declarant_id=birth.declarant_id,
            declarant_relationship=birth.declarant_relationship,
            
            witness1_name=birth.witness1_name,
            witness1_id=birth.witness1_id,
            witness2_name=birth.witness2_name,
            witness2_id=birth.witness2_id,
            
            birth_institution=birth.birth_institution,
            birth_institution_code=birth.birth_institution_code,
            doctor_name=birth.doctor_name,
            doctor_registry=birth.doctor_registry
        )
        return model
    
    def _model_to_death(self, model: DeathModel) -> DeathRecord:
        """Converte DeathModel para DeathRecord"""
        return DeathRecord(
            id=model.id,
            event_number=EventNumber(model.event_number) if model.event_number else None,
            event_date=model.event_date,
            registry_office=RegistryOffice(
                name=model.registry_office_name,
                code=model.registry_office_code,
                province=model.registry_office_province,
                municipality=model.registry_office_municipality
            ) if model.registry_office_code else None,
            status=EventStatus(model.status) if isinstance(model.status, str) else model.status,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
            updated_by=model.updated_by,
            metadata=model.metadata,
            
            deceased_id=model.deceased_id,
            deceased_name=model.deceased_name,
            deceased_birth_date=model.deceased_birth_date,
            deceased_age=model.deceased_age,
            deceased_gender=model.deceased_gender,
            deceased_marital_status=model.deceased_marital_status,
            deceased_nationality=model.deceased_nationality,
            deceased_profession=model.deceased_profession,
            deceased_address=model.deceased_address,
            
            death_date=model.death_date,
            death_time=model.death_time,
            death_place=Place(
                province=model.death_province,
                municipality=model.death_municipality,
                commune=model.death_commune,
                locality=model.death_locality
            ) if model.death_province else None,
            death_cause=model.death_cause,
            death_certificate_number=model.death_certificate_number,
            death_certificate_issuer=model.death_certificate_issuer,
            
            spouse_id=model.spouse_id,
            spouse_name=model.spouse_name,
            
            mother_name=model.mother_name,
            father_name=model.father_name,
            
            declarant_name=model.declarant_name,
            declarant_id=model.declarant_id,
            declarant_relationship=model.declarant_relationship,
            
            burial_place=model.burial_place,
            burial_date=model.burial_date,
            cemetery_name=model.cemetery_name,
            grave_number=model.grave_number
        )
    
    def _death_to_model(self, death: DeathRecord) -> DeathModel:
        """Converte DeathRecord para DeathModel"""
        model = DeathModel(
            id=death.id,
            event_number=str(death.event_number) if death.event_number else None,
            event_type=CivilEventType.DEATH.value,
            event_date=death.event_date,
            status=death.status.value if hasattr(death.status, 'value') else death.status,
            notes=death.notes,
            created_at=death.created_at,
            updated_at=death.updated_at,
            created_by=death.created_by,
            updated_by=death.updated_by,
            metadata=death.metadata,
            
            registry_office_name=death.registry_office.name if death.registry_office else None,
            registry_office_code=death.registry_office.code if death.registry_office else None,
            registry_office_province=death.registry_office.province if death.registry_office else None,
            registry_office_municipality=death.registry_office.municipality if death.registry_office else None,
            
            deceased_id=death.deceased_id,
            deceased_name=death.deceased_name,
            deceased_birth_date=death.deceased_birth_date,
            deceased_age=death.deceased_age,
            deceased_gender=death.deceased_gender,
            deceased_marital_status=death.deceased_marital_status,
            deceased_nationality=death.deceased_nationality,
            deceased_profession=death.deceased_profession,
            deceased_address=death.deceased_address,
            
            death_date=death.death_date,
            death_time=death.death_time,
            death_province=death.death_place.province if death.death_place else None,
            death_municipality=death.death_place.municipality if death.death_place else None,
            death_commune=death.death_place.commune if death.death_place else None,
            death_locality=death.death_place.locality if death.death_place else None,
            death_cause=death.death_cause,
            death_certificate_number=death.death_certificate_number,
            death_certificate_issuer=death.death_certificate_issuer,
            
            spouse_id=death.spouse_id,
            spouse_name=death.spouse_name,
            
            mother_name=death.mother_name,
            father_name=death.father_name,
            
            declarant_name=death.declarant_name,
            declarant_id=death.declarant_id,
            declarant_relationship=death.declarant_relationship,
            
            burial_place=death.burial_place,
            burial_date=death.burial_date,
            cemetery_name=death.cemetery_name,
            grave_number=death.grave_number
        )
        return model
    
    def _model_to_marriage(self, model: MarriageModel) -> MarriageRecord:
        """Converte MarriageModel para MarriageRecord"""
        return MarriageRecord(
            id=model.id,
            event_number=EventNumber(model.event_number) if model.event_number else None,
            event_date=model.event_date,
            registry_office=RegistryOffice(
                name=model.registry_office_name,
                code=model.registry_office_code,
                province=model.registry_office_province,
                municipality=model.registry_office_municipality
            ) if model.registry_office_code else None,
            status=EventStatus(model.status) if isinstance(model.status, str) else model.status,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
            updated_by=model.updated_by,
            metadata=model.metadata,
            
            spouse1_id=model.spouse1_id,
            spouse1_name=model.spouse1_name,
            spouse1_birth_date=model.spouse1_birth_date,
            spouse1_age=model.spouse1_age,
            spouse1_nationality=model.spouse1_nationality,
            spouse1_profession=model.spouse1_profession,
            spouse1_address=model.spouse1_address,
            spouse1_marital_status=MaritalStatus(model.spouse1_marital_status) if model.spouse1_marital_status else None,
            spouse1_father_name=model.spouse1_father_name,
            spouse1_mother_name=model.spouse1_mother_name,
            
            spouse2_id=model.spouse2_id,
            spouse2_name=model.spouse2_name,
            spouse2_birth_date=model.spouse2_birth_date,
            spouse2_age=model.spouse2_age,
            spouse2_nationality=model.spouse2_nationality,
            spouse2_profession=model.spouse2_profession,
            spouse2_address=model.spouse2_address,
            spouse2_marital_status=MaritalStatus(model.spouse2_marital_status) if model.spouse2_marital_status else None,
            spouse2_father_name=model.spouse2_father_name,
            spouse2_mother_name=model.spouse2_mother_name,
            
            marriage_date=model.marriage_date,
            marriage_place=Place(
                province=model.marriage_province,
                municipality=model.marriage_municipality,
                commune=model.marriage_commune,
                locality=model.marriage_locality
            ) if model.marriage_province else None,
            property_regime=MarriagePropertyRegime(model.property_regime) if model.property_regime else None,
            has_prenuptial_agreement=model.has_prenuptial_agreement,
            prenuptial_agreement_number=model.prenuptial_agreement_number,
            
            celebrant_name=model.celebrant_name,
            celebrant_id=model.celebrant_id,
            celebrant_title=model.celebrant_title,
            
            witness1_name=model.witness1_name,
            witness1_id=model.witness1_id,
            witness2_name=model.witness2_name,
            witness2_id=model.witness2_id,
            
            consent_father_spouse1=model.consent_father_spouse1,
            consent_mother_spouse1=model.consent_mother_spouse1,
            consent_father_spouse2=model.consent_father_spouse2,
            consent_mother_spouse2=model.consent_mother_spouse2
        )
    
    def _marriage_to_model(self, marriage: MarriageRecord) -> MarriageModel:
        """Converte MarriageRecord para MarriageModel"""
        model = MarriageModel(
            id=marriage.id,
            event_number=str(marriage.event_number) if marriage.event_number else None,
            event_type=CivilEventType.MARRIAGE.value,
            event_date=marriage.event_date,
            status=marriage.status.value if hasattr(marriage.status, 'value') else marriage.status,
            notes=marriage.notes,
            created_at=marriage.created_at,
            updated_at=marriage.updated_at,
            created_by=marriage.created_by,
            updated_by=marriage.updated_by,
            metadata=marriage.metadata,
            
            registry_office_name=marriage.registry_office.name if marriage.registry_office else None,
            registry_office_code=marriage.registry_office.code if marriage.registry_office else None,
            registry_office_province=marriage.registry_office.province if marriage.registry_office else None,
            registry_office_municipality=marriage.registry_office.municipality if marriage.registry_office else None,
            
            spouse1_id=marriage.spouse1_id,
            spouse1_name=marriage.spouse1_name,
            spouse1_birth_date=marriage.spouse1_birth_date,
            spouse1_age=marriage.spouse1_age,
            spouse1_nationality=marriage.spouse1_nationality,
            spouse1_profession=marriage.spouse1_profession,
            spouse1_address=marriage.spouse1_address,
            spouse1_marital_status=marriage.spouse1_marital_status.value if marriage.spouse1_marital_status else None,
            spouse1_father_name=marriage.spouse1_father_name,
            spouse1_mother_name=marriage.spouse1_mother_name,
            
            spouse2_id=marriage.spouse2_id,
            spouse2_name=marriage.spouse2_name,
            spouse2_birth_date=marriage.spouse2_birth_date,
            spouse2_age=marriage.spouse2_age,
            spouse2_nationality=marriage.spouse2_nationality,
            spouse2_profession=marriage.spouse2_profession,
            spouse2_address=marriage.spouse2_address,
            spouse2_marital_status=marriage.spouse2_marital_status.value if marriage.spouse2_marital_status else None,
            spouse2_father_name=marriage.spouse2_father_name,
            spouse2_mother_name=marriage.spouse2_mother_name,
            
            marriage_date=marriage.marriage_date,
            marriage_province=marriage.marriage_place.province if marriage.marriage_place else None,
            marriage_municipality=marriage.marriage_place.municipality if marriage.marriage_place else None,
            marriage_commune=marriage.marriage_place.commune if marriage.marriage_place else None,
            marriage_locality=marriage.marriage_place.locality if marriage.marriage_place else None,
            property_regime=marriage.property_regime.value if marriage.property_regime else None,
            has_prenuptial_agreement=marriage.has_prenuptial_agreement,
            prenuptial_agreement_number=marriage.prenuptial_agreement_number,
            
            celebrant_name=marriage.celebrant_name,
            celebrant_id=marriage.celebrant_id,
            celebrant_title=marriage.celebrant_title,
            
            witness1_name=marriage.witness1_name,
            witness1_id=marriage.witness1_id,
            witness2_name=marriage.witness2_name,
            witness2_id=marriage.witness2_id,
            
            consent_father_spouse1=marriage.consent_father_spouse1,
            consent_mother_spouse1=marriage.consent_mother_spouse1,
            consent_father_spouse2=marriage.consent_father_spouse2,
            consent_mother_spouse2=marriage.consent_mother_spouse2
        )
        return model
    
    def _update_existing(self, new_model: CivilEventModel, event_id: str) -> CivilEvent:
        """Atualiza evento existente"""
        existing = super().get_by_id(event_id)
        if not existing:
            self.db.add(new_model)
        else:
            # Atualiza campos
            for key, value in new_model.__dict__.items():
                if not key.startswith('_') and value is not None:
                    setattr(existing, key, value)
            self.db.flush()
            new_model = existing
        
        return self._to_domain(new_model)
