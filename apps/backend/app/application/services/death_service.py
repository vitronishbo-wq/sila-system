from typing import Optional, List, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session

from ...domain.models.death_record import DeathRecord
from ...domain.models.citizen_ref import CitizenRef
from ...domain.enums import EventStatus, CertificateType, CivilEventType
from ...domain.value_objects import EventNumber, RegistryOffice, Place
from .base_service import BaseService


class DeathService(BaseService[DeathRecord]):
    """Serviço para registo de óbitos"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def create_death_registration(self, data: Dict[str, Any], user_id: str) -> DeathRecord:
        """Cria um novo registo de óbito"""
        try:
            # 1. Validar dados
            self._validate_death_data(data)
            
            # 2. Iniciar transação
            with self.uow_factory.create() as uow:
                # 3. Verificar falecido
                deceased = self._get_citizen(data['deceased_id'])
                
                # 4. Verificar cônjuge se existir
                spouse = None
                if data.get('spouse_id'):
                    spouse = self._get_citizen(data['spouse_id'])
                
                # 5. Criar registo de óbito
                death_record = self._create_death_record(data, deceased, spouse, user_id)
                
                # 6. Gerar número de evento
                sequence = self.event_repo.get_next_sequence_number(
                    death_record.event_date.year, "OBITO"
                )
                death_record.generate_event_number(sequence)
                
                # 7. Persistir evento
                saved_death = self.event_repo.save(death_record)
                
                # 8. Commit
                uow.commit()
                
                self._log_action(
                    action="CREATE_DEATH",
                    entity_id=saved_death.id,
                    entity_type="DeathRecord",
                    user_id=user_id
                )
                
                return saved_death
                
        except Exception as e:
            self._handle_error(e, {"data": data, "user_id": user_id})
            raise
    
    def get_death_by_id(self, death_id: str) -> Optional[DeathRecord]:
        """Busca registo de óbito por ID"""
        event = self.event_repo.get_by_id(death_id)
        if event and isinstance(event, DeathRecord):
            return event
        return None
    
    def get_deaths_by_period(self, start_date: date, end_date: date) -> List[DeathRecord]:
        """Lista óbitos por período"""
        events = self.event_repo.get_by_date_range(start_date, end_date, CivilEventType.DEATH)
        return [e for e in events if isinstance(e, DeathRecord)]
    
    def get_death_by_citizen(self, citizen_id: str) -> Optional[DeathRecord]:
        """Busca óbito de um cidadão específico"""
        events = self.event_repo.get_by_citizen_id(citizen_id, CivilEventType.DEATH)
        return events[0] if events else None
    
    def update_death_registration(self, death_id: str, data: Dict[str, Any],
                                  user_id: str) -> Optional[DeathRecord]:
        """Atualiza registo de óbito"""
        death = self.get_death_by_id(death_id)
        if not death:
            raise ValueError(f"Óbito {death_id} não encontrado")
        
        if death.status != EventStatus.PENDING:
            raise ValueError(f"Não é possível alterar registo com status {death.status}")
        
        with self.uow_factory.create() as uow:
            # Atualizar campos permitidos
            if data.get('death_cause'):
                death.death_cause = data['death_cause']
            if data.get('burial_place'):
                death.burial_place = data['burial_place']
            if data.get('cemetery_name'):
                death.cemetery_name = data['cemetery_name']
            if data.get('grave_number'):
                death.grave_number = data['grave_number']
            if data.get('notes'):
                death.notes = data['notes']
            
            death.updated_at = datetime.now()
            death.updated_by = user_id
            
            updated = self.event_repo.save(death)
            uow.commit()
            
            self._log_action(
                action="UPDATE_DEATH",
                entity_id=death_id,
                entity_type="DeathRecord",
                user_id=user_id,
                changes=data
            )
            
            return updated
    
    def _validate_death_data(self, data: Dict[str, Any]):
        """Valida dados de óbito"""
        required_fields = [
            'deceased_id', 'deceased_name', 'death_date', 'declarant_name', 'declarant_relationship'
        ]
        
        missing = [f for f in required_fields if f not in data or not data[f]]
        if missing:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(missing)}")
        
        # Verificar se cidadão já está registado como falecido
        existing = self.get_death_by_citizen(data['deceased_id'])
        if existing:
            raise ValueError(f"Cidadão já possui registo de óbito: {existing.event_number}")
    
    def _get_citizen(self, citizen_id: str) -> CitizenRef:
        """Obtém cidadão do repositório local"""
        citizen = self.citizen_repo.get_by_id(citizen_id)
        
        if not citizen:
            raise ValueError(f"Cidadão {citizen_id} não encontrado")
        
        return citizen
    
    def _create_death_record(self, data: Dict[str, Any], deceased: CitizenRef,
                            spouse: Optional[CitizenRef], user_id: str) -> DeathRecord:
        """Cria instância de DeathRecord"""
        death_place = Place(
            province=data.get('death_province', 'LUANDA'),
            municipality=data.get('death_municipality'),
            commune=data.get('death_commune'),
            locality=data.get('death_locality')
        )
        
        registry_office = RegistryOffice(
            name=data.get('registry_office_name', 'Conservatória do Registo Civil'),
            code=data.get('registry_office_code', '00101'),
            province=data.get('registry_office_province', 'LUANDA'),
            municipality=data.get('registry_office_municipality', 'LUANDA')
        )
        
        return DeathRecord(
            deceased_id=deceased.id,
            deceased_name=deceased.full_name.full if deceased.full_name else data['deceased_name'],
            deceased_birth_date=deceased.birth_date,
            deceased_age=data.get('deceased_age'),
            deceased_gender=deceased.gender.value if deceased.gender else data.get('deceased_gender'),
            deceased_marital_status=deceased.marital_status.value if deceased.marital_status else data.get('deceased_marital_status'),
            deceased_nationality=data.get('deceased_nationality', 'ANGOLANA'),
            deceased_profession=deceased.profession,
            deceased_address=deceased.address,
            death_date=data['death_date'],
            death_time=data.get('death_time'),
            death_place=death_place,
            death_cause=data.get('death_cause'),
            death_certificate_number=data.get('death_certificate_number'),
            death_certificate_issuer=data.get('death_certificate_issuer'),
            spouse_id=spouse.id if spouse else None,
            spouse_name=spouse.full_name.full if spouse else data.get('spouse_name'),
            mother_name=data.get('mother_name', deceased.mother_name),
            father_name=data.get('father_name', deceased.father_name),
            declarant_name=data['declarant_name'],
            declarant_id=data.get('declarant_id'),
            declarant_relationship=data['declarant_relationship'],
            burial_place=data.get('burial_place'),
            burial_date=data.get('burial_date'),
            cemetery_name=data.get('cemetery_name'),
            grave_number=data.get('grave_number'),
            registry_office=registry_office,
            event_date=data.get('event_date', date.today()),
            created_by=user_id
        )
