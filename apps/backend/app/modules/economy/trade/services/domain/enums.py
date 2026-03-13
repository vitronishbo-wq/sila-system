from __future__ import annotations
from enum import Enum

class TipoEstabelecimentoComercial(Enum):
    MATRIZ = 'matriz'
    FILIAL = 'filial'
    FRANQUIA = 'franquia'
    REPRESENTACAO = 'representacao'
    LOJA = 'loja'
    QUIOSQUE = 'quiosque'
    TRAILER = 'trailer'
    AMBULANTE = 'ambulante'

class RamoComercial(Enum):
    VAREJISTA = 'varejista'
    ATACADISTA = 'atacadista'
    ELETRONICO = 'eletronico'
    SUPERMERCADO = 'supermercado'
    FARMACIA = 'farmacia'
    VESTUARIO = 'vestuario'
    CALCADOS = 'calcados'
    MOVEIS = 'moveis'
    ELETRODOMESTICOS = 'eletrodomesticos'
    ELETRONICOS = 'eletronicos'
    MATERIAL_CONSTRUCAO = 'material_construcao'
    AUTOMOTIVO = 'automotivo'
    ALIMENTACAO = 'alimentacao'
    BEBIDAS = 'bebidas'
    COMBUSTIVEL = 'combustivel'
    SERVICOS = 'servicos'
    SAUDE = 'saude'
    EDUCACAO = 'educacao'
    HOSPEDAGEM = 'hospedagem'
    LAZER = 'lazer'
    CULTURA = 'cultura'
    FINANCEIRO = 'financeiro'
    IMOBILIARIO = 'imobiliario'

class PorteComercial(Enum):
    MICRO = 'micro'
    PEQUENA = 'pequena'
    MEDIA = 'media'
    GRANDE = 'grande'
    EMPORIO = 'emporio'

class StatusComercial(Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    SUSPENSO = 'suspenso'
    LICENCIAMENTO = 'licenciamento'
    REFORMA = 'reforma'
    INTERDITADO = 'interditado'
    FALENCIA = 'falencia'

class TipoRegimeTributario(Enum):
    SIMPLES_NACIONAL = 'simples_nacional'
    LUCRO_PRESUMIDO = 'lucro_presumido'
    LUCRO_REAL = 'lucro_real'
    MEI = 'mei'

class TipoPagamento(Enum):
    DINHEIRO = 'dinheiro'
    CARTAO_CREDITO = 'cartao_credito'
    CARTAO_DEBITO = 'cartao_debito'
    PIX = 'pix'
    TRANSFERENCIA = 'transferencia'
    BOLETO = 'boleto'
    CHEQUE = 'cheque'
    VALE = 'vale'
    CREDIARIO = 'crediario'
    CARNE = 'carne'

class TipoEntrega(Enum):
    RETIRADA = 'retirada'
    DELIVERY = 'delivery'
    FRETE = 'frete'
    EXPRESSA = 'expressa'
    AGENDADA = 'agendada'

class StatusPedido(Enum):
    ORCAMENTO = 'orcamento'
    AGUARDANDO_PAGAMENTO = 'aguardando_pagamento'
    PAGO = 'pago'
    EM_PREPARACAO = 'em_preparacao'
    PRONTO = 'pronto'
    EM_TRANSPORTE = 'em_transporte'
    ENTREGUE = 'entregue'
    CANCELADO = 'cancelado'
    TROCADO = 'trocado'
    DEVOLVIDO = 'devolvido'

class TipoFidelidade(Enum):
    PONTOS = 'pontos'
    MILHAS = 'milhas'
    CASHBACK = 'cashback'
    DESCONTO = 'desconto'
    BRINDES = 'brindes'

class TipoReclamacao(Enum):
    PRODUTO = 'produto'
    SERVICO = 'servico'
    ENTREGA = 'entrega'
    PAGAMENTO = 'pagamento'
    ATENDIMENTO = 'atendimento'
    GARANTIA = 'garantia'
    TROCA = 'troca'
    DEVOLUCAO = 'devolucao'