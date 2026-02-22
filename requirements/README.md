# Requirements Directory

## ⚠️ DEPRECATION NOTICE

Este diretório é mantido apenas para compatibilidade com scripts legados.

**Os arquivos principais de dependências foram movidos para a raiz do projeto:**

```
sila-system/
├── requirements.txt         ← Use este (Produção)
├── requirements-dev.txt     ← Use este (Desenvolvimento)
├── requirements-test.txt    ← Use este (Testes)
└── requirements.lock        ← Gerado automaticamente
```

## 📁 Estrutura Antiga (Deprecated)

- `base.txt` - Dependências base (agora em `requirements.txt`)
- `dev.txt` - Dependências de desenvolvimento (agora em `requirements-dev.txt`)
- `security.txt` - Ferramentas de segurança
- `security-production.txt` - Segurança para produção
- `test.txt` - Dependências de teste (agora em `requirements-test.txt`)
- `complete.txt` - Gerado automaticamente por análise

## 🔄 Migração

Se você está usando os arquivos antigos em scripts, atualize para:

### Antes

```bash
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

### Depois

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 📚 Documentação

Para mais informações sobre a nova estrutura de dependências, consulte:

- `DEPENDENCIES_REVIEW.md` na raiz do projeto
- `scripts/analyze_dependencies.py` - Script de análise automática

## 🗑️ Remoção Planejada

Estes arquivos serão removidos em uma versão futura após migração completa de todos os
scripts.

**Data Planejada:** Após validação completa da nova estrutura
