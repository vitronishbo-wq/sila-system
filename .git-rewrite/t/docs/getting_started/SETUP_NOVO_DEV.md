# 🚀 SETUP LIMPO - NOVO DESENVOLVEDOR

**Objetivo**: Configurar ambiente Python limpo sem histórico de venv **Tempo**: ~10
minutos **Pré-requisitos**: Git clonado, Python 3.12+

---

## ✅ Passo a Passo

### 1. Clone o Repositório (Git limpo)

```bash
git clone https://github.com/seu-org/sila-system.git
cd sila-system
```

**Resultado esperado**: Git está limpo, `backend/venv/` NÃO está no repo

---

### 2. Crie o Ambiente Virtual (Local)

```bash
cd backend
python3 -m venv venv
```

**Resultado esperado**: Novo diretório `backend/venv/` criado localmente

---

### 3. Ative o Ambiente (seu SO)

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
.\venv\Scripts\activate.bat
```

**Resultado esperado**: Prompt mostra `(venv)` no início

---

### 4. Instale Dependências

```bash
pip install -r requirements.txt
```

**Resultado esperado**: Todas as bibliotecas (NumPy, Django, etc.) instaladas localmente

---

### 5. Verifique Instalação

```bash
python --version
pip list | head -5
```

**Resultado esperado**: Python 3.12+ e pacotes listados

---

### 6. Git Ignore Automático

O `.gitignore` já está configurado. Você pode validar:

```bash
cd ..  # Volte para raiz
git status backend/venv/
```

**Resultado esperado**: Nenhuma mudança em `backend/venv/` (ignorado automaticamente)

---

## 🎯 Importante

### ✅ DO'S

- ✅ Crie `venv/` localmente em sua máquina
- ✅ Use `source venv/bin/activate` ou equivalente
- ✅ Instale pacotes com `pip install`
- ✅ Sempre use `pip freeze > requirements.txt` após adicionar pacotes
- ✅ Commit apenas `requirements.txt` (nunca `venv/`)

### ❌ DON'TS

- ❌ NÃO clone `backend/venv/` do Git (não está lá)
- ❌ NÃO committe a pasta `venv/` (`.gitignore` a ignora)
- ❌ NÃO instale pacotes globalmente (use venv)
- ❌ NÃO delete `requirements.txt` (outros precisam)

---

## 🔍 Checklist Final

- [ ] Git clonado limpo
- [ ] `backend/venv/` criado localmente
- [ ] Ambiente ativado (prompt mostra `(venv)`)
- [ ] Dependências instaladas
- [ ] Python version correto (3.12+)
- [ ] Git status mostra venv ignorado

---

## 📞 Troubleshooting

### "Não consigo ativar o venv"

```bash
# Verifique se venv foi criado
ls -la backend/venv/

# Se não existir, crie
python3 -m venv backend/venv

# Tente ativar novamente
source backend/venv/bin/activate
```

### "Pacotes não instalam"

```bash
# Verifique se está no venv (prompt deve mostrar (venv))
which python  # macOS/Linux - deve mostrar path com venv/
python -m pip install --upgrade pip

# Tente instalar novamente
pip install -r requirements.txt
```

### "Meu venv está sendo commitado"

```bash
# Adicione manualmente ao .gitignore (backup)
echo "backend/venv/" >> .gitignore
git rm -r --cached backend/venv/
git commit -m "Ignore backend/venv/"
```

---

## 📚 Documentação Relacionada

- Ver: `ENV_SETUP.md` - Setup completo (incluindo frontend)
- Ver: `GIT_CLEANUP_LOG.md` - Histórico de limpeza
- Ver: `.gitignore` - Regras de ignorar

---

## ✅ Status

**Setup Limpo**: ✅ PRONTO

Seu ambiente local está isolado do Git. Nenhum arquivo de venv será accidentalmente
commitado.

---

**Data**: 16 Nov 2025 **Versão**: 1.0
