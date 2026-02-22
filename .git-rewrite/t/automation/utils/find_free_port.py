#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SILA System - Localizador de Porta Livre
=======================================

Este script identifica e imprime uma porta TCP não utilizada no sistema.
É usado para evitar conflitos de porta ao iniciar serviços, como em testes
com Docker.
"""

import socket
from contextlib import closing


def find_free_port():
    """Encontra uma porta TCP livre e a retorna."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        # Ligar à porta 0 permite que o SO escolha uma porta efêmera disponível
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


if __name__ == "__main__":
    print(find_free_port())
