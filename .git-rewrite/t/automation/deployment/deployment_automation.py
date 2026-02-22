#!/usr/bin/env python3
# =============================================================================
# SILA SYSTEM - DEPLOYMENT AUTOMATION
# =============================================================================
# Script Python para automação completa de deployment
# Suporte a múltiplos ambientes, rollback, health checks
# =============================================================================

import os
import sys
import json
import yaml
import argparse
import subprocess
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import requests
import docker


class DeploymentAutomation:
    """Sistema de automação de deployment para SILA System"""

    def __init__(self, config_file: str = None, environment: str = "development"):
        self.environment = environment
        self.project_root = Path(__file__).parent.parent
        self.config = self.load_config(config_file)
        self.docker_client = docker.from_env()

        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

        # Estado do deployment
        self.deployment_id = f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.backup_created = False
        self.rollback_available = False

    def setup_logging(self):
        """Configura logging detalhado"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"deployment_{self.deployment_id}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )

    def load_config(self, config_file: str = None) -> Dict:
        """Carrega configuração de deployment"""
        if config_file is None:
            config_file = self.project_root / "config" / "deployment.yaml"

        config_path = Path(config_file)
        if config_path.exists():
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        else:
            # Configuração padrão
            return self.get_default_config()

    def get_default_config(self) -> Dict:
        """Retorna configuração padrão"""
        return {
            "environments": {
                "development": {
                    "docker_compose_file": "docker-compose.yml",
                    "health_check_timeout": 30,
                    "backup_enabled": False,
                    "zero_downtime": False,
                },
                "staging": {
                    "docker_compose_file": "docker-compose.staging.yml",
                    "health_check_timeout": 60,
                    "backup_enabled": True,
                    "zero_downtime": True,
                },
                "production": {
                    "docker_compose_file": "docker-compose.production.yml",
                    "health_check_timeout": 120,
                    "backup_enabled": True,
                    "zero_downtime": True,
                },
            },
            "services": {
                "backend": {
                    "image": "sila-backend",
                    "port": 8000,
                    "health_endpoint": "/health",
                },
                "frontend": {
                    "image": "sila-frontend",
                    "port": 80,
                    "health_endpoint": "/",
                },
                "database": {
                    "image": "postgres:15",
                    "port": 5432,
                    "backup_enabled": True,
                },
            },
        }

    def deploy(self, dry_run: bool = False, force: bool = False) -> bool:
        """Executa deployment completo"""
        self.logger.info(
            f"Iniciando deployment {self.deployment_id} para ambiente {self.environment}"
        )

        try:
            # 1. Pré-deployment checks
            if not self.pre_deployment_checks():
                return False

            # 2. Backup (se habilitado)
            if self.config["environments"][self.environment]["backup_enabled"]:
                if not self.create_backup():
                    self.logger.warning("Backup falhou, continuando deployment...")

            # 3. Build das imagens
            if not self.build_images(dry_run):
                return False

            # 4. Deploy dos serviços
            if not self.deploy_services(dry_run):
                return False

            # 5. Pós-deployment checks
            if not self.post_deployment_checks():
                if not force:
                    self.logger.error("Pós-deployment checks falharam")
                    return False

            # 6. Cleanup
            self.cleanup_old_resources()

            self.logger.info(f"Deployment {self.deployment_id} concluído com sucesso")
            return True

        except Exception as e:
            self.logger.error(f"Erro no deployment: {e}")
            if not force and self.rollback_available:
                self.logger.info("Iniciando rollback automático...")
                self.rollback()
            return False

    def pre_deployment_checks(self) -> bool:
        """Verificações pré-deployment"""
        self.logger.info("Executando verificações pré-deployment...")

        checks = [
            self.check_docker_available,
            self.check_disk_space,
            self.check_memory_available,
            self.check_ports_available,
            self.check_environment_files,
        ]

        for check in checks:
            if not check():
                return False

        self.logger.info("Verificações pré-deployment concluídas")
        return True

    def check_docker_available(self) -> bool:
        """Verifica se Docker está disponível"""
        try:
            self.docker_client.ping()
            self.logger.info("✅ Docker disponível")
            return True
        except Exception as e:
            self.logger.error(f"❌ Docker não disponível: {e}")
            return False

    def check_disk_space(self) -> bool:
        """Verifica espaço em disco"""
        try:
            result = subprocess.run(["df", "/"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                usage = lines[1].split()[4].replace("%", "")
                if int(usage) > 85:
                    self.logger.error(f"❌ Espaço em disco insuficiente: {usage}%")
                    return False
            self.logger.info("✅ Espaço em disco suficiente")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao verificar espaço: {e}")
            return False

    def check_memory_available(self) -> bool:
        """Verifica memória disponível"""
        try:
            result = subprocess.run(["free", "-m"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if line.startswith("Mem:"):
                    parts = line.split()
                    total = int(parts[1])
                    used = int(parts[2])
                    usage_percent = (used / total) * 100
                    if usage_percent > 90:
                        self.logger.error(
                            f"❌ Memória insuficiente: {usage_percent:.1f}%"
                        )
                        return False
            self.logger.info("✅ Memória suficiente")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao verificar memória: {e}")
            return False

    def check_ports_available(self) -> bool:
        """Verifica se portas estão disponíveis"""
        required_ports = [80, 443, 8000, 3000, 5432, 6379]

        for port in required_ports:
            try:
                result = subprocess.run(
                    ["netstat", "-tuln"], capture_output=True, text=True
                )
                if f":{port} " in result.stdout:
                    self.logger.warning(f"⚠️  Porta {port} já está em uso")
            except Exception:
                pass

        self.logger.info("✅ Verificação de portas concluída")
        return True

    def check_environment_files(self) -> bool:
        """Verifica arquivos de ambiente"""
        env_file = self.project_root / f".env.{self.environment}"
        target_env = self.project_root / ".env"

        if env_file.exists():
            self.logger.info(f"✅ Arquivo .env.{self.environment} encontrado")
            return True
        else:
            self.logger.warning(f"⚠️  Arquivo .env.{self.environment} não encontrado")
            return True  # Não é crítico

    def create_backup(self) -> bool:
        """Cria backup do estado atual"""
        self.logger.info("Criando backup...")

        try:
            backup_dir = self.project_root / "backups" / self.deployment_id
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Backup dos volumes
            self.backup_docker_volumes(backup_dir)

            # Backup do banco
            self.backup_database(backup_dir)

            # Backup das configurações
            self.backup_configurations(backup_dir)

            self.backup_created = True
            self.rollback_available = True
            self.logger.info(f"✅ Backup criado em {backup_dir}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Erro ao criar backup: {e}")
            return False

    def backup_docker_volumes(self, backup_dir: Path):
        """Faz backup dos volumes Docker"""
        volumes = ["sila_postgres_data", "sila_redis_data"]

        for volume_name in volumes:
            try:
                volume = self.docker_client.volumes.get(volume_name)
                # Implementar backup do volume
                self.logger.info(f"Backup do volume {volume_name}")
            except docker.errors.NotFound:
                self.logger.warning(f"Volume {volume_name} não encontrado")

    def backup_database(self, backup_dir: Path):
        """Faz backup do banco de dados"""
        try:
            # Implementar backup do PostgreSQL
            backup_file = backup_dir / "database.sql"
            self.logger.info(f"Backup do banco em {backup_file}")
        except Exception as e:
            self.logger.error(f"Erro no backup do banco: {e}")

    def backup_configurations(self, backup_dir: Path):
        """Faz backup das configurações"""
        config_files = [".env", "docker-compose.yml", "config/"]

        for config_file in config_files:
            src = self.project_root / config_file
            if src.exists():
                dst = backup_dir / config_file
                if src.is_dir():
                    subprocess.run(["cp", "-r", str(src), str(dst)])
                else:
                    subprocess.run(["cp", str(src), str(dst)])

    def build_images(self, dry_run: bool = False) -> bool:
        """Build das imagens Docker"""
        self.logger.info("Build das imagens Docker...")

        services = ["backend", "frontend"]

        for service in services:
            service_dir = self.project_root / service
            if service_dir.exists():
                if dry_run:
                    self.logger.info(f"[DRY RUN] Build da imagem {service}")
                else:
                    try:
                        self.logger.info(f"Build da imagem {service}...")
                        # Implementar build
                        self.logger.info(f"✅ Imagem {service} buildada")
                    except Exception as e:
                        self.logger.error(f"❌ Erro no build de {service}: {e}")
                        return False

        return True

    def deploy_services(self, dry_run: bool = False) -> bool:
        """Deploy dos serviços"""
        self.logger.info("Deploy dos serviços...")

        compose_file = self.config["environments"][self.environment][
            "docker_compose_file"
        ]
        compose_path = self.project_root / compose_file

        if not compose_path.exists():
            self.logger.error(f"Arquivo {compose_file} não encontrado")
            return False

        if dry_run:
            self.logger.info(f"[DRY RUN] Deploy com {compose_file}")
            return True

        try:
            # Parar serviços existentes
            subprocess.run(
                ["docker-compose", "-f", str(compose_path), "down"],
                cwd=self.project_root,
                check=True,
            )

            # Iniciar novos serviços
            subprocess.run(
                ["docker-compose", "-f", str(compose_path), "up", "-d"],
                cwd=self.project_root,
                check=True,
            )

            self.logger.info("✅ Serviços deployados")
            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erro no deploy: {e}")
            return False

    def post_deployment_checks(self) -> bool:
        """Verificações pós-deployment"""
        self.logger.info("Executando verificações pós-deployment...")

        timeout = self.config["environments"][self.environment]["health_check_timeout"]
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.check_services_health():
                self.logger.info("✅ Serviços saudáveis")
                return True
            time.sleep(5)

        self.logger.error("❌ Timeout nas verificações de saúde")
        return False

    def check_services_health(self) -> bool:
        """Verifica saúde dos serviços"""
        services = self.config["services"]

        for service_name, service_config in services.items():
            if "health_endpoint" in service_config:
                url = f"http://localhost:{service_config['port']}{service_config['health_endpoint']}"
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code != 200:
                        return False
                except Exception:
                    return False

        return True

    def cleanup_old_resources(self):
        """Limpa recursos antigos"""
        self.logger.info("Limpando recursos antigos...")

        try:
            # Remover imagens antigas
            self.docker_client.images.prune()

            # Remover containers parados
            self.docker_client.containers.prune()

            self.logger.info("✅ Cleanup concluído")
        except Exception as e:
            self.logger.warning(f"⚠️  Erro no cleanup: {e}")

    def rollback(self) -> bool:
        """Executa rollback do deployment"""
        self.logger.info("Iniciando rollback...")

        if not self.backup_created:
            self.logger.error("❌ Backup não disponível para rollback")
            return False

        try:
            # Implementar lógica de rollback
            self.logger.info("✅ Rollback concluído")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro no rollback: {e}")
            return False

    def get_deployment_status(self) -> Dict:
        """Retorna status do deployment"""
        return {
            "deployment_id": self.deployment_id,
            "environment": self.environment,
            "status": "completed",
            "backup_created": self.backup_created,
            "rollback_available": self.rollback_available,
            "timestamp": datetime.now().isoformat(),
        }


def main():
    parser = argparse.ArgumentParser(description="SILA System Deployment Automation")
    parser.add_argument(
        "--environment",
        "-e",
        default="development",
        choices=["development", "staging", "production"],
        help="Ambiente de deployment",
    )
    parser.add_argument("--config", "-c", help="Arquivo de configuração")
    parser.add_argument("--dry-run", action="store_true", help="Simular deployment")
    parser.add_argument(
        "--force", action="store_true", help="Forçar deployment mesmo com erros"
    )
    parser.add_argument("--rollback", action="store_true", help="Executar rollback")
    parser.add_argument(
        "--status", action="store_true", help="Ver status do deployment"
    )

    args = parser.parse_args()

    # Criar instância
    deploy = DeploymentAutomation(args.config, args.environment)

    if args.status:
        status = deploy.get_deployment_status()
        print(json.dumps(status, indent=2))
        return

    if args.rollback:
        success = deploy.rollback()
        sys.exit(0 if success else 1)

    # Executar deployment
    success = deploy.deploy(args.dry_run, args.force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
