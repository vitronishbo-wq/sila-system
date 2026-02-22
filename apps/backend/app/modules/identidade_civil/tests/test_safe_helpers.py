"""
Testes Unitários para Utilitários safe.py
"""

import pytest
from datetime import date, datetime

from app.modules.identidade_civil.utils.safe import (
    safe_get,
    safe_getitem,
    safe_isoformat,
    safe_int,
    safe_float,
    safe_str,
    safe_bool,
    safe_apply,
    safe_or_raise,
)


@pytest.mark.unit
class TestSafeGet:
    """Testes para safe_get()."""
    
    def test_safe_get_existing_attribute(self, sample_citizen):
        """Testa acesso a atributo existente."""
        assert safe_get(sample_citizen, "full_name") == "João Silva"
        assert safe_get(sample_citizen, "gender") == "M"
    
    def test_safe_get_missing_attribute_returns_none(self, sample_citizen):
        """Testa que atributo faltando retorna None."""
        assert safe_get(sample_citizen, "missing_attr") is None
    
    def test_safe_get_missing_attribute_with_default(self, sample_citizen):
        """Testa default customizado para atributo faltando."""
        assert safe_get(sample_citizen, "missing_attr", "default") == "default"
        assert safe_get(sample_citizen, "missing_attr", 42) == 42
    
    def test_safe_get_none_value(self):
        """Testa acesso a atributo com valor None."""
        class Obj:
            attr = None
        
        obj = Obj()
        assert safe_get(obj, "attr") is None
        assert safe_get(obj, "attr", "default") is None
    
    def test_safe_get_exception_handling(self):
        """Testa tratamento de exceções."""
        # Teste com um objeto que não suporta getattr normalmente
        assert safe_get(None, "anything", "default") == "default"


@pytest.mark.unit
class TestSafeGetItem:
    """Testes para safe_getitem()."""
    
    def test_safe_getitem_existing_key(self):
        """Testa acesso a chave existente."""
        data = {"name": "João", "age": 30}
        assert safe_getitem(data, "name") == "João"
        assert safe_getitem(data, "age") == 30
    
    def test_safe_getitem_missing_key_returns_none(self):
        """Testa que chave faltando retorna None."""
        data = {"name": "João"}
        assert safe_getitem(data, "missing") is None
    
    def test_safe_getitem_missing_key_with_default(self):
        """Testa default customizado para chave faltando."""
        data = {"name": "João"}
        assert safe_getitem(data, "missing", "default") == "default"
        assert safe_getitem(data, "missing", 99) == 99
    
    def test_safe_getitem_non_dict(self):
        """Testa com objeto que não é dicionário."""
        assert safe_getitem("not a dict", "key", "default") == "default"
        assert safe_getitem(123, "key", "default") == "default"
        assert safe_getitem(None, "key", "default") == "default"


@pytest.mark.unit
class TestSafeIsoformat:
    """Testes para safe_isoformat()."""
    
    def test_safe_isoformat_date(self):
        """Testa conversão de date."""
        d = date(2026, 2, 16)
        result = safe_isoformat(d)
        assert result == "2026-02-16"
    
    def test_safe_isoformat_datetime(self):
        """Testa conversão de datetime."""
        dt = datetime(2026, 2, 16, 14, 30, 45)
        result = safe_isoformat(dt)
        assert "2026-02-16" in result
        assert "14:30:45" in result
    
    def test_safe_isoformat_none(self):
        """Testa com None."""
        assert safe_isoformat(None) is None
    
    def test_safe_isoformat_invalid(self):
        """Testa com objeto inválido."""
        assert safe_isoformat("not a date") is None
        assert safe_isoformat(123) is None


@pytest.mark.unit
class TestSafeInt:
    """Testes para safe_int()."""
    
    def test_safe_int_from_string(self):
        """Testa conversão de string."""
        assert safe_int("42") == 42
        assert safe_int("-10") == -10
        assert safe_int("0") == 0
    
    def test_safe_int_from_float(self):
        """Testa conversão de float."""
        assert safe_int(42.9) == 42
        assert safe_int(10.1) == 10
    
    def test_safe_int_from_int(self):
        """Testa que int já é int."""
        assert safe_int(42) == 42
    
    def test_safe_int_invalid_returns_default(self):
        """Testa que conversão inválida retorna default."""
        assert safe_int("not a number") == 0
        assert safe_int("not a number", -1) == -1
        assert safe_int(None, 100) == 100


@pytest.mark.unit
class TestSafeFloat:
    """Testes para safe_float()."""
    
    def test_safe_float_from_string(self):
        """Testa conversão de string."""
        assert safe_float("42.5") == 42.5
        assert safe_float("-10.1") == -10.1
    
    def test_safe_float_from_int(self):
        """Testa conversão de int."""
        assert safe_float(42) == 42.0
    
    def test_safe_float_from_float(self):
        """Testa que float já é float."""
        assert safe_float(42.5) == 42.5
    
    def test_safe_float_invalid_returns_default(self):
        """Testa que conversão inválida retorna default."""
        assert safe_float("not a number") == 0.0
        assert safe_float("not a number", -1.5) == -1.5


@pytest.mark.unit
class TestSafeStr:
    """Testes para safe_str()."""
    
    def test_safe_str_from_various_types(self):
        """Testa conversão de vários tipos."""
        assert safe_str(42) == "42"
        assert safe_str(42.5) == "42.5"
        assert safe_str(True) == "True"
        assert safe_str("already string") == "already string"
    
    def test_safe_str_from_none(self):
        """Testa conversão de None."""
        assert safe_str(None) == ""
        assert safe_str(None, "default") == "default"
    
    def test_safe_str_from_object(self):
        """Testa conversão de objeto."""
        obj = object()
        result = safe_str(obj)
        assert "object" in result


@pytest.mark.unit
class TestSafeBool:
    """Testes para safe_bool()."""
    
    def test_safe_bool_from_bool(self):
        """Testa que bool já é bool."""
        assert safe_bool(True) is True
        assert safe_bool(False) is False
    
    def test_safe_bool_from_string(self):
        """Testa conversão de string."""
        assert safe_bool("true") is True
        assert safe_bool("True") is True
        assert safe_bool("1") is True
        assert safe_bool("yes") is True
        assert safe_bool("sim") is True
        assert safe_bool("on") is True
        
        assert safe_bool("false") is False
        assert safe_bool("0") is False
        assert safe_bool("no") is False
    
    def test_safe_bool_from_number(self):
        """Testa conversão de numbers."""
        assert safe_bool(1) is True
        assert safe_bool(-1) is True
        assert safe_bool(0) is False
        assert safe_bool(0.0) is False
    
    def test_safe_bool_from_none(self):
        """Testa conversão de None."""
        assert safe_bool(None) is False
        assert safe_bool(None, True) is True


@pytest.mark.unit
class TestSafeApply:
    """Testes para safe_apply()."""
    
    def test_safe_apply_success(self, sample_citizen):
        """Testa aplicação bem-sucedida de função."""
        result = safe_apply(sample_citizen, "birth_date", lambda x: x.year)
        assert result == 2000
    
    def test_safe_apply_missing_attribute(self, sample_citizen):
        """Testa com atributo faltando."""
        result = safe_apply(sample_citizen, "missing", int, 0)
        assert result == 0
    
    def test_safe_apply_transform_error(self, sample_citizen):
        """Testa quando transformação falha."""
        # Tentar converter data para int vai falhar
        result = safe_apply(sample_citizen, "birth_date", int, -1)
        assert result == -1
    
    def test_safe_apply_with_lambda(self, sample_citizen):
        """Testa com função lambda."""
        result = safe_apply(
            sample_citizen, 
            "full_name", 
            lambda x: x.upper(),
            ""
        )
        assert result == "JOÃO SILVA"


@pytest.mark.unit
class TestSafeOrRaise:
    """Testes para safe_or_raise()."""
    
    def test_safe_or_raise_existing_attribute(self, sample_citizen):
        """Testa acesso a atributo existente."""
        result = safe_or_raise(sample_citizen, "full_name")
        assert result == "João Silva"
    
    def test_safe_or_raise_missing_attribute(self, sample_citizen):
        """Testa que atributo faltando lança exceção."""
        with pytest.raises(AttributeError):
            safe_or_raise(sample_citizen, "missing_attr")
    
    def test_safe_or_raise_custom_message(self, sample_citizen):
        """Testa mensagem de erro customizada."""
        with pytest.raises(AttributeError) as exc_info:
            safe_or_raise(sample_citizen, "missing", "Custom error message")
        
        assert "Custom error message" in str(exc_info.value)


@pytest.mark.unit
class TestSafeIntegration:
    """Testes de integração entre funções safe."""
    
    def test_combining_safe_functions(self, fuc_projection_data):
        """Testa combinação de múltiplas funções safe."""
        # Simular processamento de dados FUC
        name = safe_getitem(fuc_projection_data, "full_name", "Unknown")
        birth_date = safe_getitem(fuc_projection_data, "birth_date")
        age_iso = safe_isoformat(birth_date)
        
        assert name == "João Silva"
        assert age_iso == "2000-01-15"
    
    def test_safe_with_incomplete_data(self):
        """Testa safe_apply com dados incompletos."""
        data = {"price": "19.99", "quantity": "5"}
        
        price = safe_apply(data, "price", lambda x: float(x), 0.0)
        quantity = safe_apply(data, "quantity", lambda x: int(x), 0)
        total = price * quantity
        
        assert price == 19.99
        assert quantity == 5
        import pytest
        assert total == pytest.approx(99.95)
