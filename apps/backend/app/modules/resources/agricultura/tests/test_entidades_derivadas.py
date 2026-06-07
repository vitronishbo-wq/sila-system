from __future__ import annotations

from apps.backend.app.modules.resources.agricultura.domain.enums import (
    StatusEquipamento,
    StatusPlantio,
    StatusTalhao,
    TipoEquipamento,
)
from apps.backend.app.modules.resources.agricultura.domain.models.colheita import Colheita
from apps.backend.app.modules.resources.agricultura.domain.models.equipamento import Equipamento
from apps.backend.app.modules.resources.agricultura.domain.models.plantio import Plantio
from apps.backend.app.modules.resources.agricultura.domain.models.talhao import Talhao


def test_talhao_criacao_e_transicao_status():
    talhao = Talhao.criar(
        codigo_propriedade="PROP/2026/000001",
        nome="Talhao A",
        area_ha=12.5,
        tipo_solo="argiloso",
        irrigado=True,
    )
    assert talhao.status == StatusTalhao.ATIVO
    talhao.desativar()
    assert talhao.status == StatusTalhao.INATIVO
    talhao.ativar()
    assert talhao.status == StatusTalhao.ATIVO


def test_plantio_fluxo_planejar_executar_cancelar():
    plantio = Plantio.planejar(
        codigo_safra="SAF/2026/000001",
        codigo_talhao="TAL/2026/000001",
        area_plantada_ha=5.0,
        quantidade_semente=120.0,
    )
    assert plantio.status == StatusPlantio.PLANEJADO
    plantio.executar()
    assert plantio.status == StatusPlantio.EXECUTADO
    try:
        plantio.cancelar("mudanca de plano")
        raise AssertionError("cancelamento de plantio executado deveria falhar")
    except ValueError as exc:
        assert "executado" in str(exc)


def test_colheita_calcula_quantidade_liquida():
    colheita = Colheita.registrar(
        codigo_safra="SAF/2026/000001",
        codigo_talhao="TAL/2026/000001",
        quantidade_colhida_ton=18.75,
        perdas_ton=1.25,
        umidade_percentual=13.2,
    )
    assert colheita.quantidade_liquida_ton == 17.5


def test_colheita_invalida_quando_perda_excede_quantidade():
    try:
        Colheita.registrar(
            codigo_safra="SAF/2026/000001",
            codigo_talhao="TAL/2026/000001",
            quantidade_colhida_ton=2.0,
            perdas_ton=2.5,
        )
        raise AssertionError("perda maior que quantidade deveria falhar")
    except ValueError as exc:
        assert "Perdas" in str(exc)


def test_equipamento_fluxo_uso_manutencao_inativacao():
    equipamento = Equipamento.cadastrar(
        nome="Trator 110cv",
        tipo=TipoEquipamento.TRATOR,
        fabricante="AgroTech",
        modelo="AT-110",
        ano_fabricacao=2023,
    )
    assert equipamento.status == StatusEquipamento.DISPONIVEL
    equipamento.iniciar_uso()
    equipamento.registrar_uso(3.5)
    equipamento.finalizar_uso()
    assert equipamento.status == StatusEquipamento.DISPONIVEL
    assert equipamento.horas_uso == 3.5
    equipamento.enviar_manutencao()
    assert equipamento.status == StatusEquipamento.EM_MANUTENCAO
    equipamento.concluir_manutencao()
    assert equipamento.status == StatusEquipamento.DISPONIVEL
    equipamento.inativar()
    assert equipamento.status == StatusEquipamento.INATIVO


def test_equipamento_ano_fabricacao_invalido():
    try:
        Equipamento.cadastrar(
            nome="Pulverizador XP", tipo=TipoEquipamento.PULVERIZADOR, ano_fabricacao=1940
        )
        raise AssertionError("ano invalido deveria falhar")
    except ValueError as exc:
        assert "Ano de fabricacao invalido" in str(exc)
