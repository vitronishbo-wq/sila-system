from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from ...domain.models.certificate_record import CertificateRecord
from ...domain.models.birth_record import BirthRecord
from ...domain.models.death_record import DeathRecord
from ...domain.models.marriage_record import MarriageRecord
from ...domain.enums import CertificateType, CertificateStatus
from ...domain.value_objects import CertificateNumber
from .base_service import BaseService


class CertificateService(BaseService[CertificateRecord]):
    """Serviço para emissão e gestão de certificados"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def issue_certificate(self, event_id: str, event_type: str, citizen_id: str,
                         citizen_name: str, certificate_type: CertificateType,
                         user_id: str, is_duplicate: bool = False,
                         original_certificate_id: Optional[str] = None) -> CertificateRecord:
        """Emite um novo certificado para um evento"""
        with self.uow_factory.create() as uow:
            # 1. Buscar evento
            event = self.event_repo.get_by_id(event_id)
            if not event:
                raise ValueError(f"Evento {event_id} não encontrado")
            
            # 2. Verificar se já existe certificado (para não duplicar)
            if not is_duplicate:
                existing = self.certificate_repo.get_by_event_id(event_id)
                if existing:
                    return existing[0]
            
            # 3. Gerar conteúdo do certificado
            content = self._generate_certificate_content(event, certificate_type)
            
            # 4. Obter conservatória do evento
            registry_office = event.registry_office if hasattr(event, 'registry_office') else None
            
            # 5. Criar certificado
            certificate = CertificateRecord(
                certificate_type=certificate_type.value if hasattr(certificate_type, 'value') else certificate_type,
                event_id=event_id,
                event_type=event_type,
                citizen_id=citizen_id,
                citizen_name=citizen_name,
                full_content=content['full'],
                summary=content['summary'],
                issue_office=registry_office,
                status=CertificateStatus.DRAFT.value if hasattr(CertificateStatus.DRAFT, 'value') else CertificateStatus.DRAFT,
                is_duplicate=is_duplicate,
                original_certificate_id=original_certificate_id,
                created_by=user_id
            )
            
            # 6. Gerar número de certificado
            year = datetime.now().year
            cert_type_value = certificate_type.value if hasattr(certificate_type, 'value') else certificate_type
            sequence = self.certificate_repo.get_next_sequence_number(year, cert_type_value)
            certificate.generate_certificate_number(sequence, year)
            
            # 7. Emitir (muda status para ISSUED)
            certificate.issue(user_id)
            
            # 8. Persistir
            saved = self.certificate_repo.save(certificate)
            
            # 9. Registrar auditoria
            self._log_action(
                action="ISSUE_CERTIFICATE",
                entity_id=saved.id,
                entity_type="Certificate",
                user_id=user_id,
                changes={
                    "certificate_number": str(saved.certificate_number),
                    "certificate_type": cert_type_value
                }
            )
            
            uow.commit()
            return saved
    
    def authenticate_certificate(self, certificate_id: str, user_id: str) -> CertificateRecord:
        """Autentica um certificado (torna-o oficial)"""
        certificate = self.certificate_repo.get_by_id(certificate_id)
        if not certificate:
            raise ValueError(f"Certificado {certificate_id} não encontrado")
        
        cert_status = certificate.status
        if isinstance(cert_status, str):
            cert_status = CertificateStatus(cert_status)
        
        if cert_status != CertificateStatus.ISSUED:
            raise ValueError(f"Não é possível autenticar certificado com status {cert_status}")
        
        with self.uow_factory.create() as uow:
            certificate.authenticate()
            certificate.updated_by = user_id
            
            saved = self.certificate_repo.save(certificate)
            
            self._log_action(
                action="AUTHENTICATE_CERTIFICATE",
                entity_id=certificate_id,
                entity_type="Certificate",
                user_id=user_id,
                changes={"authentication_code": certificate.authentication_code}
            )
            
            uow.commit()
            return saved
    
    def create_duplicate(self, certificate_id: str, reason: str, user_id: str) -> CertificateRecord:
        """Cria segunda via de um certificado"""
        original = self.certificate_repo.get_by_id(certificate_id)
        if not original:
            raise ValueError(f"Certificado original {certificate_id} não encontrado")
        
        # Criar duplicata
        duplicate = original.create_duplicate(reason)
        duplicate.created_by = user_id
        
        # Emitir a duplicata
        return self.issue_certificate(
            event_id=original.event_id,
            event_type=original.event_type,
            citizen_id=original.citizen_id,
            citizen_name=original.citizen_name,
            certificate_type=original.certificate_type,
            user_id=user_id,
            is_duplicate=True,
            original_certificate_id=original.id
        )
    
    def verify_certificate(self, certificate_number: str, authentication_code: Optional[str] = None) -> Dict[str, Any]:
        """Verifica autenticidade de um certificado"""
        cert_number = CertificateNumber(certificate_number)
        certificate = self.certificate_repo.get_by_number(cert_number)
        
        if not certificate:
            return {
                "valid": False,
                "message": "Certificado não encontrado"
            }
        
        cert_status = certificate.status
        if isinstance(cert_status, str):
            cert_status = CertificateStatus(cert_status)
        
        if cert_status == CertificateStatus.CANCELLED:
            return {
                "valid": False,
                "message": "Certificado cancelado",
                "cancelled_at": certificate.metadata.get('cancelled_at') if certificate.metadata else None
            }
        
        if authentication_code and certificate.authentication_code != authentication_code:
            return {
                "valid": False,
                "message": "Código de autenticação inválido"
            }
        
        return {
            "valid": True,
            "authenticated": certificate.is_authenticated,
            "certificate_number": str(certificate.certificate_number),
            "certificate_type": certificate.certificate_type,
            "citizen_name": certificate.citizen_name,
            "issue_date": certificate.issue_date.isoformat() if certificate.issue_date else None,
            "event_id": certificate.event_id,
            "is_duplicate": certificate.is_duplicate,
            "authentication_code": certificate.authentication_code if certificate.is_authenticated else None
        }
    
    def get_certificate_by_number(self, certificate_number: str) -> Optional[CertificateRecord]:
        """Busca certificado por número"""
        cert_number = CertificateNumber(certificate_number)
        return self.certificate_repo.get_by_number(cert_number)
    
    def get_certificates_by_citizen(self, citizen_id: str) -> List[CertificateRecord]:
        """Lista certificados de um cidadão"""
        return self.certificate_repo.get_by_citizen_id(citizen_id)
    
    def get_certificates_by_event(self, event_id: str) -> List[CertificateRecord]:
        """Lista certificados de um evento"""
        return self.certificate_repo.get_by_event_id(event_id)
    
    def cancel_certificate(self, certificate_id: str, reason: str, user_id: str) -> CertificateRecord:
        """Cancela um certificado"""
        certificate = self.certificate_repo.get_by_id(certificate_id)
        if not certificate:
            raise ValueError(f"Certificado {certificate_id} não encontrado")
        
        cert_status = certificate.status
        if isinstance(cert_status, str):
            cert_status = CertificateStatus(cert_status)
        
        if cert_status == CertificateStatus.CANCELLED:
            raise ValueError("Certificado já está cancelado")
        
        with self.uow_factory.create() as uow:
            certificate.cancel(reason, user_id)
            
            saved = self.certificate_repo.save(certificate)
            
            self._log_action(
                action="CANCEL_CERTIFICATE",
                entity_id=certificate_id,
                entity_type="Certificate",
                user_id=user_id,
                changes={"reason": reason}
            )
            
            uow.commit()
            return saved
    
    def _generate_certificate_content(self, event: Any, cert_type: CertificateType) -> Dict[str, str]:
        """Gera conteúdo do certificado baseado no evento"""
        if isinstance(event, BirthRecord):
            return self._generate_birth_certificate_content(event, cert_type)
        elif isinstance(event, DeathRecord):
            return self._generate_death_certificate_content(event, cert_type)
        elif isinstance(event, MarriageRecord):
            return self._generate_marriage_certificate_content(event, cert_type)
        else:
            cert_type_str = cert_type.value if hasattr(cert_type, 'value') else cert_type
            return {
                "full": f"Certificado de {cert_type_str} para evento {event.id}",
                "summary": f"Certificado resumido"
            }
    
    def _generate_birth_certificate_content(self, birth: BirthRecord, cert_type: CertificateType) -> Dict[str, str]:
        """Gera conteúdo para certidão de nascimento"""
        cert_type_str = cert_type.value if hasattr(cert_type, 'value') else cert_type
        is_full = "FULL" in cert_type_str
        
        full_content = f"""
        REPÚBLICA DE ANGOLA
        MINISTÉRIO DA JUSTIÇA E DOS DIREITOS HUMANOS
        CONSERVATÓRIA DO REGISTO CIVIL
        
        CERTIDÃO DE NASCIMENTO {'INTEIRA' if is_full else ''}
        Nº {birth.event_number}
        
        {birth.child_first_names} {birth.child_last_names}
        
        Nasceu em {birth.child_birth_date.strftime('%d/%m/%Y')}
        {'às ' + birth.child_birth_time if birth.child_birth_time else ''}
        em {birth.child_birth_place.municipality if birth.child_birth_place else ''}
        
        Filho de {birth.mother_name} e {birth.father_name or 'Desconhecido'}
        
        Registado por {birth.declarant_name} ({birth.declarant_relationship})
        
        Data do registo: {birth.event_date.strftime('%d/%m/%Y')}
        Conservatória: {birth.registry_office.name if birth.registry_office else ''}
        """
        
        summary = f"Certidão de nascimento de {birth.child_first_names} {birth.child_last_names}, nascido em {birth.child_birth_date.strftime('%d/%m/%Y')}"
        
        return {"full": full_content, "summary": summary}
    
    def _generate_death_certificate_content(self, death: DeathRecord, cert_type: CertificateType) -> Dict[str, str]:
        """Gera conteúdo para certidão de óbito"""
        cert_type_str = cert_type.value if hasattr(cert_type, 'value') else cert_type
        is_full = "FULL" in cert_type_str
        
        full_content = f"""
        REPÚBLICA DE ANGOLA
        MINISTÉRIO DA JUSTIÇA E DOS DIREITOS HUMANOS
        CONSERVATÓRIA DO REGISTO CIVIL
        
        CERTIDÃO DE ÓBITO {'INTEIRA' if is_full else ''}
        Nº {death.event_number}
        
        {death.deceased_name}
        
        Faleceu em {death.death_date.strftime('%d/%m/%Y')}
        {'às ' + death.death_time if death.death_time else ''}
        em {death.death_place.municipality if death.death_place else ''}
        
        Causa da morte: {death.death_cause or 'N/I'}
        
        Cônjuge: {death.spouse_name or 'N/I'}
        
        Declarante: {death.declarant_name} ({death.declarant_relationship})
        
        Data do registo: {death.event_date.strftime('%d/%m/%Y')}
        Conservatória: {death.registry_office.name if death.registry_office else ''}
        """
        
        summary = f"Certidão de óbito de {death.deceased_name}, falecido em {death.death_date.strftime('%d/%m/%Y')}"
        
        return {"full": full_content, "summary": summary}
    
    def _generate_marriage_certificate_content(self, marriage: MarriageRecord, cert_type: CertificateType) -> Dict[str, str]:
        """Gera conteúdo para certidão de casamento"""
        cert_type_str = cert_type.value if hasattr(cert_type, 'value') else cert_type
        is_full = "FULL" in cert_type_str
        
        property_regime = marriage.property_regime
        regime_value = property_regime.value if hasattr(property_regime, 'value') else property_regime
        regime_text = {
            "COMUNHAO_GERAL": "Comunhão geral de bens",
            "SEPARACAO_BENS": "Separação de bens",
            "COMUNHAO_ADQUIRIDOS": "Comunhão de adquiridos"
        }.get(regime_value, "N/I")
        
        full_content = f"""
        REPÚBLICA DE ANGOLA
        MINISTÉRIO DA JUSTIÇA E DOS DIREITOS HUMANOS
        CONSERVATÓRIA DO REGISTO CIVIL
        
        CERTIDÃO DE CASAMENTO {'INTEIRA' if is_full else ''}
        Nº {marriage.event_number}
        
        Contraíram casamento:
        
        {marriage.spouse1_name}
        Filho de {marriage.spouse1_father_name or ''} e {marriage.spouse1_mother_name or ''}
        
        e
        
        {marriage.spouse2_name}
        Filho de {marriage.spouse2_father_name or ''} e {marriage.spouse2_mother_name or ''}
        
        Data do casamento: {marriage.marriage_date.strftime('%d/%m/%Y')}
        Local: {marriage.marriage_place.municipality if marriage.marriage_place else ''}
        
        Regime de bens: {regime_text}
        {'Com convenção antenupcial' if marriage.has_prenuptial_agreement else ''}
        
        Celebrante: {marriage.celebrant_name} ({marriage.celebrant_title})
        Testemunhas: {marriage.witness1_name} e {marriage.witness2_name}
        
        Data do registo: {marriage.event_date.strftime('%d/%m/%Y')}
        Conservatória: {marriage.registry_office.name if marriage.registry_office else ''}
        """
        
        summary = f"Certidão de casamento de {marriage.spouse1_name} e {marriage.spouse2_name}, celebrado em {marriage.marriage_date.strftime('%d/%m/%Y')}"
        
        return {"full": full_content, "summary": summary}
