from typing import Optional, List, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session

from ...domain.models.marriage_record import MarriageRecord, MarriagePropertyRegime
from ...domain.models.citizen_ref import CitizenRef
from ...domain.enums import EventStatus, MaritalStatus, CivilEventType
from ...domain.value_objects import RegistryOffice, Place
from .base_service import BaseService


class MarriageService(BaseService[MarriageRecord]):
    """Serviço para registo de casamentos"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def create_marriage_registration(self, data: Dict[str, Any], user_id: str) -> MarriageRecord:
        """Cria um novo registo de casamento"""
        try:
            # 1. Validar dados
            self._validate_marriage_data(data)
            
            # 2. Iniciar transação
            with self.uow_factory.create() as uow:
                # 3. Verificar cônjuges
                spouse1 = self._get_citizen(data['spouse1_id'])
                spouse2 = self._get_citizen(data['spouse2_id'])
                
                # 4. Verificar capacidade legal para casar
                self._check_marriage_capacity(spouse1, spouse2, data)
                
                # 5. Criar registo de casamento
                marriage_record = self._create_marriage_record(data, spouse1, spouse2, user_id)
                
                # 6. Gerar número de evento
                sequence = self.event_repo.get_next_sequence_number(
                    marriage_record.event_date.year, "CASAMENTO"
                )
                marriage_record.generate_event_number(sequence)
                
                # 7. Persistir evento
                saved_marriage = self.event_repo.save(marriage_record)
                
                # 8. Commit
                uow.commit()
                
                self._log_action(
                    action="CREATE_MARRIAGE",
                    entity_id=saved_marriage.id,
                    entity_type="MarriageRecord",
                    user_id=user_id,
                    changes={
                        "spouse1": spouse1.id,
                        "spouse2": spouse2.id,
                        "event_number": str(saved_marriage.event_number)
                    }
                )
                
                return saved_marriage
                
        except Exception as e:
            self._handle_error(e, {"data": data, "user_id": user_id})
            raise
    
    def get_marriage_by_id(self, marriage_id: str) -> Optional[MarriageRecord]:
        """Busca registo de casamento por ID"""
        event = self.event_repo.get_by_id(marriage_id)
        if event and isinstance(event, MarriageRecord):
            return event
        return None
    
    def get_marriages_by_spouse(self, spouse_id: str) -> List[MarriageRecord]:
        """Lista casamentos de um cônjuge"""
        return self.event_repo.get_marriage_by_spouse(spouse_id)
    
    def get_marriages_by_period(self, start_date: date, end_date: date) -> List[MarriageRecord]:
        """Lista casamentos por período"""
        events = self.event_repo.get_by_date_range(start_date, end_date, CivilEventType.MARRIAGE)
        return [e for e in events if isinstance(e, MarriageRecord)]
    
    def get_current_marriage(self, citizen_id: str) -> Optional[MarriageRecord]:
        """Obtém o casamento atual (não divorciado) de um cidadão"""
        marriages = self.get_marriages_by_spouse(citizen_id)
        # Retorna o mais recente que não foi cancelado
        active_marriages = [
            m for m in marriages 
            if m.status not in [EventStatus.CANCELLED]
        ]
        return active_marriages[0] if active_marriages else None
    
    def update_marriage_registration(self, marriage_id: str, data: Dict[str, Any],
                                    user_id: str) -> Optional[MarriageRecord]:
        """Atualiza registo de casamento"""
        marriage = self.get_marriage_by_id(marriage_id)
        if not marriage:
            raise ValueError(f"Casamento {marriage_id} não encontrado")
        
        if marriage.status != EventStatus.PENDING:
            raise ValueError(f"Não é possível alterar registo com status {marriage.status}")
        
        with self.uow_factory.create() as uow:
            # Atualizar campos permitidos
            if data.get('property_regime') and marriage.status == EventStatus.PENDING:
                marriage.property_regime = MarriagePropertyRegime(data['property_regime'])
            if data.get('notes'):
                marriage.notes = data['notes']
            
            marriage.updated_at = datetime.now()
            marriage.updated_by = user_id
            
            updated = self.event_repo.save(marriage)
            uow.commit()
            
            self._log_action(
                action="UPDATE_MARRIAGE",
                entity_id=marriage_id,
                entity_type="MarriageRecord",
                user_id=user_id,
                changes=data
            )
            
            return updated
    
    def cancel_marriage_registration(self, marriage_id: str, reason: str,
                                     user_id: str) -> Optional[MarriageRecord]:
        """Cancela registo de casamento (antes da celebração)"""
        marriage = self.get_marriage_by_id(marriage_id)
        if not marriage:
            raise ValueError(f"Casamento {marriage_id} não encontrado")
        
        if marriage.status != EventStatus.PENDING:
            raise ValueError(f"Não é possível cancelar registo com status {marriage.status}")
        
        with self.uow_factory.create() as uow:
            marriage.cancel(reason, user_id)
            
            updated = self.event_repo.save(marriage)
            uow.commit()
            
            self._log_action(
                action="CANCEL_MARRIAGE",
                entity_id=marriage_id,
                entity_type="MarriageRecord",
                user_id=user_id,
                changes={"reason": reason}
            )
            
            return updated
    
    def _validate_marriage_data(self, data: Dict[str, Any]):
        """Valida dados de casamento"""
        required_fields = [
            'spouse1_id', 'spouse2_id', 'marriage_date', 'celebrant_name',
            'witness1_name', 'witness2_name'
        ]
        
        missing = [f for f in required_fields if f not in data or not data[f]]
        if missing:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(missing)}")
        
        # Verificar se já são casados
        if self.get_current_marriage(data['spouse1_id']):
            raise ValueError("Cônjuge 1 já possui casamento ativo")
        if self.get_current_marriage(data['spouse2_id']):
            raise ValueError("Cônjuge 2 já possui casamento ativo")
    
    def _get_citizen(self, citizen_id: str) -> CitizenRef:
        """Obtém cidadão do repositório local"""
        citizen = self.citizen_repo.get_by_id(citizen_id)
        
        if not citizen:
            raise ValueError(f"Cidadão {citizen_id} não encontrado")
        
        return citizen
    
    def _check_marriage_capacity(self, spouse1: CitizenRef, spouse2: CitizenRef, data: Dict[str, Any]):
        """Verifica capacidade legal para casar"""
        # Verificar idade
        if not spouse1.is_emancipated():
            # Verificar consentimento dos pais
            if not (data.get('consent_father_spouse1') or data.get('consent_mother_spouse1')):
                raise ValueError("Cônjuge 1 menor requer consentimento dos pais")
        
        if not spouse2.is_emancipated():
            if not (data.get('consent_father_spouse2') or data.get('consent_mother_spouse2')):
                raise ValueError("Cônjuge 2 menor requer consentimento dos pais")
        
        # Verificar vínculos anteriores
        if spouse1.marital_status not in [MaritalStatus.SINGLE, MaritalStatus.DIVORCED, MaritalStatus.WIDOWED, None]:
            raise ValueError(f"Cônjuge 1 não está apto a casar (status: {spouse1.marital_status})")
        
        if spouse2.marital_status not in [MaritalStatus.SINGLE, MaritalStatus.DIVORCED, MaritalStatus.WIDOWED, None]:
            raise ValueError(f"Cônjuge 2 não está apto a casar (status: {spouse2.marital_status})")
    
    def _create_marriage_record(self, data: Dict[str, Any], spouse1: CitizenRef,
                                spouse2: CitizenRef, user_id: str) -> MarriageRecord:
        """Cria instância de MarriageRecord"""
        marriage_place = Place(
            province=data.get('marriage_province', 'LUANDA'),
            municipality=data.get('marriage_municipality'),
            commune=data.get('marriage_commune'),
            locality=data.get('marriage_locality')
        )
        
        registry_office = RegistryOffice(
            name=data.get('registry_office_name', 'Conservatória do Registo Civil'),
            code=data.get('registry_office_code', '00101'),
            province=data.get('registry_office_province', 'LUANDA'),
            municipality=data.get('registry_office_municipality', 'LUANDA')
        )
        
        return MarriageRecord(
            spouse1_id=spouse1.id,
            spouse1_name=spouse1.full_name.full if spouse1.full_name else data['spouse1_name'],
            spouse1_birth_date=spouse1.birth_date,
            spouse1_age=data.get('spouse1_age'),
            spouse1_nationality=data.get('spouse1_nationality', 'ANGOLANA'),
            spouse1_profession=spouse1.profession,
            spouse1_address=spouse1.address,
            spouse1_marital_status=spouse1.marital_status or MaritalStatus.SINGLE,
            spouse1_father_name=spouse1.father_name,
            spouse1_mother_name=spouse1.mother_name,
            
            spouse2_id=spouse2.id,
            spouse2_name=spouse2.full_name.full if spouse2.full_name else data['spouse2_name'],
            spouse2_birth_date=spouse2.birth_date,
            spouse2_age=data.get('spouse2_age'),
            spouse2_nationality=data.get('spouse2_nationality', 'ANGOLANA'),
            spouse2_profession=spouse2.profession,
            spouse2_address=spouse2.address,
            spouse2_marital_status=spouse2.marital_status or MaritalStatus.SINGLE,
            spouse2_father_name=spouse2.father_name,
            spouse2_mother_name=spouse2.mother_name,
            
            marriage_date=data['marriage_date'],
            marriage_place=marriage_place,
            property_regime=MarriagePropertyRegime(data.get('property_regime', 'COMUNHAO_GERAL')),
            has_prenuptial_agreement=data.get('has_prenuptial_agreement', False),
            prenuptial_agreement_number=data.get('prenuptial_agreement_number'),
            
            celebrant_name=data['celebrant_name'],
            celebrant_id=data.get('celebrant_id'),
            celebrant_title=data.get('celebrant_title', 'CONSERVADOR'),
            
            witness1_name=data['witness1_name'],
            witness1_id=data.get('witness1_id'),
            witness2_name=data['witness2_name'],
            witness2_id=data.get('witness2_id'),
            
            consent_father_spouse1=data.get('consent_father_spouse1', False),
            consent_mother_spouse1=data.get('consent_mother_spouse1', False),
            consent_father_spouse2=data.get('consent_father_spouse2', False),
            consent_mother_spouse2=data.get('consent_mother_spouse2', False),
            
            registry_office=registry_office,
            event_date=data.get('event_date', date.today()),
            created_by=user_id
        )
