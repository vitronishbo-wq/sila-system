# Virtual Environment Standard for SILA System

## 🎯 Official Virtual Environment

The **official Python virtual environment** for this project is located at:

```
/opt/sila-system/backend/venv/
```

## ✅ Activation Commands

### Linux/Mac

```bash
source /opt/sila-system/backend/venv/bin/activate
```

### Windows

```bash
/opt/sila-system/backend/venv/Scripts/activate
```

## 📋 Usage Guidelines

1. **All Python dependencies** must be installed and managed within this environment
2. **All scripts and services** should use the Python interpreter from this environment
3. **Development and testing** should be performed using this environment

## 🔧 Environment Verification

To verify you're using the correct environment:

```bash
which python
# Should return: /opt/sila-system/backend/venv/bin/python

python --version
# Should return: Python 3.12.3
```

## 📁 Project Structure

```
/opt/sila-system/
├── backend/
│   ├── venv/          # ✅ Official virtual environment
│   ├── requirements.txt
│   └── ...
├── requirements.txt   # Root requirements (for reference)
└── ...
```

## 🚫 Prohibited Actions

- Do not create additional virtual environments in the project
- Do not use system Python or other virtual environments
- Do not modify the .gitignore entries for virtual environments

## 📝 Maintenance

- Keep the environment updated with: `pip install -r backend/requirements.txt`
- Regularly clean up unused packages: `pip autoremove`
- Document any new dependencies in `backend/requirements.txt`

## 🔍 Troubleshooting

If you encounter issues:

1. **Environment not found**: Recreate using
   `python -m venv /opt/sila-system/backend/venv`
2. **Dependency issues**: Reinstall using `pip install -r backend/requirements.txt`
3. **Path issues**: Ensure your PATH includes the venv bin directory

---

_Last updated: 2025-10-23_
