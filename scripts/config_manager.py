#!/usr/bin/env python3
# =============================================================================
# SILA SYSTEM - CONFIG MANAGER
# =============================================================================
# Sistema completo de gestão de configurações
# Suporte a múltiplos ambientes, templates, validação e criptografia
# =============================================================================

import os
import sys
import json
import yaml
import argparse
import secrets
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import logging
from cryptography.fernet import Fernet
from dataclasses import dataclass, asdict
import re


@dataclass
class ConfigItem:
    """Item de configuração"""

    key: str
    value: Any
    environment: str
    encrypted: bool = False
    description: str = ""
    validation_rules: Optional[Dict] = None
    last_modified: Optional[datetime] = None


class ConfigManager:
    """Gerenciador de configurações do SILA System"""

    def __init__(self, config_dir: str = None, environment: str = "development"):
        self.project_root = Path(__file__).parent.parent
        self.config_dir = (
            Path(config_dir) if config_dir else self.project_root / "config"
        )
        self.environment = environment
        self.configs: Dict[str, ConfigItem] = {}
        self.encryption_key = None

        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

        # Inicializar
        self.init_config_dir()
        self.load_encryption_key()
        self.load_all_configs()

    def setup_logging(self):
        """Configura logging"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "config_manager.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )

    def init_config_dir(self):
        """Inicializa diretório de configurações"""
        self.config_dir.mkdir(exist_ok=True)

        # Criar subdiretórios
        (self.config_dir / "environments").mkdir(exist_ok=True)
        (self.config_dir / "templates").mkdir(exist_ok=True)
        (self.config_dir / "backups").mkdir(exist_ok=True)
        (self.config_dir / "schemas").mkdir(exist_ok=True)

        # Criar arquivos padrão se não existirem
        self.create_default_configs()

    def create_default_configs(self):
        """Cria configurações padrão"""
        default_configs = {
            "development": {
                "app": {
                    "name": "SILA System",
                    "version": "2.0.0",
                    "debug": True,
                    "log_level": "DEBUG",
                },
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "sila_db_dev",
                    "user": "sila_dev",
                    "password": "dev_password",
                },
                "redis": {"host": "localhost", "port": 6379, "db": 0},
                "security": {
                    "secret_key": "dev_secret_key_change_in_production",
                    "jwt_expire_minutes": 1440,
                    "cors_origins": ["http://localhost:3000"],
                },
            },
            "staging": {
                "app": {
                    "name": "SILA System",
                    "version": "2.0.0",
                    "debug": False,
                    "log_level": "INFO",
                },
                "database": {
                    "host": "staging-db.sila.system",
                    "port": 5432,
                    "name": "sila_db_staging",
                    "user": "sila_staging",
                    "password": "encrypted_placeholder",
                },
                "redis": {"host": "staging-redis.sila.system", "port": 6379, "db": 0},
                "security": {
                    "secret_key": "encrypted_placeholder",
                    "jwt_expire_minutes": 60,
                    "cors_origins": ["https://staging.sila.system"],
                },
            },
            "production": {
                "app": {
                    "name": "SILA System",
                    "version": "2.0.0",
                    "debug": False,
                    "log_level": "WARNING",
                },
                "database": {
                    "host": "prod-db.sila.system",
                    "port": 5432,
                    "name": "sila_db",
                    "user": "sila_prod",
                    "password": "encrypted_placeholder",
                },
                "redis": {"host": "prod-redis.sila.system", "port": 6379, "db": 0},
                "security": {
                    "secret_key": "encrypted_placeholder",
                    "jwt_expire_minutes": 30,
                    "cors_origins": ["https://sila.system"],
                },
            },
        }

        for env, config in default_configs.items():
            config_file = self.config_dir / "environments" / f"{env}.yaml"
            if not config_file.exists():
                with open(config_file, "w") as f:
                    yaml.dump(config, f, default_flow_style=False)
                self.logger.info(f"Configuração padrão criada: {env}")

    def load_encryption_key(self):
        """Carrega ou cria chave de criptografia"""
        key_file = self.config_dir / ".encryption_key"

        if key_file.exists():
            with open(key_file, "rb") as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.encryption_key)
            # Proteger arquivo
            os.chmod(key_file, 0o600)
            self.logger.info("Chave de criptografia criada")

    def encrypt_value(self, value: str) -> str:
        """Criptografa um valor"""
        if not self.encryption_key:
            raise ValueError("Chave de criptografia não disponível")

        fernet = Fernet(self.encryption_key)
        encrypted = fernet.encrypt(value.encode())
        return f"ENC:{encrypted.decode()}"

    def decrypt_value(self, encrypted_value: str) -> str:
        """Descriptografa um valor"""
        if not encrypted_value.startswith("ENC:"):
            return encrypted_value

        if not self.encryption_key:
            raise ValueError("Chave de criptografia não disponível")

        fernet = Fernet(self.encryption_key)
        encrypted = encrypted_value[4:]  # Remove "ENC:"
        decrypted = fernet.decrypt(encrypted.encode())
        return decrypted.decode()

    def load_all_configs(self):
        """Carrega todas as configurações"""
        self.configs.clear()

        # Carregar configurações do ambiente atual
        env_config_file = self.config_dir / "environments" / f"{self.environment}.yaml"
        if env_config_file.exists():
            self.load_config_file(env_config_file, self.environment)

        # Carregar configurações globais
        global_config_file = self.config_dir / "global.yaml"
        if global_config_file.exists():
            self.load_config_file(global_config_file, "global")

        self.logger.info(f"Carregadas {len(self.configs)} configurações")

    def load_config_file(self, file_path: Path, environment: str):
        """Carrega configurações de um arquivo"""
        try:
            with open(file_path, "r") as f:
                config_data = yaml.safe_load(f)

            self._parse_config_dict(config_data, environment, "")

        except Exception as e:
            self.logger.error(f"Erro ao carregar {file_path}: {e}")

    def _parse_config_dict(self, config_dict: Dict, environment: str, prefix: str):
        """Parse recursivo de dicionário de configuração"""
        for key, value in config_dict.items():
            full_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                self._parse_config_dict(value, environment, full_key)
            else:
                encrypted = isinstance(value, str) and value.startswith("ENC:")

                config_item = ConfigItem(
                    key=full_key,
                    value=value,
                    environment=environment,
                    encrypted=encrypted,
                    last_modified=datetime.now(),
                )

                self.configs[full_key] = config_item

    def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor de configuração"""
        config_item = self.configs.get(key)
        if not config_item:
            return default

        if config_item.encrypted:
            return self.decrypt_value(config_item.value)

        return config_item.value

    def set(self, key: str, value: Any, encrypt: bool = False, description: str = ""):
        """Define valor de configuração"""
        if encrypt and isinstance(value, str):
            value = self.encrypt_value(value)

        config_item = ConfigItem(
            key=key,
            value=value,
            environment=self.environment,
            encrypted=encrypt,
            description=description,
            last_modified=datetime.now(),
        )

        self.configs[key] = config_item
        self.logger.info(f"Configuração definida: {key}")

    def validate_config(self, key: str, value: Any) -> bool:
        """Valida valor de configuração"""
        config_item = self.configs.get(key)
        if not config_item or not config_item.validation_rules:
            return True

        rules = config_item.validation_rules

        # Tipo
        if "type" in rules:
            expected_type = rules["type"]
            if expected_type == "string" and not isinstance(value, str):
                return False
            elif expected_type == "integer" and not isinstance(value, int):
                return False
            elif expected_type == "float" and not isinstance(value, (int, float)):
                return False
            elif expected_type == "boolean" and not isinstance(value, bool):
                return False

        # Range
        if "min" in rules and value < rules["min"]:
            return False
        if "max" in rules and value > rules["max"]:
            return False

        # Pattern (regex)
        if "pattern" in rules and isinstance(value, str):
            if not re.match(rules["pattern"], value):
                return False

        # Options
        if "options" in rules and value not in rules["options"]:
            return False

        return True

    def save_configs(self):
        """Salva configurações no ambiente atual"""
        config_dict = {}

        for key, config_item in self.configs.items():
            if config_item.environment == self.environment:
                self._set_nested_value(config_dict, key, config_item.value)

        config_file = self.config_dir / "environments" / f"{self.environment}.yaml"

        with open(config_file, "w") as f:
            yaml.dump(config_dict, f, default_flow_style=False)

        self.logger.info(f"Configurações salvas: {self.environment}")

    def _set_nested_value(self, config_dict: Dict, key: str, value: Any):
        """Define valor aninhado em dicionário"""
        keys = key.split(".")
        current = config_dict

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value

    def backup_configs(self) -> str:
        """Cria backup das configurações"""
        backup_name = f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
        backup_file = self.config_dir / "backups" / backup_name

        import tarfile

        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(self.config_dir / "environments", arcname="environments")
            tar.add(self.config_dir / "global.yaml", arcname="global.yaml")

        self.logger.info(f"Backup criado: {backup_file}")
        return str(backup_file)

    def restore_configs(self, backup_file: str):
        """Restaura configurações do backup"""
        backup_path = Path(backup_file)
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup não encontrado: {backup_file}")

        import tarfile

        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(self.config_dir)

        # Recarregar configurações
        self.load_all_configs()

        self.logger.info(f"Configurações restauradas de: {backup_file}")

    def generate_env_file(self, output_file: str = None):
        """Gera arquivo .env a partir das configurações"""
        if output_file is None:
            output_file = self.project_root / f".env.{self.environment}"

        env_lines = []

        for key, config_item in self.configs.items():
            if config_item.environment == self.environment:
                env_key = key.upper().replace(".", "_")
                value = config_item.value

                if config_item.encrypted:
                    value = self.decrypt_value(value)

                # Converter para string
                if isinstance(value, bool):
                    value = "true" if value else "false"
                elif isinstance(value, (list, dict)):
                    value = json.dumps(value)
                else:
                    value = str(value)

                env_lines.append(f"{env_key}={value}")

        with open(output_file, "w") as f:
            f.write("\n".join(env_lines))

        self.logger.info(f"Arquivo .env gerado: {output_file}")

    def list_configs(self, environment: str = None) -> List[Dict]:
        """Lista configurações"""
        configs = []

        for key, config_item in self.configs.items():
            if environment is None or config_item.environment == environment:
                config_dict = asdict(config_item)
                if config_item.last_modified:
                    config_dict["last_modified"] = config_item.last_modified.isoformat()
                configs.append(config_dict)

        return configs

    def search_configs(self, pattern: str) -> List[Dict]:
        """Busca configurações por padrão"""
        results = []
        regex = re.compile(pattern, re.IGNORECASE)

        for key, config_item in self.configs.items():
            if regex.search(key) or regex.search(config_item.description):
                config_dict = asdict(config_item)
                if config_item.last_modified:
                    config_dict["last_modified"] = config_item.last_modified.isoformat()
                results.append(config_dict)

        return results

    def encrypt_sensitive_values(self):
        """Criptografa valores sensíveis automaticamente"""
        sensitive_keys = ["password", "secret", "key", "token", "credential"]

        for key, config_item in list(self.configs.items()):
            if not config_item.encrypted:
                key_lower = key.lower()
                if any(sensitive in key_lower for sensitive in sensitive_keys):
                    if isinstance(config_item.value, str):
                        encrypted_value = self.encrypt_value(config_item.value)
                        config_item.value = encrypted_value
                        config_item.encrypted = True
                        self.logger.info(f"Valor criptografado: {key}")

    def generate_config_schema(self) -> Dict:
        """Gera schema de validação das configurações"""
        schema = {
            "version": "1.0",
            "environments": list(
                set(item.environment for item in self.configs.values())
            ),
            "properties": {},
        }

        for key, config_item in self.configs.items():
            if key not in schema["properties"]:
                schema["properties"][key] = {
                    "type": "string",
                    "description": config_item.description,
                    "encrypted": config_item.encrypted,
                    "environments": [],
                }

            schema["properties"][key]["environments"].append(config_item.environment)

        return schema

    def export_configs(
        self, format: str = "yaml", include_encrypted: bool = False
    ) -> str:
        """Exporta configurações em formato específico"""
        export_data = {}

        for key, config_item in self.configs.items():
            if config_item.environment == self.environment:
                value = config_item.value

                if config_item.encrypted and not include_encrypted:
                    value = "***ENCRYPTED***"
                elif config_item.encrypted and include_encrypted:
                    value = self.decrypt_value(value)

                self._set_nested_value(export_data, key, value)

        if format.lower() == "yaml":
            return yaml.dump(export_data, default_flow_style=False)
        elif format.lower() == "json":
            return json.dumps(export_data, indent=2)
        else:
            raise ValueError(f"Formato não suportado: {format}")


def main():
    parser = argparse.ArgumentParser(description="SILA System Config Manager")
    parser.add_argument(
        "--environment",
        "-e",
        default="development",
        choices=["development", "staging", "production"],
        help="Ambiente de configuração",
    )
    parser.add_argument("--config-dir", "-c", help="Diretório de configurações")
    parser.add_argument("--get", "-g", help="Obter valor de configuração")
    parser.add_argument(
        "--set",
        "-s",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Definir valor de configuração",
    )
    parser.add_argument("--encrypt", action="store_true", help="Criptografar valor")
    parser.add_argument(
        "--list", "-l", action="store_true", help="Listar configurações"
    )
    parser.add_argument("--search", help="Buscar configurações")
    parser.add_argument("--backup", "-b", action="store_true", help="Criar backup")
    parser.add_argument("--restore", help="Restaurar do backup")
    parser.add_argument(
        "--generate-env", action="store_true", help="Gerar arquivo .env"
    )
    parser.add_argument(
        "--export", choices=["yaml", "json"], help="Exportar configurações"
    )
    parser.add_argument(
        "--include-encrypted",
        action="store_true",
        help="Incluir valores criptografados na exportação",
    )

    args = parser.parse_args()

    # Criar gerenciador
    config_manager = ConfigManager(args.config_dir, args.environment)

    try:
        if args.get:
            value = config_manager.get(args.get)
            if value is not None:
                print(value)
            else:
                print(f"Configuração '{args.get}' não encontrada")
                sys.exit(1)

        elif args.set:
            key, value = args.set
            # Tentar converter para tipo apropriado
            try:
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                elif value.isdigit():
                    value = int(value)
                elif "." in value and value.replace(".", "").isdigit():
                    value = float(value)
            except ValueError:
                pass  # Manter como string

            config_manager.set(key, value, encrypt=args.encrypt)
            config_manager.save_configs()
            print(f"Configuração '{key}' definida")

        elif args.list:
            configs = config_manager.list_configs()
            print(json.dumps(configs, indent=2))

        elif args.search:
            results = config_manager.search_configs(args.search)
            print(json.dumps(results, indent=2))

        elif args.backup:
            backup_file = config_manager.backup_configs()
            print(f"Backup criado: {backup_file}")

        elif args.restore:
            config_manager.restore_configs(args.restore)
            print("Configurações restauradas")

        elif args.generate_env:
            config_manager.generate_env_file()
            print("Arquivo .env gerado")

        elif args.export:
            exported = config_manager.export_configs(
                args.export, args.include_encrypted
            )
            print(exported)

        else:
            print("Use --help para ver opções disponíveis")

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
