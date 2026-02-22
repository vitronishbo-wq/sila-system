# ===========================================
# Frontend - Multi-stage Dockerfile
# Versão: 1.0 - Build otimizado com Nginx
# ===========================================

# ===========================
# Stage 1: Build
# ===========================
FROM node:20-alpine AS builder

# Metadados
LABEL stage=builder

# Variáveis de ambiente
ENV NODE_ENV=production \
    VITE_API_BASE_URL=http://localhost:8000/api/v1

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar TODAS as dependências (forçar dev)
RUN npm install --include=dev --verbose

# Copiar código-fonte
COPY . .

# Verificar que vite e typescript estão instalados
RUN ls -la node_modules/.bin/ | grep -E "(vite|tsc)" || echo "Warning: missing tools"

# Build com Vite
RUN npm run build

# ===========================
# Stage 2: Runtime (Nginx)
# ===========================
FROM nginx:alpine

# Metadados
LABEL maintainer="SILA System Team" \
      version="1.0" \
      description="Frontend React/Vite para Sistema SILA"

# Variáveis de ambiente
ENV NGINX_PORT=80 \
    VITE_API_BASE_URL=http://api:8000/api/v1

# Instalar curl para healthcheck
RUN apk add --no-cache curl

# Copiar arquivos de configuração Nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Copiar build do stage anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Expor porta
EXPOSE 80

# Iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]
