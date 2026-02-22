"""
Testes para Safe Helpers - Utilitários de Acesso Seguro
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
)


class TestSafeGetBasic:
    """Testes básicos para safe_get"""
    
    def test_safe_get_existing_attribute(self):
        """Testa acesso a atributo existente"""
        class User:
            name = "João"
        
        user = User()
        assert safe_get(user, "name") == "João"
    
    def test_safe_get_missing_attribute_returns_none(self):
        """Testa que atributo faltando retorna None"""
        class User:
            name = "João"
        
        user = User()
        assert safe_get(user, "age") is None
    
    def test_safe_get_with_default(self):
        """Testa default customizado"""
        class User:
            name = "João"
        
        user = User()
        assert safe_get(user, "age", 18) == 18
        assert safe_get(user, "age", "unknown") == "unknown"
    
    def test_safe_get_none_object(self):
        """Testa com objeto None"""
        assert safe_get(None, "attr", "default") == "default"


class TestSafeGetItem:
    """Testes para safe_getitem"""
    
    def test_safe_getitem_existing_key(self):
        """Testa acesso a chave existente"""
        data = {"name": "João", "age": 30}
        assert safe_getitem(data, "name") == "João"
        assert safe_getitem(data, "age") == 30
    
    def test_safe_getitem_missing_key(self):
        """Testa chave faltando"""
        data = {"name": "João"}
        assert safe_getitem(data, "age") is None
    
    def test_safe_getitem_with_default(self):
        """Testa default customizado"""
        data = {"name": "João"}
        assert safe_getitem(data, "age", 99) == 99
    
    def test_safe_getitem_non_dict(self):
        """Testa com objeto que não é dicionário"""
        assert safe_getitem("not dict", "key", "default") == "default"
        assert safe_getitem(123, "key", "default") == "default"


class TestSafeIsoformat:
    """Testes para safe_isoformat"""
    
    def test_safe_isoformat_date(self):
        """Testa conversão de date"""
        d = date(2026, 2, 16)
        assert safe_isoformat(d) == "2026-02-16"
    
    def test_safe_isoformat_datetime(self):
        """Testa conversão de datetime"""
        dt = datetime(2026, 2, 16, 14, 30, 45)
        result = safe_isoformat(dt)
        assert "2026-02-16" in result
        assert "14:30:45" in result
    
    def test_safe_isoformat_none(self):
        """Testa com None"""
        assert safe_isoformat(None) is None
    
    def test_safe_isoformat_invalid(self):
        """Testa com tipo inválido"""
        assert safe_isoformat("not a date") is None
        assert safe_isoformat(123) is None


class TestSafeNumericConversions:
    """Testes para conversões numéricas"""
    
    def test_safe_int_from_string(self):
        """Testa conversão string para int"""
        assert safe_int("42") == 42
        assert safe_int("-10") == -10
        assert safe_int("0") == 0
    
    def test_safe_int_invalid(self):
        """Testa conversão inválida"""
        assert safe_int("not a number") == 0
        assert safe_int("not a number", -1) == -1
        assert safe_int(None, 99) == 99
    
    def test_safe_float_from_string(self):
        """Testa conversão string para float"""
        assert safe_float("42.5") == 42.5
        assert safe_float("-10.1") == -10.1
    
    def test_safe_float_invalid(self):
        """Testa conversão inválida"""
        assert safe_float("not a number") == 0.0
        assert safe_float("not a number", -1.5) == -1.5


class TestSafeStringConversion:
    """Testes para safe_str"""
    
    def test_safe_str_from_various_types(self):
        """Testa conversão de vários tipos"""
        assert safe_str(42) == "42"
        assert safe_str(42.5) == "42.5"
        assert safe_str(True) == "True"
        assert safe_str("already string") == "already string"
    
    def test_safe_str_from_none(self):
        """Testa conversão de None"""
        assert safe_str(None) == ""
        assert safe_str(None, "default") == "default"


class TestSafeBoolConversion:
    """Testes para safe_bool"""
    
    def test_safe_bool_from_bool(self):
        """Testa que bool já é bool"""
        assert safe_bool(True) is True
        assert safe_bool(False) is False
    
    def test_safe_bool_from_string(self):
        """Testa conversão de string"""
        assert safe_bool("true") is True
        assert safe_bool("True") is True
        assert safe_bool("1") is True
        assert safe_bool("yes") is True
        assert safe_bool("false") is False
        assert safe_bool("0") is False
    
    def test_safe_bool_from_number(self):
        """Testa conversão de numbers"""
        assert safe_bool(1) is True
        assert safe_bool(0) is False
        assert safe_bool(0.0) is False
    
    def test_safe_bool_from_none(self):
        """Testa conversão de None"""
        assert safe_bool(None) is False
        assert safe_bool(None, True) is True


# ============================================================================
# Integração
# ============================================================================

class TestSafeHelpersIntegration:
    """Testes de integração entre funções"""
    
    def test_combining_safe_functions(self):
        """Testa combinação de múltiplas funções"""
        data = {
            "name": "João",
            "age": "30",
            "active": "true",
            "created": date(2020, 1, 1)
        }
        
        name = safe_getitem(data, "name", "Unknown")
        age = safe_apply(data, "age", lambda x: int(x), 0) if "age" in data else 0
        active = safe_bool(safe_getitem(data, "active", "false"))
        created = safe_isoformat(safe_getitem(data, "created"))
        
        assert name == "João"
        assert active is True
        assert created == "2020-01-01"
    
    def test_safe_with_incomplete_data(self):
        """Testa com dados incompletos"""
        data = {"price": "19.99", "quantity": "5"}
        
        price = safe_float(safe_getitem(data, "price", "0"))
        quantity = safe_int(safe_getitem(data, "quantity", "0"))
        discount = safe_float(safe_getitem(data, "discount", "0"))
        
        total = (price * quantity) - discount
        
        assert price == 19.99
        assert quantity == 5
        assert discount == 0.0
        assert abs(total - 99.95) < 0.01  # Comparar com tolerância de float


import pytest
from app.modules.identidade_civil.utils.safe import safe_apply


class TestSafeApply:
    """Testes para safe_apply"""
    
    def test_safe_apply_with_valid_data(self):
        """Testa aplicação de função com dados válidos"""
        class Obj:
            value = "123"
        
        obj = Obj()
        result = safe_apply(obj, "value", int, 0)
        assert result == 123
    
    def test_safe_apply_with_missing_attr(self):
        """Testa com atributo faltando"""
        class Obj:
            pass
        
        obj = Obj()
        result = safe_apply(obj, "missing", int, 0)
        assert result == 0
    
    def test_safe_apply_with_lambda(self):
        """Testa com função lambda"""
        class Obj:
            name = "joão"
        
        obj = Obj()
        result = safe_apply(obj, "name", lambda x: x.upper(), "")
        assert result == "JOÃO"
