#!/usr/bin/env python3
"""
🔧 Script de Configuração do Health Check

Este script ajuda a configurar o sistema de health check para diferentes
ambientes (desenvolvimento, teste, produção) e valida as configurações.
"""

import argparse
import sys
from pathlib import Path
from typing import Any


class HealthCheckSetup:
    """Configurador do sistema de health check."""

    def __init__(self):
        self.backend_dir = Path(__file__).parent.parent
        self.env_file = self.backend_dir / ".env.health_check.local"
        self.template_file = self.backend_dir / ".env.health_check"

    def create_env_file(self, environment: str = "development") -> Path:
        """Cria arquivo de configuração para o ambiente especificado."""

        configs = {
            "development": {
                "API_BASE_URL": "http://localhost:8000",
                "TEST_USERNAME": "admin",
                "TEST_PASSWORD": "test_password_123",
                "VERBOSE_MODE": "true",
                "DEV_MODE": "true",
                "LOG_LEVEL": "DEBUG",
            },
            "testing": {
                "API_BASE_URL": "http://localhost:8000",
                "TEST_USERNAME": "test_user",
                "TEST_PASSWORD": "test_pass",
                "VERBOSE_MODE": "true",
                "CI_MODE": "true",
                "LOG_LEVEL": "INFO",
            },
            "production": {
                "API_BASE_URL": "https://api.sila.com.br",
                "TEST_USERNAME": "monitor_user",
                "TEST_PASSWORD": "secure_password",
                "VERBOSE_MODE": "false",
                "MIN_HEALTH_THRESHOLD": "95",
                "LOG_LEVEL": "WARNING",
            },
        }

        if environment not in configs:
            raise ValueError(f"Ambiente inválido: {environment}. Use: {list(configs.keys())}")

        # Lê template base
        template_content = ""
        if self.template_file.exists():
            template_content = self.template_file.read_text(encoding="utf-8")

        # Substitui valores específicos do ambiente
        env_config = configs[environment]
        for key, value in env_config.items():
            template_content = self._replace_config_value(template_content, key, value)

        # Salva arquivo de configuração
        self.env_file.write_text(template_content, encoding="utf-8")

        print(f"✅ Arquivo de configuração criado: {self.env_file}")
        print(f"🔧 Ambiente: {environment}")

        return self.env_file

    def _replace_config_value(self, content: str, key: str, value: str) -> str:
        """Substitui valor de configuração no template."""
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if line.strip().startswith(f"{key}=") and not line.strip().startswith("#"):
                lines[i] = f"{key}={value}"
                break
        else:
            # Se não encontrou a linha, adiciona no final
            lines.append(f"{key}={value}")

        return "\n".join(lines)

    def validate_config(self) -> dict[str, Any]:
        """Valida configurações do health check."""
        print("🔍 Validando configurações...")

        if not self.env_file.exists():
            print("⚠️ Arquivo de configuração não encontrado. Execute setup primeiro.")
            return {
                "valid": False,
                "errors": ["Arquivo de configuração não encontrado"],
            }

        # Carrega configurações
        config = self._load_env_file()

        errors = []
        warnings = []

        # Validações básicas
        if not config.get("API_BASE_URL"):
            errors.append("API_BASE_URL não definida")

        if not config.get("TEST_USERNAME"):
            errors.append("TEST_USERNAME não definida")

        if not config.get("TEST_PASSWORD"):
            errors.append("TEST_PASSWORD não definida")

        # Validações de formato
        try:
            timeout = float(config.get("TEST_TIMEOUT", "10"))
            if timeout <= 0:
                errors.append("TEST_TIMEOUT deve ser maior que 0")
        except ValueError:
            errors.append("TEST_TIMEOUT deve ser um número")

        try:
            threshold = int(config.get("MIN_HEALTH_THRESHOLD", "80"))
            if not 0 <= threshold <= 100:
                errors.append("MIN_HEALTH_THRESHOLD deve estar entre 0 e 100")
        except ValueError:
            errors.append("MIN_HEALTH_THRESHOLD deve ser um número inteiro")

        # Avisos
        if config.get("TEST_PASSWORD") == "test_password_123":
            warnings.append("Senha padrão em uso - considere alterar em produção")

        if config.get("DEV_MODE") == "true" and config.get("SKIP_AUTH") == "true":
            warnings.append("Modo de desenvolvimento com autenticação desabilitada")

        result = {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "config": config,
        }

        # Exibe resultados
        if errors:
            print("❌ Erros encontrados:")
            for error in errors:
                print(f"   • {error}")

        if warnings:
            print("⚠️ Avisos:")
            for warning in warnings:
                print(f"   • {warning}")

        if result["valid"]:
            print("✅ Configurações válidas")

        return result

    def _load_env_file(self) -> dict[str, str]:
        """Carrega arquivo .env como dicionário."""
        config = {}

        if self.env_file.exists():
            with open(self.env_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()

        return config

    def test_connection(self) -> bool:
        """Testa conexão com o servidor configurado."""
        import httpx

        config = self._load_env_file()
        base_url = config.get("API_BASE_URL", "http://localhost:8000")

        print(f"🌐 Testando conexão com {base_url}...")

        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{base_url}/docs")

                if response.status_code == 200:
                    print("✅ Servidor está respondendo")
                    return True
                else:
                    print(f"⚠️ Servidor respondeu com status {response.status_code}")
                    return False

        except httpx.ConnectError:
            print("❌ Não foi possível conectar ao servidor")
            print("💡 Verifique se o servidor SILA está rodando")
            return False
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False

    def install_dependencies(self) -> bool:
        """Instala dependências necessárias."""
        import subprocess

        print("📦 Instalando dependências...")

        requirements_file = self.backend_dir / "requirements_test.txt"

        if not requirements_file.exists():
            print("❌ Arquivo requirements_test.txt não encontrado")
            return False

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("✅ Dependências instaladas com sucesso")
                return True
            else:
                print(f"❌ Erro ao instalar dependências: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Erro ao executar pip: {e}")
            return False

    def create_sample_script(self) -> Path:
        """Cria script de exemplo para execução."""
        script_content = """#!/bin/bash

# 🛡️ Script de Exemplo - Health Check SILA System
# Este script foi gerado automaticamente pelo setup

# Carrega configurações
if [ -f ".env.health_check.local" ]; then
    export $(cat .env.health_check.local | grep -v '^#' | xargs)
fi

# Executa health check
echo "🛡️ Executando Health Check do SILA System..."
python backend/scripts/run_health_check.py \\
    --url "${API_BASE_URL:-http://localhost:8000}" \\
    --timeout "${TEST_TIMEOUT:-10}" \\
    --username "${TEST_USERNAME:-admin}" \\
    --password "${TEST_PASSWORD:-test_password_123}" \\
    --format "${DEFAULT_REPORT_FORMAT:-txt}" \\
    --output "${DEFAULT_OUTPUT_FILE:-health_report.txt}"

# Verifica resultado
if [ $? -eq 0 ]; then
    echo "✅ Health check concluído com sucesso!"
else
    echo "❌ Health check falhou!"
    exit 1
fi
"""

        script_file = self.backend_dir / "run_health_check_example.sh"
        script_file.write_text(script_content)
        script_file.chmod(0o755)

        print(f"✅ Script de exemplo criado: {script_file}")

        return script_file


def main():
    """Função principal do setup."""
    parser = argparse.ArgumentParser(
        description="Configura o sistema de health check do SILA System"
    )

    parser.add_argument(
        "--environment",
        "-e",
        choices=["development", "testing", "production"],
        default="development",
        help="Ambiente para configuração (padrão: development)",
    )

    parser.add_argument(
        "--validate",
        "-v",
        action="store_true",
        help="Apenas valida configurações existentes",
    )

    parser.add_argument(
        "--test-connection", action="store_true", help="Testa conexão com o servidor"
    )

    parser.add_argument(
        "--install-deps", action="store_true", help="Instala dependências necessárias"
    )

    parser.add_argument("--create-script", action="store_true", help="Cria script de exemplo")

    parser.add_argument("--all", action="store_true", help="Executa todas as operações")

    args = parser.parse_args()

    setup = HealthCheckSetup()

    print("🔧 SILA System - Setup do Health Check")
    print("=" * 40)

    try:
        # Cria configuração se não for apenas validação
        if not args.validate or args.all:
            setup.create_env_file(args.environment)

        # Valida configurações
        validation_result = setup.validate_config()

        # Instala dependências se solicitado
        if args.install_deps or args.all:
            setup.install_dependencies()

        # Testa conexão se solicitado
        if args.test_connection or args.all:
            setup.test_connection()

        # Cria script de exemplo se solicitado
        if args.create_script or args.all:
            setup.create_sample_script()

        print("\n🎉 Setup concluído!")
        print("\n📚 Próximos passos:")
        print("   1. Ajuste as configurações em .env.health_check.local")
        print("   2. Execute: python backend/scripts/run_health_check.py")
        print("   3. Ou use o script Bash: ./backend/scripts/run_health_check.sh")

        if not validation_result["valid"]:
            print("\n⚠️ Corrija os erros de configuração antes de executar o health check")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Erro durante setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
