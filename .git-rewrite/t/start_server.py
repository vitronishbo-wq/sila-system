#!/usr/bin/env python3
import os
import sys
import subprocess

os.chdir('/home/truman/dev/sila-system/apps/backend')
sys.path.insert(0, '.')

# Ativate venv e iniciar uvicorn
cmd = [
    sys.executable, '-m', 'uvicorn',
    'main:app',
    '--reload',
    '--host', '0.0.0.0',
    '--port', '8000'
]

print(f"Starting server: {' '.join(cmd)}")
subprocess.run(cmd)
