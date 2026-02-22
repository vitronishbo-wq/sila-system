"""Sample data for justice module testing and demonstration."""

from datetime import datetime, timedelta
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from modules.justice.models import (
    Case,
    CaseEvent,
    CasePriority,
    CaseStatus,
    CaseType,
    Court,
    CourtJurisdiction,
    CourtType,
    DocumentCategory,
    DocumentStatus,
    DocumentType,
    EventStatus,
    EventType,
    LegalDocument,
)


class JusticeSampleData:
    """Sample data generator for justice module."""

    @staticmethod
    def create_sample_courts(db: Session, user_id: int) -> List[Court]:
        """Create sample courts for Angola."""
        courts_data = [
            {
                "name": "Tribunal Supremo de Angola",
                "code": "TSA-001",
                "court_type": CourtType.SUPREME,
                "jurisdiction": CourtJurisdiction.NATIONAL,
                "province": "Luanda",
                "municipality": "Luanda",
                "address": "Largo do Tribunal Supremo, Luanda",
                "phone": "+244 222 334 455",
                "email": "tribunal.supremo@tribunais.ao",
                "chief_judge": "Dr. João Manuel dos Santos",
                "total_judges": 15,
                "courtrooms": 8,
                "max_cases_per_month": 50,
            },
            {
                "name": "Tribunal Provincial de Luanda",
                "code": "TPL-001",
                "court_type": CourtType.PROVINCIAL,
                "jurisdiction": CourtJurisdiction.PROVINCIAL,
                "province": "Luanda",
                "municipality": "Luanda",
                "address": "Rua Major Kanhangulo, Luanda",
                "phone": "+244 222 445 566",
                "email": "tribunal.luanda@tribunais.ao",
                "chief_judge": "Dra. Maria Fernanda Silva",
                "total_judges": 8,
                "courtrooms": 5,
                "max_cases_per_month": 200,
            },
            {
                "name": "Tribunal Municipal de Viana",
                "code": "TMV-001",
                "court_type": CourtType.MUNICIPAL,
                "jurisdiction": CourtJurisdiction.MUNICIPAL,
                "province": "Luanda",
                "municipality": "Viana",
                "address": "Avenida Principal, Viana",
                "phone": "+244 222 556 677",
                "email": "tribunal.viana@tribunais.ao",
                "chief_judge": "Dr. António Carlos Mendes",
                "total_judges": 4,
                "courtrooms": 3,
                "max_cases_per_month": 150,
            },
            {
                "name": "Tribunal Provincial do Bengo",
                "code": "TPB-001",
                "court_type": CourtType.PROVINCIAL,
                "jurisdiction": CourtJurisdiction.PROVINCIAL,
                "province": "Bengo",
                "municipality": "Caxito",
                "address": "Praça da Independência, Caxito",
                "phone": "+244 234 123 456",
                "email": "tribunal.bengo@tribunais.ao",
                "chief_judge": "Dra. Isabel Rodrigues",
                "total_judges": 6,
                "courtrooms": 4,
                "max_cases_per_month": 120,
            },
        ]

        courts = []
        for court_data in courts_data:
            court = Court(
                **court_data,
                created_by=user_id,
                operating_hours="08:00-17:00",
                languages="Português, Kimbundu, Kikongo",
                current_case_load=0,
            )
            db.add(court)
            courts.append(court)

        db.commit()
        return courts

    @staticmethod
    def create_sample_cases(
        db: Session, courts: List[Court], user_id: int
    ) -> List[Case]:
        """Create sample legal cases."""
        cases_data = [
            {
                "title": "Conflito de Propriedade Urbana",
                "description": "Disputa sobre propriedade de terreno urbano em Luanda entre dois cidadãos.",
                "case_type": CaseType.CIVIL,
                "priority": CasePriority.MEDIUM,
                "plaintiff_citizen_id": 1001,
                "defendant_citizen_id": 1002,
                "court_id": courts[1].id,  # Tribunal Provincial de Luanda
                "judge_name": "Dr. Carlos Alberto Neto",
                "is_public": True,
            },
            {
                "title": "Processo Criminal - Furto Qualificado",
                "description": "Processo criminal por furto qualificado em estabelecimento comercial.",
                "case_type": CaseType.CRIMINAL,
                "priority": CasePriority.HIGH,
                "plaintiff_name": "Ministério Público",
                "defendant_citizen_id": 1003,
                "court_id": courts[1].id,
                "judge_name": "Dra. Ana Paula Santos",
                "prosecutor_name": "Dr. Miguel Fernandes",
                "is_confidential": True,
            },
            {
                "title": "Divórcio Litigioso",
                "description": "Processo de divórcio com partilha de bens e guarda de menores.",
                "case_type": CaseType.FAMILY,
                "priority": CasePriority.MEDIUM,
                "plaintiff_citizen_id": 1004,
                "defendant_citizen_id": 1005,
                "court_id": courts[2].id,  # Tribunal Municipal de Viana
                "judge_name": "Dra. Teresa Almeida",
                "is_public": False,
            },
            {
                "title": "Conflito Laboral - Despedimento Ilegal",
                "description": "Ação por despedimento sem justa causa e pagamento de indemnizações.",
                "case_type": CaseType.LABOR,
                "priority": CasePriority.MEDIUM,
                "plaintiff_citizen_id": 1006,
                "defendant_name": "Empresa ABC, Lda",
                "court_id": courts[1].id,
                "judge_name": "Dr. Paulo Mendes",
                "is_public": True,
            },
            {
                "title": "Impugnação de Ato Administrativo",
                "description": "Impugnação de decisão administrativa sobre licenciamento comercial.",
                "case_type": CaseType.ADMINISTRATIVE,
                "priority": CasePriority.LOW,
                "plaintiff_name": "Comercial XYZ, Lda",
                "defendant_name": "Administração Municipal de Luanda",
                "court_id": courts[1].id,
                "judge_name": "Dra. Cristina Sousa",
                "is_public": True,
            },
        ]

        cases = []
        for i, case_data in enumerate(cases_data):
            # Generate case number
            year = datetime.now().year
            case_number = f"{case_data['case_type'].value[:3].upper()}-LUA-{year}-{str(i+1).zfill(4)}"

            case = Case(
                case_number=case_number,
                **case_data,
                filing_date=datetime.now() - timedelta(days=30 + i * 10),
                created_by=user_id,
                status=CaseStatus.IN_PROGRESS if i < 3 else CaseStatus.REGISTERED,
            )
            db.add(case)
            cases.append(case)

        db.commit()
        return cases

    @staticmethod
    def create_sample_events(
        db: Session, cases: List[Case], user_id: int
    ) -> List[CaseEvent]:
        """Create sample case events."""
        events_data = [
            {
                "case_id": cases[0].id,
                "event_type": EventType.HEARING,
                "title": "Audiência de Instrução e Julgamento",
                "description": "Primeira audiência para ouvir as partes e testemunhas.",
                "scheduled_date": datetime.now() + timedelta(days=15),
                "duration_minutes": 120,
                "location": "Sala 3 - Tribunal Provincial de Luanda",
                "judge_name": "Dr. Carlos Alberto Neto",
                "is_public": True,
            },
            {
                "case_id": cases[1].id,
                "event_type": EventType.DEPOSITION,
                "title": "Depoimento do Arguido",
                "description": "Depoimento do arguido no processo criminal.",
                "scheduled_date": datetime.now() + timedelta(days=7),
                "duration_minutes": 90,
                "location": "Sala 1 - Tribunal Provincial de Luanda",
                "judge_name": "Dra. Ana Paula Santos",
                "prosecutor_name": "Dr. Miguel Fernandes",
                "is_public": False,
            },
            {
                "case_id": cases[0].id,
                "event_type": EventType.EVIDENCE_SUBMISSION,
                "title": "Apresentação de Documentos",
                "description": "Apresentação de documentos de propriedade e plantas cadastrais.",
                "scheduled_date": datetime.now() - timedelta(days=5),
                "actual_date": datetime.now() - timedelta(days=5),
                "status": EventStatus.COMPLETED,
                "duration_minutes": 60,
                "location": "Secretaria do Tribunal",
                "outcome": "Documentos aceitos e juntados aos autos",
            },
            {
                "case_id": cases[2].id,
                "event_type": EventType.MEDIATION,
                "title": "Sessão de Mediação Familiar",
                "description": "Tentativa de acordo sobre guarda dos filhos.",
                "scheduled_date": datetime.now() + timedelta(days=10),
                "duration_minutes": 180,
                "location": "Sala de Mediação - Tribunal Municipal de Viana",
                "judge_name": "Dra. Teresa Almeida",
                "is_public": False,
            },
        ]

        events = []
        for event_data in events_data:
            event = CaseEvent(**event_data, created_by=user_id)
            db.add(event)
            events.append(event)

        db.commit()
        return events

    @staticmethod
    def create_sample_documents(
        db: Session, cases: List[Case], user_id: int
    ) -> List[LegalDocument]:
        """Create sample legal documents."""
        documents_data = [
            {
                "case_id": cases[0].id,
                "title": "Petição Inicial - Conflito de Propriedade",
                "description": "Petição inicial do processo de conflito de propriedade urbana.",
                "document_type": DocumentType.PETITION,
                "category": DocumentCategory.PROCEDURAL,
                "issuing_authority": "Advogado do Requerente",
                "recipient": "Tribunal Provincial de Luanda",
                "legal_basis": "Código Civil Angolano, Art. 1305º e seguintes",
                "is_public": True,
            },
            {
                "case_id": cases[1].id,
                "title": "Auto de Notícia Criminal",
                "description": "Auto de notícia do crime de furto qualificado.",
                "document_type": DocumentType.EVIDENCE,
                "category": DocumentCategory.EVIDENCE,
                "issuing_authority": "Polícia Nacional de Angola",
                "recipient": "Ministério Público",
                "is_confidential": True,
                "status": DocumentStatus.ISSUED,
            },
            {
                "case_id": None,  # Standalone document
                "title": "Certidão de Antecedentes Criminais",
                "description": "Certidão negativa de antecedentes criminais.",
                "document_type": DocumentType.CERTIFICATE,
                "category": DocumentCategory.CERTIFICATE,
                "issuing_authority": "Sistema de Justiça SILA",
                "recipient": "Cidadão ID 1007",
                "validity_period_days": 90,
                "status": DocumentStatus.ISSUED,
                "requires_signature": True,
                "is_signed": True,
                "is_public": False,
            },
            {
                "case_id": cases[2].id,
                "title": "Acordo de Regulação do Poder Paternal",
                "description": "Acordo sobre guarda e alimentos dos filhos menores.",
                "document_type": DocumentType.CONTRACT,
                "category": DocumentCategory.JUDICIAL,
                "issuing_authority": "Tribunal Municipal de Viana",
                "legal_basis": "Código da Família, Art. 181º e seguintes",
                "requires_signature": True,
                "status": DocumentStatus.PENDING_REVIEW,
            },
            {
                "case_id": cases[3].id,
                "title": "Sentença Condenatória",
                "description": "Sentença condenando a empresa ao pagamento de indemnização.",
                "document_type": DocumentType.SENTENCE,
                "category": DocumentCategory.JUDICIAL,
                "issuing_authority": "Tribunal Provincial de Luanda",
                "judge_name": "Dr. Paulo Mendes",
                "legal_basis": "Lei Geral do Trabalho, Art. 78º",
                "status": DocumentStatus.ISSUED,
                "is_public": True,
            },
        ]

        documents = []
        for i, doc_data in enumerate(documents_data):
            # Generate document number
            year = datetime.now().year
            doc_number = f"{doc_data['document_type'].value[:3].upper()}-{year}-{str(i+1).zfill(4)}"

            document = LegalDocument(
                document_number=doc_number,
                **doc_data,
                issue_date=datetime.now() - timedelta(days=i * 5),
                created_by=user_id,
            )

            # Set expiry date for certificates
            if doc_data.get("validity_period_days"):
                document.expiry_date = document.issue_date + timedelta(
                    days=doc_data["validity_period_days"]
                )

            db.add(document)
            documents.append(document)

        db.commit()
        return documents

    @staticmethod
    def create_complete_sample_data(db: Session, user_id: int) -> Dict[str, Any]:
        """Create complete sample data set for justice module."""
        print("Creating sample courts...")
        courts = JusticeSampleData.create_sample_courts(db, user_id)

        print("Creating sample cases...")
        cases = JusticeSampleData.create_sample_cases(db, courts, user_id)

        print("Creating sample events...")
        events = JusticeSampleData.create_sample_events(db, cases, user_id)

        print("Creating sample documents...")
        documents = JusticeSampleData.create_sample_documents(db, cases, user_id)

        # Update court case loads
        for court in courts:
            court_cases = [c for c in cases if c.court_id == court.id and c.is_active]
            court.current_case_load = len(court_cases)

        db.commit()

        return {
            "courts": len(courts),
            "cases": len(cases),
            "events": len(events),
            "documents": len(documents),
            "summary": {
                "total_records": len(courts)
                + len(cases)
                + len(events)
                + len(documents),
                "active_cases": len([c for c in cases if c.is_active]),
                "public_cases": len([c for c in cases if c.is_public]),
                "confidential_cases": len([c for c in cases if c.is_confidential]),
                "upcoming_events": len([e for e in events if e.is_upcoming]),
                "issued_documents": len(
                    [d for d in documents if d.status == DocumentStatus.ISSUED]
                ),
            },
        }
