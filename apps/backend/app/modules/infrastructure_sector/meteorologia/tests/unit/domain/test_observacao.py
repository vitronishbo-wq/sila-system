from app.modules.infrastructure_sector.meteorologia.domain.enums import AlertType
from app.modules.infrastructure_sector.meteorologia.domain.models import ObservacaoMeteorologica

def test_criar_observacao_basica() -> None:
    obs = ObservacaoMeteorologica(temperatura=25.5, humidade=60.0, pressao=1013.25)
    assert obs.temperatura == 25.5
    assert obs.humidade == 60.0
    assert obs.has_alerts is False

def test_alerta_temperatura_extrema() -> None:
    obs = ObservacaoMeteorologica(temperatura=42.0, humidade=45.0, pressao=1012.0)
    alertas = obs.analisar_severidade()
    assert len(alertas) == 1
    assert alertas[0]['tipo'] == AlertType.HEAT_WAVE.value
    assert obs.has_alerts is True

def test_alerta_humidade_critica() -> None:
    obs = ObservacaoMeteorologica(temperatura=35.0, humidade=15.0, pressao=1010.0)
    alertas = obs.analisar_severidade()
    assert len(alertas) >= 1
    assert any((a['tipo'] == AlertType.DROUGHT.value for a in alertas))

def test_multiplos_alertas() -> None:
    obs = ObservacaoMeteorologica(temperatura=45.0, humidade=10.0, velocidade_vento=100.0)
    alertas = obs.analisar_severidade()
    assert len(alertas) >= 3
    assert obs.has_alerts is True

def test_validar_dados_temperatura_invalida() -> None:
    obs = ObservacaoMeteorologica(temperatura=70.0)
    warnings = obs.validar_dados()
    assert len(warnings) >= 1
    assert 'Temperatura fora de faixa' in warnings[0]

def test_validar_dados_humidade_invalida() -> None:
    obs = ObservacaoMeteorologica(humidade=150.0)
    warnings = obs.validar_dados()
    assert len(warnings) >= 1
    assert 'Humidade invalida' in warnings[0]

def test_to_dict_inclui_alertas() -> None:
    obs = ObservacaoMeteorologica(temperatura=42.0)
    obs.analisar_severidade()
    data = obs.to_dict()
    assert 'alertas' in data
    assert 'has_alerts' in data
    assert data['has_alerts'] is True
    assert len(data['alertas']) >= 1