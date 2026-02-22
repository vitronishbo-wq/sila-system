from dotenv import dotenv_values
from datetime import datetime
from pathlib import Path

# 📌 Variáveis críticas institucionais
VARIAVEIS_CRITICAS = [
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "DEBUG",
    "SILA_SYSTEM_ID",
]

# 📄 Caminho do .env
env_path = Path(".env")
config = dotenv_values(env_path)

# 📋 Log institucional em Markdown
log_path = Path(f"env_validacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
with log_path.open("w", encoding="utf-8") as log:
    log.write(f"# ✅ Validação Institucional do .env\n\n")
    log.write(f"**Arquivo auditado:** `{env_path.resolve()}`\n\n")
    log.write("## Variáveis Críticas\n")

    faltantes = []
    for var in VARIAVEIS_CRITICAS:
        valor = config.get(var)
        if valor is None or valor.strip() == "":
            log.write(f"- ❌ `{var}`: **ausente ou vazio**\n")
            faltantes.append(var)
        else:
            log.write(f"- ✅ `{var}`: `{valor}`\n")

    log.write("\n## Resultado\n")
    if faltantes:
        log.write(
            f"❌ {len(faltantes)} variáveis críticas ausentes: {', '.join(faltantes)}\n"
        )
    else:
        log.write("✅ Todas as variáveis críticas estão presentes e válidas\n")

print(f"📋 Validação concluída. Log salvo em: {log_path}")
