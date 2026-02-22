# Master Index Generator - Guia de Uso

## 📋 Visão Geral

Script profissional para indexar, filtrar e exportar metadados de arquivos de código com
suporte a:

- **Metadados**: tamanho (bytes/KB/MB), data de modificação
- **Filtros**: extensão, tamanho, data, profundidade
- **Saídas**: TXT, JSON, CSV
- **Performance**: processamento paralelo (ThreadPoolExecutor)
- **Segurança**: suporte a .gitignore

## 🚀 Instalação Rápida

```bash
chmod +x master_index_generator.py
```

## 📝 Uso Básico

### 1️⃣ Indexar todos os arquivos Python

```bash
python3 master_index_generator.py . --ext py
```

**Saída:**

- `all_code_index.txt` (índice formatado)
- Resumo estatístico no console

### 2️⃣ Múltiplas extensões, sorted by size

```bash
python3 master_index_generator.py . \
  --ext py js ts cpp c java \
  --sort size \
  --csv --json
```

**Exports:**

- `all_code_index.txt` (sempre)
- `all_code_index.json` (com `--json`)
- `all_code_index.csv` (com `--csv`)

### 3️⃣ Respeitar .gitignore, excluir pastas

```bash
python3 master_index_generator.py . \
  --require-gitignore \
  --exclude node_modules venv __pycache__ .git
```

### 4️⃣ Filtrar por tamanho e data

```bash
python3 master_index_generator.py . \
  --ext py \
  --min-size 50 \
  --max-date 2024-11-01
```

- `--min-size 50`: apenas arquivos > 50 KB
- `--max-date 2024-11-01`: apenas antes de 1º nov 2024

### 5️⃣ Controlar profundidade de scan

```bash
python3 master_index_generator.py . \
  --ext py \
  --depth 3
```

Limita a busca a 3 níveis de profundidade

### 6️⃣ Dry-run com debug

```bash
python3 master_index_generator.py . \
  --ext py \
  --dry \
  --debug
```

- `--dry`: mostra o que seria incluído sem escrever arquivos
- `--debug`: log detalhado de cada passo

### 7️⃣ Incluir arquivos ocultos

```bash
python3 master_index_generator.py . \
  --include-hidden
```

Inclui arquivos que começam com `.` (ex: `.env`, `.gitignore`)

### 8️⃣ Controlar threads paralelos

```bash
python3 master_index_generator.py . \
  --workers 4
```

Usa 4 threads para extrair metadados (default: 8)

## 📊 Exemplos Práticos

### Exemplo 1: Análise de código Python

```bash
python3 master_index_generator.py /seu/projeto \
  --ext py \
  --exclude venv node_modules __pycache__ \
  --sort size \
  --csv --json
```

**Resultado:**

- Índice de todos os `.py`
- Maior para menor (sorted by size)
- Exportado em 3 formatos
- Pastas excludentes ignoradas

### Exemplo 2: Buscar arquivos grandes

```bash
python3 master_index_generator.py . \
  --ext py \
  --min-size 100 \
  --sort size
```

Encontra arquivos Python > 100 KB

### Exemplo 3: Auditoria de projeto completo

```bash
python3 master_index_generator.py . \
  --require-gitignore \
  --include-hidden \
  --sort name \
  --json
```

- Respeita `.gitignore`
- Inclui hidden files
- Ordem alfabética
- Exporta como JSON

### Exemplo 4: Scan limitado (performance test)

```bash
python3 master_index_generator.py . \
  --depth 2 \
  --ext py \
  --workers 2 \
  --dry \
  --debug
```

Test com 2 threads, profundidade limitada, sem escrever

## 📈 Formato de Saída

### TXT (Legível)

```
# Generated: 2025-11-18 03:58:26
# Project: /home/truman/dev/sila-system
# Total Files: 1099
# Sorted by: size
# Extensions: .py
# Excluded folders: venv, node_modules, __pycache__, .git

1. File: /path/to/file.py
   Size: 57.28 KB (58653 bytes)
   Extension: .py
   Last Modified: 2025-11-17 01:11:44
```

### CSV (Excel-compatible)

```
path,size_bytes,size_kb,size_mb,last_modified,extension
/path/to/file.py,58653,57.28,0.06,2025-11-17 01:11:44,.py
```

### JSON (Machine-readable)

```json
[
  {
    "path": "/path/to/file.py",
    "size_bytes": 58653,
    "size_kb": 57.28,
    "size_mb": 0.06,
    "last_modified": "2025-11-17 01:11:44",
    "is_file": true,
    "extension": ".py"
  }
]
```

## 🎯 Opções Completas

| Flag                  | Tipo       | Descrição            | Exemplo                     |
| --------------------- | ---------- | -------------------- | --------------------------- |
| `project`             | Positional | Diretório alvo       | `.` ou `/home/user/project` |
| `--ext`               | Multi      | Extensões            | `py js ts`                  |
| `--exclude`           | Multi      | Pastas para ignorar  | `venv node_modules`         |
| `--sort`              | Choice     | Ordem de saída       | `name` \| `size` \| `date`  |
| `--depth`             | Int        | Profundidade máxima  | `3`                         |
| `--min-size`          | Float      | Tamanho mín (KB)     | `50`                        |
| `--max-size`          | Float      | Tamanho máx (KB)     | `1000`                      |
| `--min-date`          | Date       | Data mín             | `2024-11-01`                |
| `--max-date`          | Date       | Data máx             | `2024-11-30`                |
| `--json`              | Flag       | Exportar JSON        | presente                    |
| `--csv`               | Flag       | Exportar CSV         | presente                    |
| `--dry`               | Flag       | Modo teste           | presente                    |
| `--debug`             | Flag       | Log detalhado        | presente                    |
| `--include-hidden`    | Flag       | Incluir `.` files    | presente                    |
| `--require-gitignore` | Flag       | Respeitar .gitignore | presente                    |
| `--workers`           | Int        | Threads paralelos    | `4` (default: 8)            |

## 🔥 Dicas & Truques

### Buscar top 10 arquivos maiores

```bash
python3 master_index_generator.py . --ext py --sort size
# Depois verificar as primeiras 11 linhas do .txt
```

### Exportar para Planilha Excel

```bash
python3 master_index_generator.py . --csv
# Abrir all_code_index.csv no LibreOffice/Excel
```

### Gerar relatório JSON para análise

```bash
python3 master_index_generator.py . \
  --ext py \
  --json \
  --sort date
# Parsear all_code_index.json com jq ou Python
```

### Auditoria rápida de mudanças recentes

```bash
python3 master_index_generator.py . \
  --min-date 2025-11-01 \
  --sort date \
  --json
```

### Performance: teste com poucos workers

```bash
python3 master_index_generator.py . --workers 2 --dry
```

## 🐛 Troubleshooting

### "No such file or directory"

```bash
# Usar caminho absoluto ou ./
python3 master_index_generator.py /home/user/project --ext py
```

### "Permission denied" (Windows/WSL)

```bash
# Via WSL:
wsl -e bash -c "cd /home/user/project && python3 master_index_generator.py ."
```

### Script muito lento

```bash
# Aumentar workers e excluir pastas grandes
python3 master_index_generator.py . \
  --workers 16 \
  --exclude venv node_modules .git __pycache__ build dist
```

### Output muito grande

```bash
# Limitar por extensão
python3 master_index_generator.py . --ext py  # não all
# Ou usar min-size
python3 master_index_generator.py . --min-size 50
```

## 📦 Casos de Uso

✅ **Code Audits**: revisar todos os arquivos do projeto ✅ **Size Analysis**: encontrar
bloat no código ✅ **Reporting**: gerar índices para documentação ✅ **Quality Gates**:
validar estrutura de módulos ✅ **Migration**: mapear arquivos para refatoring ✅
**Compliance**: rastrear mudanças recentes

---

**Versão:** 1.0 **Autor:** Truman + ChatGPT **Data:** 2025-11-18
