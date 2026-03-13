"""
Testes Unitários para o Modelo SQLAlchemy CitizenModel
"""
import pytest
from datetime import date, datetime
from uuid import uuid4
from app.modules.justice.bounded_contexts.infrastructure.models.citizen_model import CitizenModel

@pytest.mark.unit
class TestCitizenModel:
    """Testes para o modelo SQLAlchemy CitizenModel."""

    def test_citizen_model_creation(self, sample_citizen_model):
        """Testa criação básica de CitizenModel."""
        assert sample_citizen_model.citizen_id is not None
        assert sample_citizen_model.full_name == 'Ana Oliveira'
        assert sample_citizen_model.document_number == '00000000000000000000000000000003'
        assert sample_citizen_model.birth_date == date(1995, 3, 10)
        assert sample_citizen_model.gender == 'F'
        assert sample_citizen_model.phone == '+244923456789'
        assert sample_citizen_model.email == 'ana.oliveira@example.com'

    def test_citizen_model_with_defaults(self):
        """Testa criação com valores padrão."""
        model = CitizenModel(citizen_id=uuid4(), full_name='Test User')
        assert model.full_name == 'Test User'
        assert model.document_number is None
        assert model.birth_date is None
        assert model.gender is None
        assert model.phone is None
        assert model.email is None
        assert model.vital_status == 'alive'

    def test_citizen_model_str_representation(self, sample_citizen_model):
        """Testa representação em string."""
        str_repr = str(sample_citizen_model)
        assert 'Citizen' in str_repr
        assert 'Ana Oliveira' in str_repr

    def test_citizen_model_repr(self, sample_citizen_model):
        """Testa representação para debugging."""
        repr_str = repr(sample_citizen_model)
        assert 'CitizenModel' in repr_str
        assert 'Ana Oliveira' in repr_str

    def test_citizen_model_to_dict(self, sample_citizen_model):
        """Testa conversão para dicionário."""
        dict_repr = sample_citizen_model.to_dict()
        assert isinstance(dict_repr, dict)
        assert dict_repr['full_name'] == 'Ana Oliveira'
        assert dict_repr['citizen_id'] == str(sample_citizen_model.citizen_id)
        assert dict_repr['gender'] == 'F'
        assert dict_repr['vital_status'] == 'alive'

    def test_citizen_model_timestamps(self, sample_citizen_model):
        """Testa que timestamps estão presentes."""
        assert isinstance(sample_citizen_model.created_at, datetime)
        assert isinstance(sample_citizen_model.updated_at, datetime)

    def test_citizen_model_vital_status_default(self):
        """Testa default de vital_status."""
        model = CitizenModel(citizen_id=uuid4(), full_name='User')
        assert model.vital_status == 'alive'

    def test_citizen_model_with_custom_vital_status(self):
        """Testa criação com custom vital_status."""
        model = CitizenModel(citizen_id=uuid4(), full_name='User', vital_status='deceased')
        assert model.vital_status == 'deceased'

@pytest.mark.unit
class TestCitizenModelAttributes:
    """Testes para atributos específicos do CitizenModel."""

    def test_citizen_id_is_uuid(self):
        """Testa que citizen_id é UUID."""
        citizen_id = uuid4()
        model = CitizenModel(citizen_id=citizen_id, full_name='Test')
        assert model.citizen_id == citizen_id

    def test_full_name_is_string_required(self):
        """Testa que full_name é obrigatório e string."""
        with pytest.raises(TypeError):
            CitizenModel(citizen_id=uuid4())

    def test_document_number_optional(self):
        """Testa que document_number é opcional."""
        model = CitizenModel(citizen_id=uuid4(), full_name='Test')
        assert model.document_number is None

    def test_birth_date_as_date_type(self):
        """Testa que birth_date é do tipo date."""
        birth = date(2000, 1, 1)
        model = CitizenModel(citizen_id=uuid4(), full_name='Test', birth_date=birth)
        assert isinstance(model.birth_date, date)
        assert model.birth_date == birth

    def test_gender_values(self):
        """Testa valores válidos para gender."""
        genders = [None, 'M', 'F', 'O', 'X']
        for gender in genders:
            model = CitizenModel(citizen_id=uuid4(), full_name='Test', gender=gender)
            assert model.gender == gender

    def test_email_format_storage(self):
        """Testa que email é armazenado como string."""
        email = 'test@example.com'
        model = CitizenModel(citizen_id=uuid4(), full_name='Test', email=email)
        assert model.email == email
        assert isinstance(model.email, str)

    def test_fuc_sync_timestamp_optional(self):
        """Testa que fuc_sync_timestamp é opcional."""
        model = CitizenModel(citizen_id=uuid4(), full_name='Test')
        assert model.fuc_sync_timestamp is None

    def test_fuc_sync_timestamp_datetime(self):
        """Testa que fuc_sync_timestamp é datetime."""
        now = datetime.utcnow()
        model = CitizenModel(citizen_id=uuid4(), full_name='Test', fuc_sync_timestamp=now)
        assert isinstance(model.fuc_sync_timestamp, datetime)

@pytest.mark.unit
class TestCitizenModelDataTypes:
    """Testes para validação de tipos de dados."""

    def test_phone_number_is_string(self):
        """Testa que phone é armazenado como string."""
        phone = '+244912345678'
        model = CitizenModel(citizen_id=uuid4(), full_name='Test', phone=phone)
        assert model.phone == phone
        assert isinstance(model.phone, str)

    def test_model_mutability(self, sample_citizen_model):
        """Testa que modelo pode ser modificado."""
        original_name = sample_citizen_model.full_name
        sample_citizen_model.full_name = 'Modified Name'
        assert sample_citizen_model.full_name == 'Modified Name'
        assert sample_citizen_model.full_name != original_name

    def test_to_dict_with_null_values(self):
        """Testa to_dict com valores null."""
        model = CitizenModel(citizen_id=uuid4(), full_name='Test')
        dict_repr = model.to_dict()
        assert dict_repr['document_number'] is None
        assert dict_repr['birth_date'] is None
        assert dict_repr['gender'] is None
        assert dict_repr['phone'] is None
        assert dict_repr['email'] is None
        assert dict_repr['fuc_sync_timestamp'] is None

    def test_to_dict_iso_date_conversion(self):
        """Testa que to_dict converte dates para ISO."""
        birth = date(2000, 1, 15)
        model = CitizenModel(citizen_id=uuid4(), full_name='Test', birth_date=birth)
        dict_repr = model.to_dict()
        assert dict_repr['birth_date'] == '2000-01-15'
        assert isinstance(dict_repr['birth_date'], str)

@pytest.mark.unit
class TestCitizenModelStringRepresentations:
    """Testes para representações em string."""

    def test_str_includes_full_name(self, sample_citizen_model):
        """Testa que str() inclui full_name."""
        str_repr = str(sample_citizen_model)
        assert sample_citizen_model.full_name in str_repr

    def test_str_includes_citizen_id(self, sample_citizen_model):
        """Testa que str() inclui citizen_id."""
        str_repr = str(sample_citizen_model)
        assert str(sample_citizen_model.citizen_id) in str_repr

    def test_repr_includes_class_name(self, sample_citizen_model):
        """Testa que repr() inclui nome da classe."""
        repr_str = repr(sample_citizen_model)
        assert 'CitizenModel' in repr_str

    def test_repr_includes_full_name(self, sample_citizen_model):
        """Testa que repr() inclui full_name."""
        repr_str = repr(sample_citizen_model)
        assert sample_citizen_model.full_name in repr_str