# 🚀 Quick Migration Usage Guide

## Step 1: Preview Changes (Dry Run)

```bash
cd /home/mint/Desktop/sila-system
python3 scripts/migrate_pydantic_v1_to_v2.py --dry-run
```

**What this does:**

- ✅ Scans all Python files in `backend/app/`, `tests/`, and `scripts/`
- ✅ Shows exactly what will be changed
- ✅ Generates a detailed report
- ❌ Does NOT modify any files

**Expected output:**

```
Found 1226 Python files to scan

📝 backend/app/modules/service_hub/schemas/service_hub.py
  • @validator→@field_validator: 10
  • Import additions: 1

📊 MIGRATION SUMMARY
Files scanned:     1226
Files modified:    18

Transformations applied:
  • @validator → @field_validator:      29
  • @root_validator → @model_validator: 6
  • .dict() → .model_dump():            11
  • .json() → .model_dump_json():       10
  • .parse_obj() → .model_validate():   4
  • .from_orm() → .model_validate():    1

✅ Total transformations: 61
```

---

## Step 2: Apply Migration (With Backups)

```bash
python3 scripts/migrate_pydantic_v1_to_v2.py
```

**What this does:**

- ✅ Creates `.v1.bak` backup files for every modified file
- ✅ Applies all 7 transformation rules
- ✅ Automatically adds required imports
- ✅ Generates timestamped report

**Backup example:**

```
backend/app/modules/service_hub/schemas/service_hub.py      # Modified file
backend/app/modules/service_hub/schemas/service_hub.py.v1.bak  # Backup
```

---

## Step 3: Verify Changes

### Run Tests

```bash
cd backend
pytest tests/ -v
```

### Type Check

```bash
mypy backend/app --ignore-missing-imports
```

### Check Specific File

```bash
# View what changed
diff backend/app/modules/service_hub/schemas/service_hub.py.v1.bak \
     backend/app/modules/service_hub/schemas/service_hub.py
```

---

## Step 4: Update Pydantic Version

```bash
cd backend
pip install "pydantic>=2.0.0" --upgrade
```

---

## Rollback (If Needed)

### Option 1: Restore from backups

```bash
# Restore all files
find . -name "*.v1.bak" -exec bash -c 'mv "$1" "${1%.v1.bak}"' _ {} \;

# Restore specific file
mv backend/app/modules/service_hub/schemas/service_hub.py.v1.bak \
   backend/app/modules/service_hub/schemas/service_hub.py
```

### Option 2: Use Git

```bash
git checkout -- backend/app/
git checkout -- tests/
git checkout -- scripts/
```

---

## Advanced Options

### Migrate Without Backups (Not Recommended)

```bash
python3 scripts/migrate_pydantic_v1_to_v2.py --no-backup
```

### Migrate Specific Directory

Edit the script and modify `search_dirs`:

```python
search_dirs = [
    self.project_root / "backend" / "app" / "modules" / "citizenship",
]
```

---

## Example: Before & After

### Before (v1)

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    email: str

    @validator("email")
    def normalize_email(cls, v):
        return v.lower()
```

### After (v2) - Automatically Generated

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    email: str

    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower()
```

---

## Files That Will Be Modified

Based on dry-run results:

1. **Citizenship Schemas** (9 files)

   - `certidao_casamento.py`
   - `certidao_obito.py`
   - `atualizacao_endereco.py`
   - `emissao_passaporte.py`
   - `certidao_nascimento.py`
   - `regitro_eleitoral.py`
   - `declaracao_residencia.py`
   - `visto_permanencia.py`
   - `emissao_b_i.py`

2. **Service Hub** (1 file)

   - `service_hub.py` - 10 validators

3. **Training** (1 file)

   - `training.py` - 9 validators

4. **Tests** (1 file)

   - `test_schemas.py` - 2 `.dict()` calls

5. **Scripts** (6 files)
   - Various utility scripts

---

## Troubleshooting

### Issue: "No module named 'pydantic'"

**Solution:** Install dependencies first

```bash
cd backend
pip install -r requirements.txt
```

### Issue: Script doesn't find files

**Solution:** Run from project root

```bash
cd /home/mint/Desktop/sila-system
python3 scripts/migrate_pydantic_v1_to_v2.py --dry-run
```

### Issue: Permission denied

**Solution:** Make script executable

```bash
chmod +x scripts/migrate_pydantic_v1_to_v2.py
```

---

## Next Steps After Migration

1. ✅ Review migration report
2. ✅ Run test suite
3. ✅ Check for any manual fixes needed
4. ✅ Update `requirements.txt` with Pydantic v2
5. ✅ Commit changes
6. ✅ Clean up `.v1.bak` files after verification

```bash
# After successful verification, remove backups
find . -name "*.v1.bak" -delete
```

---

## Report Location

After running, check:

```
pydantic_migration_report_YYYYMMDD_HHMMSS.txt
```

This contains the full log of all changes made.
