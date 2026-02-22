# SILA System – Setup Guide

## 1. Clone o repositório

git clone https://github.com/sila-system/sila.git cd sila

## 2. Crie e ative o ambiente virtual

python3 -m venv backend/venv source backend/venv/bin/activate

## 3. Instale as dependências

pip install -r backend/requirements.txt

## 4. Execute os testes de modelo

python3 -c 'from modules.education.models.ensino_superior import \*; print("✅ Modelos
OK")'

## 5. Execute o deploy

./deploy_official.sh --env=development --services=backend

## 6. Verifique o monitoramento

python3 health/health_checker.py
