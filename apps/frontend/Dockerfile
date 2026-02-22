# Estágio 1: Build
FROM node:20-alpine AS builder
WORKDIR /app

# Otimização de rede para o npm em ambientes com instabilidade
RUN npm config set registry https://registry.npmjs.org/ && \
    npm config set fetch-retries 10 && \
    npm config set fetch-retry-mintimeout 30000 && \
    npm config set fetch-retry-maxtimeout 120000

# Instalação de dependências
COPY package*.json ./
RUN for i in 1 2 3 4 5; do \
    npm install --no-audit && break || \
    (echo "Tentativa $i falhou, tentando novamente em 15s..." && sleep 15); \
    done

# Construção do projeto
COPY . .
# Define a variável de ambiente para o build do Vite
ARG VITE_API_URL=/api/v1
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Estágio 2: Runner (Servidor Nginx leve)
FROM nginx:stable-alpine AS runner

# Configuração customizada do Nginx para Single Page Application (SPA)
RUN echo 'server { \
    listen 80; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html; \
    try_files $uri $uri/ /index.html; \
    } \
    }' > /etc/nginx/conf.d/default.conf

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]