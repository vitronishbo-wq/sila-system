#!/usr/bin/env python3
"""
🚀 Script de Execução do Health Check de Módulos

Este script executa o sistema de verificação de saúde de módulos
do SILA System de forma standalone, com configurações flexíveis
e relatórios detalhados.

Uso:
    python scripts/run_health_check.py [opções]

Opções:
    --url URL          URL base da API (padrão: http://127.0.0.1:8000)
    --timeout SECONDS  Timeout para requisições (padrão: 10.0)
    --username USER    Usuário para autenticação (padrão: admin)
    --password PASS    Senha para autenticação (padrão: test_password_123)
    --output FILE      Arquivo de saída do relatório (padrão: health_report.txt)
    --format FORMAT    Formato do relatório (txt, json, html)
    --modules LIST     Lista de módulos para testar (separados por vírgula)
    --verbose          Modo verboso com mais detalhes
    --help             Mostra esta ajuda
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Adiciona o diretório backend ao path
script_dir = Path(__file__).parent
backend_dir = script_dir.parent
sys.path.insert(0, str(backend_dir))

try:
    from tests.module_health_check import ModuleHealthChecker, ModuleHealthResult
except ImportError as e:
    print(f"❌ Erro ao importar módulos de teste: {e}")
    print("Certifique-se de estar executando o script do diretório correto.")
    sys.exit(1)


class HealthCheckRunner:
    """Executor do health check com configurações avançadas."""

    def __init__(self, config: dict):
        self.config = config
        self.checker = ModuleHealthChecker(base_url=config["url"], timeout=config["timeout"])

        # Configura credenciais se fornecidas
        if settings.get("username") and settings.get("password"):
            settings.TEST_USERNAME = config["username"]
            settings.TEST_PASSWORD = config["password"]

    async def run(self) -> dict[str, ModuleHealthResult]:
        """Executa o health check completo."""
        print("🛡️ SILA SYSTEM - Health Check de Módulos")
        print("=" * 50)
        print(f"📡 URL Base: {self.config['url']}")
        print(f"⏱️  Timeout: {self.config['timeout']}s")
        print(f"👤 Usuário: {self.settings.get('username', 'admin')}")
        print(f"📊 Módulos: {len(self.checker.critical_modules)}")
        print("=" * 50)

        # Executa verificação
        results = await self.checker.run_health_check()

        # Filtra módulos se especificado
        if self.settings.get("modules"):
            filtered_results = {}
            for module in self.config["modules"]:
                if module in results:
                    filtered_results[module] = results[module]
            results = filtered_results

        return results

    async def close(self):
        """Fecha o verificador."""
        await self.checker.close()

    def save_report(self, results: dict[str, ModuleHealthResult], format_type: str = "txt"):
        """Salva relatório no formato especificado."""
        output_file = self.settings.get("output", "health_report.txt")

        if format_type == "json":
            self._save_json_report(results, output_file)
        elif format_type == "html":
            self._save_html_report(results, output_file)
        else:
            self._save_text_report(results, output_file)

        return output_file

    def _save_text_report(self, results: dict[str, ModuleHealthResult], filename: str):
        """Salva relatório em formato texto."""
        report = self.checker.generate_report(results)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

    def _save_json_report(self, results: dict[str, ModuleHealthResult], filename: str):
        """Salva relatório em formato JSON."""
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "base_url": self.config["url"],
                "timeout": self.config["timeout"],
                "username": self.settings.get("username", "admin"),
            },
            "summary": {
                "total_modules": len(results),
                "healthy_modules": sum(1 for r in results.values() if r.is_healthy),
                "health_percentage": (
                    sum(1 for r in results.values() if r.is_healthy) / len(results)
                )
                * 100,
            },
            "modules": {},
        }

        for module_name, result in results.items():
            json_data["modules"][module_name] = {
                "is_healthy": result.is_healthy,
                "status_code": result.status_code,
                "response_time": result.response_time,
                "error_message": result.error_message,
                "endpoint_tested": result.endpoint_tested,
                "integration_status": result.integration_status,
            }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

    def _save_html_report(self, results: dict[str, ModuleHealthResult], filename: str):
        """Salva relatório em formato HTML."""
        healthy_count = sum(1 for r in results.values() if r.is_healthy)
        total_count = len(results)
        health_percentage = (healthy_count / total_count) * 100 if total_count > 0 else 0

        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Saúde - SILA System</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .summary {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .metric {{ text-align: center; padding: 15px; border-radius: 5px; }}
        .metric.healthy {{ background: #d4edda; color: #155724; }}
        .metric.unhealthy {{ background: #f8d7da; color: #721c24; }}
        .module {{ margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid; }}
        .module.healthy {{ background: #f8f9fa; border-left-color: #28a745; }}
        .module.unhealthy {{ background: #fff5f5; border-left-color: #dc3545; }}
        .module-header {{ font-weight: bold; font-size: 1.1em; }}
        .module-details {{ margin-top: 10px; font-size: 0.9em; color: #666; }}
        .timestamp {{ text-align: center; color: #666; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Relatório de Saúde dos Módulos</h1>
            <h2>SILA System</h2>
        </div>

        <div class="summary">
            <div class="metric {"healthy" if health_percentage >= 80 else "unhealthy"}">
                <h3>{health_percentage:.1f}%</h3>
                <p>Saúde Geral</p>
            </div>
            <div class="metric">
                <h3>{healthy_count}/{total_count}</h3>
                <p>Módulos Saudáveis</p>
            </div>
            <div class="metric">
                <h3>{self.config["url"]}</h3>
                <p>Base URL</p>
            </div>
        </div>

        <h3>📋 Detalhes por Módulo</h3>
"""

        for module_name, result in results.items():
            status_class = "healthy" if result.is_healthy else "unhealthy"
            status_icon = "✅" if result.is_healthy else "❌"
            status_text = "SAUDÁVEL" if result.is_healthy else "PROBLEMA"

            html += f"""
        <div class="module {status_class}">
            <div class="module-header">{status_icon} {module_name.upper()}: {status_text}</div>
            <div class="module-details">
                <strong>Status:</strong> {result.status_code or "N/A"} |
                <strong>Tempo:</strong> {result.response_time:.2f}s |
                <strong>Endpoint:</strong> {result.endpoint_tested or "N/A"}
"""

            if result.error_message:
                html += f"<br><strong>Erro:</strong> {result.error_message}"

            if result.integration_status:
                html += "<br><strong>Integrações:</strong> "
                for integration, status in result.integration_status.items():
                    int_icon = "✅" if status else "❌"
                    html += f"{int_icon} {integration} "

            html += "</div></div>"

        html += f"""
        <div class="timestamp">
            Relatório gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        </div>
    </div>
</body>
</html>
"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)


def parse_arguments():
    """Parse dos argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="Executa health check de módulos do SILA System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000",
        help="URL base da API (padrão: http://127.0.0.1:8000)",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Timeout para requisições em segundos (padrão: 10.0)",
    )

    parser.add_argument(
        "--username", default="admin", help="Usuário para autenticação (padrão: admin)"
    )

    parser.add_argument(
        "--password",
        default="test_password_123",
        help="Senha para autenticação (padrão: test_password_123)",
    )

    parser.add_argument(
        "--output",
        default="health_report.txt",
        help="Arquivo de saída do relatório (padrão: health_report.txt)",
    )

    parser.add_argument(
        "--format",
        choices=["txt", "json", "html"],
        default="txt",
        help="Formato do relatório (padrão: txt)",
    )

    parser.add_argument("--modules", help="Lista de módulos para testar (separados por vírgula)")

    parser.add_argument("--verbose", action="store_true", help="Modo verboso com mais detalhes")

    return parser.parse_args()


async def main():
    """Função principal."""
    args = parse_arguments()

    # Configuração
    config = {
        "url": args.url,
        "timeout": args.timeout,
        "username": args.username,
        "password": args.password,
        "output": args.output,
        "format": args.format,
        "modules": args.modules.split(",") if args.modules else None,
        "verbose": args.verbose,
    }

    runner = HealthCheckRunner(config)

    try:
        # Executa health check
        results = await runner.run()

        # Gera relatório
        output_file = runner.save_report(results, config["format"])

        # Estatísticas finais
        healthy_count = sum(1 for r in results.values() if r.is_healthy)
        total_count = len(results)
        health_percentage = (healthy_count / total_count) * 100 if total_count > 0 else 0

        print("\n" + "=" * 50)
        print("📊 RESULTADOS FINAIS:")
        print(f"   • Módulos saudáveis: {healthy_count}/{total_count} ({health_percentage:.1f}%)")
        print(f"   • Relatório salvo: {output_file}")

        if health_percentage >= 80:
            print("   • ✅ Sistema com boa saúde!")
        else:
            print("   • ⚠️ Sistema com problemas - verificar módulos com falha")

        print("=" * 50)

        # Exit code baseado na saúde do sistema
        if health_percentage < 80:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⏹️ Execução interrompida pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        if config["verbose"]:
            import traceback

            traceback.print_exc()
        sys.exit(1)
    finally:
        await runner.close()


if __name__ == "__main__":
    asyncio.run(main())
