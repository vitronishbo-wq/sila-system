#!/bin/bash
echo "🔧 Inicializando SILA System..."

# Ativar ambiente virtual
source /opt/sila-system/backend/venv/bin/activate

# Instalar dependências
pip install -r /opt/sila-system/backend/requirements.txt

# Rodar migrations
alembic upgrade head

# Iniciar monitoramento
bash /opt/sila-system/scripts/start_monitoring.sh

# Validar modelos
python3 -c 'from modules.education.models.ensino_superior import *; print("✅ Modelos OK")'

echo "✅ Bootstrap completo!"
