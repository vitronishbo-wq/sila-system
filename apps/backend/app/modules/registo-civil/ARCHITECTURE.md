# Arquitetura: Registo Civil

## Contexto
Registo de nascimentos, casamentos e obitos com integracao via X-Road.

## Entidades
- RegistoNascimento: dados de nascimento, filiacao, naturalidade
- RegistoObito: dados de obito, causa, local
- RegistoCasamento: dados de casamento, regime de bens

## Integracoes
- X-Road: notificacao de obito para bloqueio de BI
- Identity: actualizacao de perfil do cidadao
