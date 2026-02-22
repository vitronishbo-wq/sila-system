# Governance Migration - Setup Instructions

## 🐛 Error: ModuleNotFoundError: No module named 'asyncpg'

This error occurs when the required Python dependencies are not installed in your
virtual environment.

## ✅ Solution

### Step 1: Install Dependencies

Make sure you're in the backend directory with your virtual environment activated, then
install the requirements:

```bash
cd ~/dev/sila-system/backend
source .venv/bin/activate  # or activate your venv
pip install -r requirements.txt
```

This will install `asyncpg` and all other required dependencies.

### Step 2: Verify Installation

Check if `asyncpg` is installed:

```bash
python -c "import asyncpg; print('✅ asyncpg installed:', asyncpg.__version__)"
```

### Step 3: Run Migration

Once dependencies are installed, run the migration:

```bash
alembic upgrade head
```

## 📋 Alternative: Install asyncpg Only

If you only need to install `asyncpg`:

```bash
pip install asyncpg==0.30.0
```

## 🔍 Troubleshooting

### If pip install fails:

1. **Update pip:**

   ```bash
   pip install --upgrade pip
   ```

2. **Check Python version:**

   ```bash
   python --version  # Should be 3.8+
   ```

3. **Verify virtual environment:**
   ```bash
   which python  # Should point to .venv/bin/python
   ```

### If you're using a different virtual environment:

Make sure you activate the correct virtual environment before installing:

```bash
# If using venv
source .venv/bin/activate

# If using conda
conda activate your_env_name

# If using poetry
poetry shell
```

## ✅ Expected Output

After successful installation and migration:

```
INFO  [alembic.runtime.migration] Context impl PostgresqlContext.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20250105_health -> 20250105_governance, Create governance module tables
```

## 🎯 Quick Commands

```bash
# Full setup (one-liner)
cd ~/dev/sila-system/backend && source .venv/bin/activate && pip install -r requirements.txt && alembic upgrade head
```

## 📝 Notes

- The `asyncpg` package is required for async PostgreSQL connections
- It's already listed in `requirements.txt` (version 0.30.0)
- Make sure your virtual environment is activated before installing
- The migration will create 4 tables: `institutions`, `mandates`, `council_meetings`,
  `decisions`
