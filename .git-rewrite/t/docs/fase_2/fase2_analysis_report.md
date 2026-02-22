📊 Resumo da Análise Fase 2 🔴 Nível 1: 21 scripts (intocáveis) 🟠 Nível 2: 14 scripts
(analisar antes) 🟢 Nível 3: 30 scripts (candidatos à consolidação) ⚠️ Duplicações
detectadas (hash exato): 0 🔗 Scripts com dependências internas/externas: 55

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/clean_pendrive_safe.sh 38: if [ -d
"/tmp" ] && mount | grep -q "/tmp"; then 118: read -p "⚠️ Esta operação irá remover
arquivos temporários. Continuar? (s/N): " -n 1 -r

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/safe_root_reorganizer.sh 154:echo "#
Mode: $( [ "$APPLY" = true ] && echo "APPLY" || echo "DRY-RUN" )" >> "$PLAN_FILE"
230:mapfile -d '' ROOT_FILES < <(find . -maxdepth 1 -type f -print0) 421: log_success
"Reorganização aplicada. Recomenda-se revisar com: git status"

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/cleanup_temp_files.sh 38:# 1. Limpar
cache do Python 53:# 2. Limpar logs antigos 66:# 3. Limpar arquivos temporários do
projeto 83:# 4. Limpar node_modules cache (se existir) 97:# 5. Limpar containers Docker
parados (opcional)

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/restructure_project.sh 34: echo -e
"${GREEN}Movendo: $source -> $destination${NC}" 37: echo -e
"${RED}Aviso: $source não encontrado. Pulando.${NC}" 73: echo -e
"${RED}AVISO: Há mudanças não commitadas. Recomenda-se fazer commit antes de continuar.${NC}"
82:## 1. CRIAÇÃO DA NOVA ESTRUTURA DE DIRETÓRIOS 84:echo -e "
${BLUE}--- 1. CRIAÇÃO DE DIRETÓRIOS CHAVE ---${NC}" 141:## 2. REORGANIZAÇÃO DE ARQUIVOS
CHAVE E DIRETÓRIOS EXISTENTES 143:echo -e "
${BLUE}--- 2. REORGANIZAÇÃO DE ARQUIVOS EXISTENTES ---${NC}" 145:# A. Mover Scripts de
Automação 170:# B. Mover Ferramentas e Analisadores 184:# C. Mover Configurações 192:#
D. Mover Documentação 198:# E. Mover Infraestrutura 207:# F. Mover Requirements 217:# G.
Mover Scripts de CI/CD 223:# H. Mover Scripts de Diagnóstico 229:# I. Mover Arquivos de
Dados e Logs 237:## 3. AJUSTES ESPECIAIS E LIMPEZA 239:echo -e "
${BLUE}--- 3. AJUSTES FINAIS ---${NC}" 264:## 4. RELATÓRIO FINAL 274:echo "1.
${YELLOW}Revisar mudanças:${NC} git status" 275:echo "2.
${YELLOW}Refatorar imports:${NC} Atualizar caminhos nos arquivos movidos" 276:echo "3.
${YELLOW}Atualizar configurações:${NC} Makefile, docker-compose.yml, etc." 277:echo "4.
${YELLOW}Testar aplicação:${NC} Verificar se tudo funciona" 278:echo "5.
${YELLOW}Commit das mudanças:${NC} git commit -m 'Reorganização da estrutura do
projeto'"

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/cleanup_project.sh 27:# 1. REMOVER
DOCKER-COMPOSE REDUNDANTES 29:[ -f "devops/docker-compose.yml" ] && rm
"devops/docker-compose.yml" && log_success "Removido devops/docker-compose.yml" 30:[ -f
"scripts/docker-compose.yml" ] && rm "scripts/docker-compose.yml" && log_success
"Removido scripts/docker-compose.yml" 32:# 2. REMOVER SCRIPTS OBSOLETOS EM /devops
40:# 3. MOVER ARQUIVOS ÚTEIS PARA /devops/archive 46:[ -f "sila_up.sh" ] && mv
"sila_up.sh" "devops/archive/" && log_success "sila_up.sh arquivado" 48:# 4. REMOVER
SCRIPTS OBSOLETOS DA RAIZ 55:# 5. LIMPEZA MASSIVA DE DOCUMENTAÇÃO REDUNDANTE 63:# 6.
LIMPEZA DE DIRETÓRIOS VAZIOS E TEMPORÁRIOS 69:# 7. LIMPEZA DE ARQUIVOS DE BACKUP E
TEMPORÁRIOS 76:# 8. MOSTRAR ESTRUTURA FINAL LIMPA

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/repair_all_simple.sh 33:[ -f
"docker-compose.yml" ] && cp docker-compose.yml "$BACKUP_DIR/"

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/consolidate_root_scripts.sh
16:ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
76:  [[ -z "${SRC}" ]]
&& continue

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/cleanup_obsolete.sh 33:# 1. ARQUIVOS DE
COMANDOS OBSOLETOS 35:log_step "1. Removendo Arquivos de Comandos Obsoletos" 53:# 2.
DOCUMENTOS E RELATÓRIOS OBSOLETOS 55:log_step "2. Removendo Documentos e Relatórios
Obsoletos" 129:# 3. SCRIPTS PYTHON OBSOLETOS 131:log_step "3. Removendo Scripts Python
Obsoletos" 196:# 4. DIRETÓRIOS DE ARQUIVO ANTIGOS 198:log_step "4. Removendo Diretórios
de Arquivo" 207:# 5. READMES DUPLICADOS/OBSOLETOS 209:log_step "5. Removendo READMEs
Obsoletos" 229:# 6. RELATÓRIOS EM SUBDIRETÓRIOS 231:log_step "6. Removendo Relatórios em
Subdiretórios" 254:# 7. ARQUIVOS DE CONFIGURAÇÃO TEMPORÁRIOS 256:log_step "7. Removendo
Arquivos Temporários" 273:# 8. CRIAR ARQUIVO DE COMANDOS ESSENCIAIS 275:log_step "8.
Criando Arquivo de Comandos Essenciais" 282:### 🐳 **Docker & Desenvolvimento** 328:###
👤 **Usuários & Admin** 413:1. ./repair_all_simple.sh 414:2. docker compose up -d 415:3.
./scripts/generate-types.sh 420:1. docker compose up -d 421:2. # Desenvolver... 422:3.
docker compose logs -f backend # Ver logs 427:1. docker compose down 428:2.
./repair_all_simple.sh 429:3. docker compose up -d --build 434:1. ./start_enterprise.sh
--rebuild --frontend 435:2. # Verificar saúde dos serviços 436:3. curl -f
http://localhost:8000/health 447:# 9. VALIDAÇÃO FINAL 449:log_step "9. Validação Final"
475:# 10. RELATÓRIO FINAL 477:log_step "10. Relatório Final da Limpeza"

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/repair_all_runner.sh 59:log_step "1.
Criando Backup Completo" 62:[ -f "docker-compose.yml" ] && cp docker-compose.yml
"$BACKUP_DIR/"
63:[ -f "docker-compose.override.yml" ] && cp docker-compose.override.yml "$BACKUP_DIR/"
64:[ -d "frontend/packages/shared-api/src" ] && cp -r frontend/packages/shared-api/src
"$BACKUP_DIR/"
65:[ -f "frontend/apps/web/Dockerfile" ] && cp frontend/apps/web/Dockerfile "$BACKUP_DIR/"
72:log_step "2. Criando fix-backend.sh" 146:log_step "3. Atualizando fix-frontend.sh"
159:log_step "4. Executando Correções Básicas" 171: log_step "5. Configurando Hot
Reload" 207: log_step "6. Configurando Geração de Tipos TypeScript" 232: npm run
generate:types 2>/dev/null && log_success "Tipos TypeScript gerados!" || log_warning
"Falha ao gerar tipos - execute 'npm run generate:types' após subir o backend" 235:
log_warning "Backend não está rodando. Execute 'npm run generate:types' no frontend após
subir o backend" 245: log_step "7. Configurando Monitoring com Prometheus" 330:log_step
"8. Validação Final" 341:if [ -d "frontend/apps/web" ] && [ -d "frontend/packages" ];
then 356:log_step "9. Relatório Final"

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/cleanup_all_backups.sh 25:rm -f
docker-compose.yml.bak.20251103_135027 && echo -e "${GREEN}✅${NC}
docker-compose.yml.bak.20251103_135027" &&
DELETED_FILES=$((DELETED_FILES + 1))
26:rm -f docker-compose.dev.yml.bak.20251103_135027 && echo -e "${GREEN}✅${NC} docker-compose.dev.yml.bak.20251103_135027" && DELETED_FILES=$((DELETED_FILES +
1)) 27:rm -f docker-compose.migration.yml.bak.20251103_135027 && echo -e
"${GREEN}✅${NC} docker-compose.migration.yml.bak.20251103_135027" &&
DELETED_FILES=$((DELETED_FILES + 1))
28:rm -f docker-compose.test.yml.bak.20251103_135027 && echo -e "${GREEN}✅${NC} docker-compose.test.yml.bak.20251103_135027" && DELETED_FILES=$((DELETED_FILES +
1)) 29:rm -f devops/docker-compose.yml.bak.20251103_135027 && echo -e "${GREEN}✅${NC}
devops/docker-compose.yml.bak.20251103_135027" &&
DELETED_FILES=$((DELETED_FILES + 1))
32:rm -f scripts/preencher_env_critico.py.bak.20251103_135027 && echo -e "${GREEN}✅${NC} scripts/preencher_env_critico.py.bak.20251103_135027" && DELETED_FILES=$((DELETED_FILES +
1)) 33:rm -f scripts/preencher_env_critico_multi.py.bak.20251103_135027 && echo -e
"${GREEN}✅${NC} scripts/preencher_env_critico_multi.py.bak.20251103_135027" &&
DELETED_FILES=$((DELETED_FILES + 1))
34:rm -f scripts/preencher_env_critico_multi_csv.py.bak.20251103_135027 && echo -e "${GREEN}✅${NC} scripts/preencher_env_critico_multi_csv.py.bak.20251103_135027" && DELETED_FILES=$((DELETED_FILES +
1)) 35:rm -f scripts/auto_create_admin.sh.bak.20251103_135027 && echo -e
"${GREEN}✅${NC} scripts/auto_create_admin.sh.bak.20251103_135027" &&
DELETED_FILES=$((DELETED_FILES + 1))
38:rm -f scripts/utils/update_translations.py.v1.bak && echo -e "${GREEN}✅${NC} scripts/utils/update_translations.py.v1.bak" && DELETED_FILES=$((DELETED_FILES +
1)) 39:rm -f scripts/migrate_pydantic_v1_to_v2.py.v1.bak && echo -e "${GREEN}✅${NC}
scripts/migrate_pydantic_v1_to_v2.py.v1.bak" &&
DELETED_FILES=$((DELETED_FILES + 1))
40:rm -f scripts/archive/upgrade_pydantic_v2_smart.py.v1.bak && echo -e "${GREEN}✅${NC} scripts/archive/upgrade_pydantic_v2_smart.py.v1.bak" && DELETED_FILES=$((DELETED_FILES +
1)) 43:rm -f backend/modules/payment/models.py.bak && echo -e "${GREEN}✅${NC}
backend/modules/payment/models.py.bak" &&
DELETED_FILES=$((DELETED_FILES + 1))
61:rm -f devops/docker-compose.yml.bak && echo -e "${GREEN}✅${NC} devops/docker-compose.yml.bak" && DELETED_FILES=$((DELETED_FILES +
1)) 64:find . -type f -name "_.bak" ! -path "_/venv/_" ! -path "_/node_modules/_" -exec
rm -f {} \; -print | while read file; do 70:find . -type f -name "_.bak._" ! -path
"_/venv/_" ! -path "_/node_modules/\*" -exec rm -f {} \; -print | while read file; do

🔗 Dependências detectadas (🟠 Nível 2) em
/home/truman/dev/sila-system/scripts/maintenance/structure-guard.sh 226: local
has_models=$([ -f "${MODULES_PATH}/${domain}/models.py" ] && echo "✓" || echo "✗")
227:            local has_routes=$([
-f "${MODULES_PATH}/${domain}/routes.py" ] && echo "✓" || echo "✗") 228: local
has_services=$([ -f "${MODULES_PATH}/${domain}/services.py" ] && echo "✓" || echo "✗")
306:        if [ -d "${MODULES_PATH}/${component}" ] && [ ! -d "${CORE_PATH}/${component}" ]; then
362:    if [ "$STRICT_MODE"
= true ] && [ $VIOLATIONS -gt 0 ]; then

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/scripts/init_project_final.ps1 102: - Linux/Mac:
\`source venv/bin/activate\`

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/core/sila_stop.sh 51:# 1. Checar se há containers
ativos 59:# 2. Derrubar a stack completa 69: log ERROR "Ocorreu um erro ao derrubar o
Docker Compose. Verifique o status."

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/core/sila.sh 15: echo "💡 Execute: cd
/opt/sila-system && ./automation/utils/listar_codigo.sh"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/core/sila_start.sh 152: log WARN "Interrupção
detectada (Ctrl+C). Tentando derrubar os containers..." 170:
[[! -f "docker-compose.yml"]] && missing_files+=("docker-compose.yml") 171:
[[! -f "backend/Dockerfile"]] && missing_files+=("backend/Dockerfile") 172:
[[! -f "backend/config/settings.py"]] && missing_files+=("backend/config/settings.py")
226: source "$env_file"
233:    export FRONTEND_TARGET=$([ "$mode" = "development" ] &&
echo "dev" || echo "runtime") 234: export DEBUG=$([ "$mode" = "development" ] && echo
"true" || echo "false") 260: log INFO "Modo DEV. Iniciando build do frontend (usando o
script auxiliar)..." 264: log WARN "Script automation/maintenance/build_frontend.sh não
encontrado. Pulando build do frontend." 303: log INFO "Aguardando o serviço...
(Tentativa em ${elapsed}/${max_seconds}s)" 319: log FATAL "Falha crítica: O backend não
iniciou corretamente. Verifique os logs." 336: log WARN "Métricas indisponíveis.
Verifique o endpoint." 368: log WARN "Sistema rodando em background. Use 'docker compose
logs -f' para ver logs." 410: find automation/ -type f -name "\*.sh" -exec chmod +x {}
\; 2>/dev/null || log WARN "Não foi possível aplicar permissões. Ignorando."

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/core/start_sila.sh 19:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"
42:        if [[ -f ".env.development" ]] && [[ ! -f ".env.production" ]]; then
60:    [[ -f ".env" ]] && cp ".env" "$backup_dir/"
61: [[-f "docker-compose.yml"]] && cp "docker-compose.yml" "$backup_dir/"
97:DEBUG=$([
"$mode" = "development" ] && echo "true" || echo "false") 98:LOG_LEVEL=$([ "$mode" =
"development" ] && echo "DEBUG" || echo "INFO") 101:FRONTEND_TARGET=$([ "$mode" =
"development" ] && echo "dev" || echo "runtime") 108: export FRONTEND_TARGET=$([ "$mode"
= "development" ] && echo "dev" || echo "runtime") 109: export DEBUG=$([ "$mode" =
"development" ] && echo "true" || echo "false") 120: echo -e
"${RED}❌ Docker não encontrado. Instale o Docker primeiro.${NC}" 125: if ! command -v
docker-compose &> /dev/null && ! docker compose version &> /dev/null; then 126: echo -e
"${RED}❌ Docker Compose não encontrado. Instale o Docker Compose primeiro.${NC}" 199:
echo -e "${YELLOW}💡 Sistema rodando em background. Use 'make logs' para ver logs.${NC}"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/core/status_sila.sh 59:║ 🔍 SILA System - Status &
Healthcheck ║ 64:# 1. Listar o status dos containers 71:# 2. Executar Healthcheck do
Backend 76: log ERROR "Curl não está instalado. Não é possível executar healthcheck
HTTP." 86: log ERROR "BACKEND HEALTHCHECK: Falha no Status ($HEALTHCHECK_STATUS).
Verifique logs do backend." 100:# 3. Status de Portas (apenas informativo) 126: log WARN
"Netcat (nc) não está instalado. Pulando verificação de portas."

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/core/sila_config.sh 14:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"
33:        log_error "Comando '$1' não encontrado. Por favor, instale-o antes de continuar."
42:    # 1. Criar ambiente virtual
50:    # 2. Ativar VENV e instalar dependências
51:    source "$PROJECT_ROOT/.venv/bin/activate"
71: log_warn "Diretório do Frontend
('$frontend_dir') não encontrado. Pulando instalação."
76:        log_warn "'package.json' não encontrado em '$frontend_dir'.
Pulando instalação." 81: if (cd "$frontend_dir" && npm install); then 103: # 1.
Verificar ferramentas essenciais 110: # 2. Instalar dependências 114: # 3. Normalizar
dependências (atualmente um placeholder)

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/infra/get-docker.sh 7:# for production
environments. Before running this script, make yourself familiar 19:# Docker Buildx,
Docker Compose, containerd, and runc. When using this script 21:# of these packages.
Always test upgrades in a test environment before 23:# - Isn't designed to upgrade an
existing Docker installation. When using the 35:# 1. download the script 39:# 2. verify
the script's content 43:# 3. run the script with --dry-run to verify the steps it
executes 47:# 4. run the script either as root, or using sudo to perform the
installation. 81:# installing Docker packages. This is useful when you want to add the
repository 198:# or CalVer (YY.MM) version strings. It returns 0 (success) if version A
is newer 199:# or equal than version B, or 1 (fail) otherwise. Patch releases and
pre-release 276: lsb_dist="$(. /etc/os-release && echo "$ID")" 287: if command_exists
docker && [ -e /var/run/docker.sock ]; then 312: echo " to root access on the host.
Refer to the 'Docker daemon attack surface'" 346: if [ -r /etc/debian_version ] && [
"$lsb_dist" != "ubuntu" ] && [ "$lsb_dist" != "raspbian" ]; then 444: if [ -z
"$dist_version" ] && [ -r /etc/lsb-release ]; then 445:
dist_version="$(. /etc/lsb-release && echo "$DISTRIB_CODENAME")" 474: if [ -z
"$dist_version" ] && [ -r /etc/os-release ]; then 475:
dist_version="$(. /etc/os-release && echo "$VERSION_ID")" 483: if [ -z "$dist_version" ]
&& [ -r /etc/os-release ]; then 484:
dist_version="$(. /etc/os-release && echo "$VERSION_ID")"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/infra/nginx_automation.sh 18:# 1. cd
/caminho/para/sila-system 19:# 2. bash nginx_automation.sh --help # Ver opções 20:# 3.
bash nginx_automation.sh --diagnose # Verificar problemas 21:# 4. bash
nginx_automation.sh --auto # Configurar automaticamente 22:# 5. bash nginx_automation.sh
--generate # Gerar nginx.conf 37:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"
304:    # PERFORMANCE & OTIMIZAÇÃO
717:        echo "  Status: $(docker ps &>/dev/null && echo 'Rodando' || echo 'Parado')"
730:    echo "  Existe: $(test -f "$NGINX_CONFIG"
&& echo 'Sim' || echo 'Não')" 732: echo " Válida: $(validate_nginx_config &>/dev/null &&
echo 'Sim' || echo 'Não')" 813: error "Docker não está disponível. Instale o Docker e
tente novamente."

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/infra/nginx_monitor.sh
12:SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 107: echo "Próxima
verificação em 30 segundos... (Ctrl+C para parar)"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/infra/install_vsc_extensions.sh
16:SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 353: echo " 1. Reinicie o
VS Code" 354: echo " 2. As extensões serão carregadas automaticamente" 355: echo " 3.
Configure suas preferências pessoais se necessário"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/infra/monitor*sila.sh
14:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"
23:if [[ -d "$PROJECT_ROOT/infrastructure" ]] &&
[[-f "$PROJECT_ROOT/infrastructure/docker/docker-compose.yml"]]; then 36:if
[[-n "${DISPLAY:-}"]] && command -v whiptail >/dev/null 2>&1; then 124:
log_files=$(ls -1t "$LOG_DIR"/deploy*_.log 2>/dev/null | head -5 | sed 's|._/||' | nl -s
". ") 137: local log_file="$LOG_DIR/$(echo "$log_files" | sed -n "${choice}p" | cut -d'
' -f2- | sed 's/^[0-9]\*. //')" 176: echo -e "${CYAN}${BOLD}║ ${GREEN}1${NC}. Containers
Docker ativos ║${NC}"
177:    echo -e "${CYAN}${BOLD}║  ${BLUE}2${NC}. Logs por ambiente
║${NC}"
178:    echo -e "${CYAN}${BOLD}║  ${YELLOW}3${NC}. Uso de CPU/RAM/Disco
║${NC}"
179:    echo -e "${CYAN}${BOLD}║  ${MAGENTA}4${NC}. Últimos backups
║${NC}"
180:    echo -e "${CYAN}${BOLD}║  ${WHITE}5${NC}. Status do sistema
║${NC}"
181:    echo -e "${CYAN}${BOLD}║  ${RED}6${NC}. Configurações
║${NC}"
182:    echo -e "${CYAN}${BOLD}║  ${DIM}7${NC}. Sair
║${NC}"
227:        echo -e "  ${count}. $base_name"
235:    if [[ -n "$choice" ]] &&
[["$choice" =~ ^[0-9]+$]] && [[$choice -ge 1]] && [[$choice -le 5]]; then 300: echo -e
"🐳 Docker:
$(command -v docker >/dev/null 2>&1 && echo "${GREEN}Disponível${NC}" || echo "${RED}Não
disponível${NC}")"
301:    echo -e "📋 Docker Compose: $(command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1 && echo "${GREEN}Disponível${NC}" || echo "${RED}Não
disponível${NC}")"
410:                AUTO_REFRESH=$([ "$AUTO_REFRESH" = true ] && echo
false || echo true) 416: if [["$new_interval" =~ ^[0-9]+$]] && [ "$new_interval" -gt 0
]; then 429: echo -e "1. Toggle refresh automático (atual:
$AUTO_REFRESH)"
430:        echo -e "2. Alterar intervalo de refresh (atual: $MONITOR_INTERVAL)"
431:        echo -e "3. Ver informações do sistema"
432:        echo -e "4. Voltar"
439:                AUTO_REFRESH=$([
"$AUTO_REFRESH" = true ] && echo false || echo true) 445: if
[["$new_interval" =~ ^[0-9]+$]] && [ "$new_interval" -gt 0 ]; then 560:
[[-d "$PROJECT_ROOT/apps/backend"]] && SNAP_BACKEND_PRESENT=true ||
SNAP_BACKEND_PRESENT=false 561: [[-d "$PROJECT_ROOT/apps/frontend"]] &&
SNAP_FRONTEND_PRESENT=true || SNAP_FRONTEND_PRESENT=false

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/infra/nginx_diagnostic.sh
12:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"
169:    if [[ -d "frontend/webapp/dist" ]] && [[ -f "frontend/webapp/dist/index.html" ]]; then
291:    if [[ -n "$RESPONSE"
]] && echo "$RESPONSE" | grep -q "Welcome to nginx"; then

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/setup/init_live_session.sh 43:# 1. Verificar se HD
está montado 52: error "Falha ao montar HD interno. Verifique se /dev/sda2 existe."
56:# 2. Verificar se o projeto existe 64:# 3. Criar diretórios necessários 70:# 4.
Verificar Git 78: if sudo apt update -qq && sudo apt install -y git
--no-install-recommends; then 85:# 5. Verificar chaves SSH 117:# 6. Verificar e
configurar Docker 153:# 7. Verificar Docker Compose 165:# 8. Mostrar resumo 176:# 9.
Navegar para o projeto 183:echo " 1. Para fazer deploy: ./deploy_final.sh" 184:echo " 2.
Para deploy rápido: ./quick_deploy.sh" 185:echo " 3. Para deploy completo:
./deploy_master.sh"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/setup/init_database.sh 40:curl -s
http://localhost:8000/docs > /dev/null && echo "✅ Backend funcionando!" || echo "❌
Backend com problemas"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/tests/test_nginx_automation.sh
10:SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/tests/test_start_backend.sh
15:SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
50:    echo -e "${YELLOW}⚠️
Script não é executável. Ajustando...${NC}"
146:    echo -e "${RED}⚠️ Alguns testes
falharam. Verifique os erros acima.${NC}"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/tests/smoke-test.sh 94: if echo
"$raw" | jq . >/dev/null 2>&1; then
158:  if $VERBOSE && [[ -n "$body" ]]; then

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/utils/validar_dependencias_sila.sh
36:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"
69:        "DEBUG") [[ "$VERBOSE" == "true" ]] && echo -e
"${CYAN}[DEBUG]${NC} $message" ;;
74:    [[ "$NOTIFY" != "true" ]] && return 94: log
"ERROR" "Comando
'$cmd' não encontrado. Instale $package"
147:        log "WARNING" "Ambiente virtual não encontrado. Criando..."
155:    source venv/bin/activate || {
358:    if cd "$BACKEND_DIR"
&& source venv/bin/activate && python3 -c " 369: if cd
"$FRONTEND_DIR" && node -e "
383:    return "$([["$backend_ok" == "true" && "$frontend_ok" == "true"]];
echo $?)"
417:    if [[ "$backend_ok" == "true" && "$frontend_ok" == "true" ]]; then

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/utils/complete_env.sh 8:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)" 133: # Telemetry & Analytics (Optional)

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/utils/make_executable.sh 45:echo " 1.
./init_live_session.sh # Inicializar ambiente" 46:echo " 2. ./setup_docker_hd.sh #
Configurar Docker" 47:echo " 3. ./setup_git_remote.sh # Configurar Git" 48:echo " 4.
./deploy_final.sh # Fazer deploy"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/utils/prepare_environment.sh 6:# 1. Forçar
permissões de escrita em todo o projeto (APENAS PARA DESENVOLVIMENTO) 11:# 2. Limpeza
profunda e forçada 13:find . -type d -name "**pycache**" -exec rm -rf {} + 2>/dev/null
|| true 14:find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
18:# 3. Criar ambiente virtual e instalar dependências sem cache 21:source
.venv/bin/activate 27:# 4. Garantir permissões de execução no VENV 32:# 5. Instalar e
rodar pre-commit para garantir a qualidade 39:echo "🎉 Ambiente de desenvolvimento
preparado e desbloqueado. Pronto para automação."

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/deploy/package.sh 109:1. **GUIA_PARA_LEIGOS.md**
(15 min) 113:2. **README_MIGRATION.md** (10 min) 116:3. **ETAPA_5_SUMMARY.md** (10 min)
178:1. Leia GUIA_PARA_LEIGOS.md 179:2. Consulte README_MIGRATION.md 180:3. Execute com
--help: `bash scripts/onboarding.sh --help` 181:4. Pergunte ao Tech Lead 278: echo " 1.
Transportar arquivo: $PACKAGE_FILE" 279: echo " 2. Extrair: tar xzf $PACKAGE_FILE" 280:
echo " 3. Ler: cat LEIA-ME-PRIMEIRO.txt" 281: echo " 4. Setup: bash setup.sh" 282: echo
" 5. Começar: bash onboarding.sh --interactive"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/deploy/START_NGINX.sh
19:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"
35:    echo -e "${YELLOW}⚠️${NC}  Docker não encontrado. Instale em: https://www.docker.com/"
40:if [[ -d "$SCRIPT_DIR/apps/backend"
]] && [[-d "$SCRIPT_DIR/apps/frontend"]]; then

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/deploy/quick_deploy.sh
11:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"
32:if git diff --quiet && git diff --cached --quiet; then
33:    echo -e "${GREEN}✅
Nenhuma alteração detectada. Sistema já está atualizado.${NC}"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/dev/project_analyzer.sh 19:readonly
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
71:        ["Python"]="$(find
. -name "_.py" -not -path "_/node_modules/_" -not -path "_/venv/_" | wc -l)" 72:
["TypeScript/JavaScript"]="$(find . -name "_.ts" -o -name "_.tsx" -o -name "_.js" -o
-name "_.jsx" -not -path "_/node_modules/_" -not -path "_/venv/_" | wc -l)" 73: ["Config
Files"]="$(find . -name "_.yml" -o -name "_.yaml" -o -name "_.json" -o -name "_.toml"
-not -path "_/node_modules/_" -not -path "_/venv/_" | wc -l)" 74: ["Markdown"]="$(find .
-name "_.md" -not -path "_/node_modules/_" -not -path "_/venv/_" | wc -l)" 75: ["Shell
Scripts"]="$(find . -name "*.sh" -not -path "*/node_modules/*" -not -path "*/venv/*" | wc -l)"
76:        ["Docker Files"]="$(find
. -name "Dockerfile*" -o -name "docker-compose*.yml" -not -path "_/node_modules/_" -not
-path "_/venv/_" | wc -l)" 104: grep -q "wait_for_db" "backend/entrypoint.sh" && \
108: grep -q "alembic" "backend/entrypoint.sh" && \n 🔗 Dependências detectadas (🟢 Nível 3)
em /home/truman/dev/sila-system/scripts/dev/advanced_project_analyzer.sh 42: find . -name
"requirements.txt" -exec echo "📦 {}:" \; -exec cat {} \; > "$ANALYSIS_DIR/python_deps.txt"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/dev/master-index.sh 5:SCRIPT_DIR="$(cd "$(dirname
"${BASH_SOURCE[0]}")" && pwd)"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/migration/execute*auth_migration.sh 49: if [
"$ENVIRONMENT" = "production" ] && [ -f "infrastructure/docker/docker-compose.prod.yml"
]; then 52: elif [ "$ENVIRONMENT" = "staging" ] && [ -f
"infrastructure/docker/docker-compose.staging.yml" ]; then 112:# 1. Limpeza completa do
ambiente Docker 135:# 2. Iniciar e verificar PostgreSQL 184:# 3. Criar backup 226:# 3.
Criar e configurar ambiente virtual Python 229:source .venv/bin/activate 236:# 4.
Executar migração de senhas em modo de teste 241:# 5. Solicitar confirmação para
continuar 248:# 6. Executar migração de senhas em produção 253:# 7. Iniciar serviços
258:# 8. Verificar logs por erros 286: warning "Encontrados possíveis erros nos logs.
Verifique service_logs.txt" 296: error "Alguns serviços podem ter falhado ao iniciar.
Verifique services_status.txt" 301:# 9. Testar endpoint de autenticação 307: warning
"Endpoint de autenticação pode ter problemas. Verifique manualmente." 313:echo "1.
Backup do banco: $BACKUP_FILE" 314:echo "2. Log de migração: Verifique
password_migration*\*.log" 315:echo "3. Estatísticas: password_migration_stats.json"
316:echo "4. Logs dos serviços: service_logs.txt"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/migration/prepare_migration.sh 30: # 1. Criar
diretório de backups 33: # 2. Verificar/criar diretório de logs 36: # 3. Instalar
dependências Python necessárias 38: source .venv/bin/activate 2>/dev/null || python3 -m
venv .venv && source .venv/bin/activate 42: # 4. Verificar conexão com banco 73: # 5.
Verificar variáveis de ambiente críticas 83: source .env 2>/dev/null || true

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/migration/monitor-migration.sh 17:# CORES & ESTILOS
159: if [ -d "${MODULES_PATH}/monitoring" ] && [ -d "${CORE_PATH}/monitoring" ]; then
164: if [ -d "${MODULES_PATH}/auth" ] && [ -d "${CORE_PATH}/auth" ]; then 169: if [ -d
"${MODULES_PATH}/common" ] && [ -d "${CORE_PATH}/utils/common" ]; then 282: echo -e "
Todos os checks passaram. Sistema pronto para produção." 307: echo -e "
${BLUE}Próxima verificação em 30 segundos... (Ctrl+C para parar)${RESET}" 329: [ -d
"${CORE_PATH}" ] && echo " ✓ core/ encontrado" || echo " ✗ core/ não encontrado" 330: [
-d "${MODULES_PATH}" ] && echo " ✓ modules/ encontrado" || echo " ✗ modules/ não
encontrado"

🔗 Dependências detectadas (🔴 Nível 1) em
/home/truman/dev/sila-system/scripts/migration/onboarding.sh 52: echo "║ 🚀 SILA
System - Onboarding & Migração ║" 128: echo "ONBOARDING & MIGRAÇÃO - RELATÓRIO COMPLETO"
132: echo "Modo: $([ "$DRY_RUN" = true ] && echo "DRY-RUN" || echo "REAL")" 344: echo
"Status: $([ "$DRY_RUN" = true ] && echo "DRY-RUN (SEM MODIFICAÇÕES)" || echo "MIGRAÇÃO
EXECUTADA")" 348: echo " 1. Revisar relatório: $REPORT_FILE" 349: echo " 2. Fazer code
review" 350: echo " 3. Merge para main" 351: echo " 4. Deploy staging"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/tests/run-tests-simple.ps1 34: &
$activateScript 46: & $backendScript

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/tests/test-simple.ps1 10: # 1. Check Python
18: # 2. Check virtual environment 26: # 3. Run a simple Python command

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/tests/run-tests-direct.ps1 10:.
"venv\Scripts\Activate.ps1"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/tests/test.ps1 149:1. Criar ambiente
virtual: `python -m venv venv` 150:2. Ativar ambiente: 152: - Linux/Mac:
`source venv/bin/activate` 153:3. Instalar dependências:
`pip install -r requirements.txt`

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/tests/run-tests.ps1 4:# ─── Encoding &
Error Preferences ───────────────────────────────────────────── 20: # 1. Validate
environment paths 29: # 2. Activate virtual environment 36: . $activateScript 38: # 3.
Switch to backend directory 43: # 4. Execute backend tests 45: &
$config.BackendTestScript

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/deploy/down.ps1 5:Modo de execução: 'dev'
ou 'prod'. Default: dev 15: $null = & docker compose version 2>$null 32: & $composeCmd
down

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/deploy/start-project.ps1 51: # 1.
Environment Setup 75: # 2. Database Initialization 79: &
$dbInitScript
87:    # 3. Backend Startup
94:            & $venvActivate
121:                    Write-Log "⏳ Waiting for backend to start... (Attempt $i/$maxRetries)"
-Level "WARN" 134: # 4. Frontend Startup

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/deploy/dev-up.ps1 6:Modo de execução: 'dev'
(hot-reload) ou 'prod' (build + nginx). Default: dev 17:
$null = & docker compose version 2>$null 31:
$output = & $BaseCmd @Args *>&1
35:        throw "Falha ao executar '$($BaseCmd -join ' ') $($Args
-join ' ')'. Verifique os logs." 40:
$out = & docker ps -a --format "{{.Names}}	{{.Image}}	{{.Status}}	{{.Ports}}" 2>$null 46:
$out = & docker ps -q 2>$null 58: $out = & $ComposeCmd @args 2>$null 143: Write-Log "⚠️
npm audit encontrou problemas. Veja: $logDir
pm-audit-$timestamp.log" "Yellow" 155:
Write-Log "⚠️ pip-audit encontrou problemas. Veja: $logDir\pip-audit-$timestamp.log"
"Yellow"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/deploy/start_backend.ps1 104:$command = "cd
/home/truman/dev/sila-system && $envString bash start_backend.sh"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/dev/setup_project.ps1 36:- `backend/` -
Backend source code 39:- `frontend/` - Frontend source code 55:1. Clone the repository
56:2. Set up the backend: 63:3. Set up the frontend: 70:1. Start the backend: 75:2.
Start the frontend:

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/dev/setup_env.ps1 159:Write-Host "1. Create
a virtual environment: python -m venv venv" 160:Write-Host "2. Activate the virtual
environment: .env\Scripts\Activate" 161:Write-Host "3. Install dependencies: pip install
-r requirements.txt" 162:Write-Host "4. Create a .env file with your configuration"
163:Write-Host "5. Start the development server: uvicorn main:app --reload"

🔗 Dependências detectadas (🟢 Nível 3) em
/home/truman/dev/sila-system/scripts/windows/dev/init_project.ps1 94:1. Create a virtual
environment: 100:2. Install dependencies: 105:3. Set up environment variables in `.env`
file 107:4. Run migrations: 112:5. Start the server: 208:1. Set up the backend: 216:2.
Set up the frontend: 224:1. Start the backend: 230:2. Start the frontend:
