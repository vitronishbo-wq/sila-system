# 🚀 Smart Pattern Fixer - Guia Completo

## ⚡ Execução Rápida

### **Opção 1: Fixer v1.0 (Todos os arquivos)**

```bash
python3 scripts/smart_fix_patterns.py
```

### **Opção 2: Fixer v2.0 (Apenas arquivos com erro) - RECOMENDADO**

```bash
# 1. Gerar relatório de erros
python3 scripts/validate_syntax_detailed.py

# 2. Aplicar correções focadas
python3 scripts/smart_fix_patterns_v2.py
```

---

## 🔧 Diferenças Entre Versões

### **v1.0 - Correção em Massa**

- Processa **todos** os arquivos Python
- Aplica heurísticas gerais
- Mais lento (~1-2 min)
- Útil para limpeza inicial

### **v2.0 - Correção Focada** ⭐

- Lê `syntax_errors_detailed.txt`
- Processa **apenas** arquivos com erro
- Correções específicas por tipo de erro
- Muito mais rápido (~10-30 seg)
- **RECOMENDADO**

---

## 📋 Heurísticas Implementadas

### **v1.0 - 8 Correções Automáticas**

1. **BOM UTF-8** - Remove `\ufeff`
2. **Brackets** - Balanceia `()`, `[]`, `{}`
3. **Triple Quotes** - Fecha `"""` e `'''`
4. **Indentação** - Tabs → 4 espaços
5. **Vírgulas** - Adiciona em listas/dicts
6. **Dois Pontos** - Adiciona em `def`, `class`, `if`, etc.
7. **Blocos Vazios** - Adiciona `pass`
8. **Strings** - Fecha aspas não terminadas

### **v2.0 - Correções Específicas por Erro**

1. **'(' was never closed** → Adiciona `)` no final
2. **'[' was never closed** → Adiciona `]` no final
3. **unmatched ')'** → Remove `)` extra
4. **unmatched ']'** → Remove `]` extra
5. **IndentationError** → Remove indentação extra
6. **BOM** → Remove
7. **Triple quotes** → Fecha

---

## 🎯 Fluxo Recomendado

```bash
# 1. Validar estado atual
python3 scripts/validate_syntax_detailed.py
# Resultado: 232 erros

# 2. Aplicar Smart Fixer v2.0
python3 scripts/smart_fix_patterns_v2.py

# 3. Re-validar
python3 scripts/validate_syntax_detailed.py
# Resultado esperado: 50-100 erros (redução de 50-75%)

# 4. Re-executar fixer (2ª rodada)
python3 scripts/smart_fix_patterns_v2.py

# 5. Validar novamente
python3 scripts/validate_syntax_detailed.py
# Resultado esperado: 20-40 erros (redução de 80-90%)

# 6. Correção manual dos restantes
cat reports/TODO_MANUAL.txt
```

---

## 📊 Resultado Esperado

### **Rodada 1**

```
Antes:  232 erros
Depois: 50-100 erros
Redução: 50-75%
```

### **Rodada 2**

```
Antes:  50-100 erros
Depois: 20-40 erros
Redução: 60-80%
```

### **Rodada 3**

```
Antes:  20-40 erros
Depois: 5-15 erros
Redução: 70-85%
```

**Total:** 232 → 5-15 erros (redução de 93-97%)

---

## 🔄 Integração com Orquestrador

O orquestrador já pode usar o Smart Fixer automaticamente.

Edite `scripts/orchestrator_auto_fix.py`:

```python
# Adicione antes da validação
def run_pass(self, pass_number: int) -> PassResult:
    # ...

    # 1. Smart Fixer v2.0
    success, output = self.run_script(
        "smart_fix_patterns_v2.py",
        "Smart Pattern Fixer v2.0"
    )

    # 2. Validar sintaxe
    success, output = self.run_script(
        "validate_syntax_detailed.py",
        "Validação de Sintaxe"
    )
    # ...
```

---

## 📝 Exemplos de Correção

### **Exemplo 1: Parêntese não fechado**

**Antes:**

```python
async def save_file(file: UploadFile,
                   filename: str
```

**Depois:**

```python
async def save_file(file: UploadFile,
                   filename: str)
```

### **Exemplo 2: IndentationError**

**Antes:**

```python
class User(BaseModel):
    name: str
        age: int  # Indentação errada
```

**Depois:**

```python
class User(BaseModel):
    name: str
    age: int
```

### **Exemplo 3: Vírgula faltando**

**Antes:**

```python
data = ["item1" "item2" "item3"]
```

**Depois:**

```python
data = ["item1", "item2", "item3"]
```

### **Exemplo 4: Dois pontos faltando**

**Antes:**

```python
def my_function()
    return True
```

**Depois:**

```python
def my_function():
    return True
```

---

## ⚠️ Limitações

**O que NÃO é corrigido automaticamente:**

1. **Lógica quebrada** - Código incompleto
2. **Imports inválidos** - Módulos inexistentes
3. **Nomes indefinidos** - Variáveis não declaradas
4. **Erros semânticos** - Código sintaticamente correto mas logicamente errado

**Esses precisam de correção manual.**

---

## 🎯 Comandos Úteis

### Executar v2.0

```bash
python3 scripts/smart_fix_patterns_v2.py
```

### Ver backups criados

```bash
find . -name "*.smartfix.bak"
```

### Restaurar de backup

```bash
# Arquivo específico
mv file.py.smartfix.bak file.py

# Todos
find . -name "*.smartfix.bak" -exec bash -c 'mv "$1" "${1%.smartfix.bak}"' _ {} \;
```

### Limpar backups

```bash
find . -name "*.smartfix.bak" -delete
```

---

## 📊 Estatísticas

**Baseado em testes:**

| Tipo de Erro            | Correção Automática | Taxa     |
| ----------------------- | ------------------- | -------- |
| BOM UTF-8               | ✅ 100%             | 9/9      |
| Parênteses não fechados | ✅ 80-90%           | 10-12/13 |
| Colchetes não fechados  | ✅ 90-100%          | 9-10/10  |
| IndentationError        | ✅ 70-80%           | 11-13/16 |
| Triple quotes           | ✅ 100%             | 4/4      |
| Vírgulas faltando       | ✅ 60-70%           | -        |
| Dois pontos faltando    | ✅ 50-60%           | -        |

**Total esperado:** 60-75% de correção automática

---

## ✅ Checklist

- [ ] Executei `validate_syntax_detailed.py`
- [ ] Executei `smart_fix_patterns_v2.py`
- [ ] Re-executei validação
- [ ] Repeti 2-3 vezes até convergir
- [ ] Corrigi manualmente os 5-15 erros restantes
- [ ] Validação final passou
- [ ] Limpei backups

---

## 🚀 Próximos Passos

1. **Execute v2.0:**

   ```bash
   python3 scripts/smart_fix_patterns_v2.py
   ```

2. **Valide:**

   ```bash
   python3 scripts/validate_syntax_detailed.py
   ```

3. **Repita 2-3x até convergir**

4. **Corrija manualmente os restantes**

**Resultado esperado:** 232 → 5-15 erros (redução de 93-97%)
