from typing import Optional, List, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session

from ...domain.models.birth_record import BirthRecord
from ...domain.models.citizen_ref import CitizenRef
from ...domain.enums import EventStatus
from ...domain.value_objects import RegistryOffice, Place
from .base_service import BaseService


class BirthService(BaseService[BirthRecord]):
    """Serviço para registo de nascimentos"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def create_birth_registration(self, data: Dict[str, Any], user_id: str) -> BirthRecord:
        """
        Cria um novo registo de nascimento
        Fluxo completo: validação → criação → certificado → FUC
        """
        try:
            # 1. Validar dados
            self._validate_birth_data(data)
            
            # 2. Iniciar transação
            with self.uow_factory.create() as uow:
                # 3. Verificar/criar cidadãos
                mother = self._get_or_create_citizen(data['mother_id'], user_id)
                father = None
                if data.get('father_id'):
                    father = self._get_or_create_citizen(data['father_id'], user_id)
                
                # 4. Criar registo de nascimento
                birth_record = self._create_birth_record(data, mother, father, user_id)
                
                # 5. Gerar número de evento
                sequence = self.event_repo.get_next_sequence_number(
                    birth_record.event_date.year, "NASCIMENTO"
                )
                birth_record.generate_event_number(sequence)
                
                # 6. Persistir evento
                saved_birth = self.event_repo.save(birth_record)
                
                # 7. Commit da transação
                uow.commit()
                
                # 8. Registrar auditoria
                self._log_action(
                    action="CREATE_BIRTH",
                    entity_id=saved_birth.id,
                    entity_type="BirthRecord",
                    user_id=user_id,
                    changes={"event_number": str(saved_birth.event_number)}
                )
                
                return saved_birth
                
        except Exception as e:
            self._handle_error(e, {"data": data, "user_id": user_id})
            raise
    
    def get_birth_by_id(self, birth_id: str) -> Optional[BirthRecord]:
        """Busca registo de nascimento por ID"""
        event = self.event_repo.get_by_id(birth_id)
        if event and isinstance(event, BirthRecord):
            return event
        return None
    
    def get_births_by_mother(self, mother_id: str, limit: int = 10) -> List[BirthRecord]:
        """Lista nascimentos por mãe"""
        return self.event_repo.get_birth_by_mother(mother_id, limit)
    
    def get_births_by_period(self, start_date: date, end_date: date) -> List[BirthRecord]:
        """Lista nascimentos por período"""
        from ...domain.enums import CivilEventType
        events = self.event_repo.get_by_date_range(start_date, end_date, CivilEventType.BIRTH)
        return [e for e in events if isinstance(e, BirthRecord)]
    
    def update_birth_registration(self, birth_id: str, data: Dict[str, Any], 
                                  user_id: str) -> Optional[BirthRecord]:
        """Atualiza registo de nascimento"""
        birth = self.get_birth_by_id(birth_id)
        if not birth:
            raise ValueError(f"Nascimento {birth_id} não encontrado")
        
        if birth.status != EventStatus.PENDING:
            raise ValueError(f"Não é possível alterar registo com status {birth.status}")
        
        with self.uow_factory.create() as uow:
            # Atualiza campos permitidos
            if data.get('child_first_names'):
                birth.child_first_names = data['child_first_names']
            if data.get('child_last_names'):
                birth.child_last_names = data['child_last_names']
            if data.get('notes'):
                birth.notes = data['notes']
            
            birth.updated_at = datetime.now()
            birth.updated_by = user_id
            
            updated = self.event_repo.save(birth)
            uow.commit()
            
            self._log_action(
                action="UPDATE_BIRTH",
                entity_id=birth_id,
                entity_type="BirthRecord",
                user_id=user_id,
                changes=data
            )
            
            return updated
    
    def cancel_birth_registration(self, birth_id: str, reason: str, 
                                  user_id: str) -> Optional[BirthRecord]:
        """Cancela registo de nascimento"""
        birth = self.get_birth_by_id(birth_id)
        if not birth:
            raise ValueError(f"Nascimento {birth_id} não encontrado")
        
        with self.uow_factory.create() as uow:
            birth.cancel(reason, user_id)
            updated = self.event_repo.save(birth)
            uow.commit()
            
            self._log_action(
                action="CANCEL_BIRTH",
                entity_id=birth_id,
                entity_type="BirthRecord",
                user_id=user_id,
                changes={"reason": reason}
            )
            
            return updated
    
    def _validate_birth_data(self, data: Dict[str, Any]):
        """Valida dados de nascimento"""
        required_fields = [
            'child_first_names', 'child_last_names', 'child_gender', 
            'child_birth_date', 'mother_id', 'declarant_name', 'declarant_relationship'
        ]
        
        missing = [f for f in required_fields if f not in data or not data[f]]
        if missing:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(missing)}")
    
    def _get_or_create_citizen(self, citizen_id: str, user_id: str) -> CitizenRef:
        """Obtém ou cria cidadão"""
        citizen = self.citizen_repo.get_by_id(citizen_id)
        
        if not citizen:
            raise ValueError(f"Cidadão {citizen_id} não encontrado")
        
        return citizen
    
    def _create_birth_record(self, data: Dict[str, Any], mother: CitizenRef, 
                            father: Optional[CitizenRef], user_id: str) -> BirthRecord:
        """Cria instância de BirthRecord"""
        birth_place = Place(
            province=data.get('birth_province', 'LUANDA'),
            municipality=data.get('birth_municipality'),
            commune=data.get('birth_commune'),
            locality=data.get('birth_locality')
        )
        
        registry_office = RegistryOffice(
            name=data.get('registry_office_name', 'Conservatória do Registo Civil'),
            code=data.get('registry_office_code', '00101'),
            province=data.get('registry_office_province', 'LUANDA'),
            municipality=data.get('registry_office_municipality', 'LUANDA')
        )
        
        return BirthRecord(
            child_first_names=data['child_first_names'],
            child_last_names=data['child_last_names'],
            child_gender=data['child_gender'],
            child_birth_date=data['child_birth_date'],
            child_birth_time=data.get('child_birth_time'),
            child_birth_place=birth_place,
            mother_id=mother.id,
            mother_name=mother.full_name.full if mother.full_name else data['mother_name'],
            mother_age=data.get('mother_age'),
            mother_nationality=data.get('mother_nationality', 'ANGOLANA'),
            mother_profession=data.get('mother_profession'),
            mother_marital_status=data.get('mother_marital_status'),
            father_id=father.id if father else None,
            father_name=father.full_name.full if father else data.get('father_name'),
            father_age=data.get('father_age'),
            father_nationality=data.get('father_nationality', 'ANGOLANA'),
            father_profession=data.get('father_profession'),
            is_late_registration=data.get('is_late_registration', False),
            late_registration_years=data.get('late_registration_years'),
            declarant_name=data['declarant_name'],
            declarant_id=data.get('declarant_id'),
            declarant_relationship=data['declarant_relationship'],
            witness1_name=data.get('witness1_name'),
            witness1_id=data.get('witness1_id'),
            witness2_name=data.get('witness2_name'),
            witness2_id=data.get('witness2_id'),
            birth_institution=data.get('birth_institution'),
            birth_institution_code=data.get('birth_institution_code'),
            doctor_name=data.get('doctor_name'),
            doctor_registry=data.get('doctor_registry'),
            registry_office=registry_office,
            event_date=data.get('event_date', date.today()),
            created_by=user_id
        )
