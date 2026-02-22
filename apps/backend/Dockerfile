# --- STAGE 1: System Base (Ferramentas de Sistema) ---
FROM python:3.12-slim-bookworm AS system-base

# Cache estável: dependências de SO raramente mudam
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    libpq-dev \
    gcc \
    python3-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- STAGE 2: Dependencies (Instalação Pip com Cache Otimizado) ---
FROM system-base AS deps

# Argumento para definir qual arquivo de requisitos instalar (dev ou prod)
ARG REQUIREMENTS_FILE=requirements/prod.txt

# Copia APENAS os arquivos de requisitos para garantir que o cache do Docker
# só seja invalidado se as dependências mudarem de fato.
COPY requirements/base.txt /tmp/requirements/
COPY ${REQUIREMENTS_FILE} /tmp/requirements/install.txt

# Upgrade pip (Camada separada para cache do instalador)
RUN python -m pip install --upgrade pip

# Instalação das dependências (Camada que falhou anteriormente)
RUN python -m pip install --no-cache-dir --default-timeout=1000 -r /tmp/requirements/install.txt

# --- STAGE 3: Final Stage (Runtime Encurtada) ---
FROM system-base

# Copia as dependências pré-instaladas (Python packages) do estágio intermédio
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copia o código fonte (esta camada muda com frequência, fica no fim)
COPY apps/backend /app

# Garante que scripts de entrada tenham permissão e formato correto
RUN find . -name "*.sh" -exec sed -i 's/\r$//' {} \; && \
    chmod +x /app/entrypoint.sh

EXPOSE 8000

# O entrypoint gestiona migrações e espera pela DB
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]