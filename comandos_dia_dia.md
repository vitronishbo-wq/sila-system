/home/dev03wsl/sila-system/ROOT_CAUSE_AND_FIX_PLAN.md



emails=(
  "canzu024@gmail.com    - antigravit  - vs code"
  "a.j.fec.trade@gmail.com - gravity  - vs code"
  "silamarco217@gmail.com  - gravity  - vs code*"
  "1silajaneiro@gmail.com  - antigravit  - vs code"
  "2silajaneiro@gmail.com  - antigravit  - vs code"
  "3silajaneiro@gmail.com  - antigravit  - vs code"
  "4silajaneiro@gmail.com  - vs code  - antigravit"
  "silajaneiro5@gmail.com  - vs code  - antigravit"
  "silajaneiro4@gmail.com  - vs code  - antigravit"
  "silajaneiro009@gmail    - antigravit  - vs code"
  "silajaneiro9@gmail.com - vs code   - antigravit"
  "silajaneiro12@gmail.com - antigravit   - vs code"

  "jomacomercial22024@gmail.com  - vs code"
  "luzayamocomercial2024@gmail.com  - vs code"
  "nacassinguecomercial2024@gmail.com - vs code"
  "mwangonortcomercial2024@gmail.com  - vs code"
  "cossenguecomercial2024@gmail.com  - vs code"
  "jomacomercial2024@gmail.com  - vs code"
  "mucuenocomercial2024@gmail.com  - vs code"
  "recreativocomercial2024@gmail.com  - vs code"
  "silafevereiro793@gmail.com  - vs code"
  "silaabril24@gmail.com   - vs code"
  "silajaneiro8@gmail.com - vs code"
  "silajaneiro11@gmail.com - Truman1_1* - vs code"
  "janeirosila9@gmail.com  - vs code"
  "ssilajaneiro0@gmail.com  - vs code"
  "ssilajaneiro1@gmail.com  - vs code"
  "ssilajaneiro2@gmail.com  

  "jomacomercial12024@gmail.com"
  "trumanmarcelo@gmail.com"
  "wtmedia0@gmail.com"
  "ideolidia019@gmail.com"
  "silamaio356@gmail.com"
  "silajunho41@gmail.com   - gravity"
  "silaagosto83@gmail.com - gravity"
  "silasetembro83@gmail.com - gravity"
  "silajaneiro009@gmail.com - gravity"
  "fevereirosila0@gmail.com"
  "fevereirosila1@gmail.com"
  "fevereirosila55@gmail.com"
)




daily_commands=(
  # =========================
  # VS Code / Extensões
  # =========================
  "code --install-extension GitHub.copilot-chat --force"
  "code --list-extensions | grep copilot"

  # =========================
  # Git / Repositório
  # =========================
  "echo \"# sila-system\" >> README.md"
  "git init"
  "git add README.md"
  "git commit -m \"first commit\""
  "git branch -M main"
  "git remote add origin https://github.com/vitronishbo-wq/sila-system.git"
  "git push -u origin main"

  # =========================
  # Servidor / Uvicorn
  # =========================
  "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
  "sudo lsof -i :8000"
  "sudo kill -9 <PID>"

  # =========================
  # Seeds / Inicialização
  # =========================
  "python seeds/core/seed_angola_dpa_2024_v2.py"

  # =========================
  # Ambiente / Virtualenv
  # =========================
  "cd ~/sila-system/apps/backend && source .venv/bin/activate"

  # =========================
  # Banco de Dados / Postgres
  # =========================
  "sudo -u postgres psql -d sila_system"
  "PGPASSWORD='Trumanmarcelo_1983' psql -h 127.0.0.1 -U sila_user -d sila_system_test"
  "alembic -c alembic_core/alembic.ini current"

  psql -h 127.0.0.1 -U sila_user -d sila_db \
> -c "SELECT email, administrative_level, roles, is_active, hashed_password FROM users ORDER BY email;"

  # =========================
  # Estrutura / Tree
  # =========================
  tree -L 18 -I \"venv|__pycache__|*.egg-info|node_modules|dist|build\" && app/modules
  "tree -L 4"

  # =========================


E‑mails listados
ADMIN_CENTRAL → central@sila.gov.ao
ADMIN_PROVINCIAL (Huambo) → prov.huambo@sila.gov.ao
ADMIN_MUNICIPAL (Huambo) → mun.huambo@sila.gov.ao
ADMIN_COMMUNAL (Huambo) → comun.huambo@sila.gov.ao
CITIZEN → truman@gmail.com
Senha universal pra tudo: Sila_1983













































Sila System - Configuração Local
Serviços (WSL/Ubuntu)
PostgreSQL: sudo service postgresql start (Porta: 5432)
Redis: sudo service redis-server start (Porta: 6379)
Credenciais Banco de Dados (PostgreSQL)
Host: 127.0.0.1
Porta: 5432
Usuário: sila_user
Senha db: Trumanmarcelo_1983
Senha sudo: Truman1*
Database: sila_db
Configuração .env (Backend)
POSTGRES_HOST=127.0.0.1
REDIS_HOST=127.0.0.1
DATABASE_URL=postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
Execução Backend
Diretório: ~/sila-system/apps/backend
Ativação: source .venv/bin/activate
Comando: python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Comandos de Banco
Migração: python -m alembic upgrade head
Acesso psql: sudo -u postgres psql