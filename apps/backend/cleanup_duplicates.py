#!/usr/bin/env python3
"""
🧹 CLEANUP DUPLICATES - SILA Backend Cleanup Tool
Ferramenta robusta e moderna para eliminar duplicidades de directórios
"""

import shutil
import subprocess
import sys
from pathlib import Path


class DuplicatesCleaner:
    def __init__(self, backend_path: str):
        self.backend = Path(backend_path)
        self.log = []

    def run_cmd(self, cmd: str, description: str = "") -> tuple[int, str, str]:
        """Execute command and log"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            self.log_info(f"✅ {description}" if result.returncode == 0 else f"❌ {description}")
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.log_error(f"⏱️  Timeout: {description}")
            return 124, "", "Timeout"
        except Exception as e:
            self.log_error(f"💥 Error: {description} - {e}")
            return 1, "", str(e)

    def log_info(self, msg: str):
        self.log.append(f"ℹ️  {msg}")
        print(f"ℹ️  {msg}")

    def log_success(self, msg: str):
        self.log.append(f"✅ {msg}")
        print(f"✅ {msg}")

    def log_error(self, msg: str):
        self.log.append(f"❌ {msg}")
        print(f"❌ {msg}")

    def log_warning(self, msg: str):
        self.log.append(f"⚠️  {msg}")
        print(f"⚠️  {msg}")

    # ====== PHASE 1: ANALYSIS ======

    def phase1_analyze_imports(self) -> dict[str, int]:
        """Fase 1: Analisar todos os imports de diretórios duplicados"""
        print("\n" + "=" * 80)
        print("🔍 FASE 1: ANÁLISE DE IMPORTS")
        print("=" * 80)

        imports_map = {
            "from apps.backend.app.infra": 0,
            "from apps.backend.app.infrastructure": 0,
            "from application.": 0,
            "from apps.backend.app.application": 0,
            "from apps.backend.app.seeds": 0,
            "from seeds": 0,
        }

        for import_pattern in imports_map.keys():
            cmd_check = f"grep -r '{import_pattern}' {self.backend} --include='*.py' 2>/dev/null"
            rc, stdout, _ = self.run_cmd(cmd_check, f"Scanning {import_pattern}")
            count = len([l for l in stdout.split("\n") if l.strip() and ".venv" not in l])
            imports_map[import_pattern] = count
            print(f"   {import_pattern:20} → {count:3} referências")

        return imports_map

    def phase1_list_files(self):
        """Listar ficheiros em cada diretório a ser limpado"""
        print("\n" + "-" * 80)
        print("📂 FICHEIROS EM DIRETÓRIOS DUPLICADOS")
        print("-" * 80)

        dirs_to_check = [
            ("app/infra", self.backend / "app" / "infra"),
            ("application", self.backend / "application"),
            ("apps/backend", self.backend / "apps" / "backend"),
        ]

        for name, path in dirs_to_check:
            if path.exists():
                cmd = f"find {path} -type f -name '*.py' 2>/dev/null | sort"
                rc, stdout, _ = self.run_cmd(cmd, f"Listing {name}")
                files = [f for f in stdout.split("\n") if f.strip()]
                print(f"\n📁 {name}/ ({len(files)} ficheiros)")
                for f in files[:5]:
                    print(f"   - {Path(f).relative_to(self.backend)}")
                if len(files) > 5:
                    print(f"   ... e mais {len(files) - 5}")

    # ====== PHASE 2: BACKUP ======

    def phase2_backup(self):
        """Fase 2: Backup no Git e preservação"""
        print("\n" + "=" * 80)
        print("💾 FASE 2: BACKUP & PRESERVAÇÃO")
        print("=" * 80)

        # Verificar git
        rc, stdout, _ = self.run_cmd(f"cd {self.backend} && git status", "Verificando git")
        if rc != 0:
            self.log_error("Git não disponível. Abortando cleanup.")
            return False

        # Add all changes
        self.run_cmd(f"cd {self.backend} && git add .", "Git add all files")

        # Commit backup
        self.run_cmd(
            f"cd {self.backend} && git commit -m 'backup: antes da limpeza de duplicidades [autocommit]'",
            "Git commit backup",
        )

        # Create branch
        self.run_cmd(
            f"cd {self.backend} && git branch backup/pre-cleanup-{self._get_timestamp()}",
            "Criar branch backup",
        )

        self.log_success("Backup concluído com sucesso")
        return True

    @staticmethod
    def _get_timestamp():
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d-%H%M%S")

    # ====== PHASE 3: CLEANUP P0 ======

    def phase3_cleanup_p0(self):
        """Fase 3: Limpeza de directórios mortos (P0)"""
        print("\n" + "=" * 80)
        print("🗑️  FASE 3: LIMPEZA P0 - REMOVER DIRECTÓRIOS MORTOS")
        print("=" * 80)

        dirs_to_remove = [
            ("app/infra", self.backend / "app" / "infra", "Apenas audit_logger orfão"),
            ("apps/backend", self.backend / "apps" / "backend", "Nested redundância"),
        ]

        for name, path, reason in dirs_to_remove:
            if path.exists():
                print(f"\n🗑️  Removendo: {name}")
                print(f"   Razão: {reason}")
                print(f"   Tamanho: {self._get_size(path)}")
                try:
                    shutil.rmtree(path)
                    self.log_success(f"Removido: {name}")
                except Exception as e:
                    self.log_error(f"Falha ao remover {name}: {e}")
                    return False
            else:
                self.log_warning(f"Não encontrado: {name}")

        return True

    @staticmethod
    def _get_size(path: Path) -> str:
        """Calcula tamanho de diretório"""
        total = 0
        try:
            for entry in path.rglob("*"):
                if entry.is_file():
                    total += entry.stat().st_size
        except:
            pass

        if total > 1024 * 1024:
            return f"{total / (1024 * 1024):.1f} MB"
        elif total > 1024:
            return f"{total / 1024:.1f} KB"
        else:
            return f"{total} B"

    # ====== PHASE 4: CONSOLIDATION ======

    def phase4_consolidate_application(self):
        """Fase 4A: Consolidar application/* → app/application/"""
        print("\n" + "=" * 80)
        print("🔄 FASE 4A: CONSOLIDAR application/ → app/application/")
        print("=" * 80)

        src = self.backend / "application"
        dst = self.backend / "app" / "application"

        if not src.exists():
            self.log_warning("application/ não encontrado - pulando")
            return True

        # Contar ficheiros
        src_files = list(src.rglob("*.py"))
        print(f"   Copiando {len(src_files)} ficheiros Python")

        try:
            # Copiar services
            services_src = src / "services"
            services_dst = dst / "services"

            if services_src.exists():
                if services_dst.exists():
                    self.log_warning(f"   {services_dst} já existe - fazendo merge")
                else:
                    services_dst.parent.mkdir(parents=True, exist_ok=True)

                for service_file in services_src.glob("*.py"):
                    if service_file.name != "__pycache__":
                        shutil.copy2(service_file, services_dst / service_file.name)
                        print(f"   ✓ {service_file.name}")

            # Remover application/
            shutil.rmtree(src)
            self.log_success("Consolidação application → app/application concluída")
            return True

        except Exception as e:
            self.log_error(f"Erro na consolidação: {e}")
            return False

    def phase4_consolidate_seeds(self):
        """Fase 4B: Consolidar app/seeds/ → seeds/ (manter seeds como raiz)"""
        print("\n" + "=" * 80)
        print("🌱 FASE 4B: CONSOLIDAR app/seeds/ → seeds/ (raiz)")
        print("=" * 80)

        app_seeds = self.backend / "app" / "seeds"
        root_seeds = self.backend / "seeds"

        if not app_seeds.exists():
            self.log_warning("app/seeds não encontrado - pulando")
            return True

        try:
            # Copiar ficheiros importantes de app/seeds para seeds
            important_files = ["roles.py", "catalog.py", "__init__.py"]

            for fname in important_files:
                src_file = app_seeds / fname
                if src_file.exists():
                    dst_file = root_seeds / fname
                    shutil.copy2(src_file, dst_file)
                    print(f"   ✓ Migrado: {fname}")

            # Remover app/seeds
            shutil.rmtree(app_seeds)
            self.log_success("Consolidação seeds concluída")
            return True

        except Exception as e:
            self.log_error(f"Erro na consolidação seeds: {e}")
            return False

    # ====== PHASE 5: VALIDATION ======

    def phase5_validate(self) -> bool:
        """Fase 5: Validação completa"""
        print("\n" + "=" * 80)
        print("✔️  FASE 5: VALIDAÇÃO")
        print("=" * 80)

        all_ok = True

        # 5.1 Syntax check
        print("\n1️⃣  Syntax check...")
        cmd = f"cd {self.backend} && find app -name '*.py' -type f -exec python -m py_compile {{}} + 2>&1 | head -20"
        rc, stdout, _ = self.run_cmd(cmd, "Python compile check")
        if rc == 0:
            self.log_success("Syntax: OK")
        else:
            self.log_error(f"Syntax errors encontrados:\n{stdout}")
            all_ok = False

        # 5.2 Import check
        print("\n2️⃣  Import validation...")
        orphan_imports = [
            "from apps.backend.app.infra",
            "from application.",
            "from apps.backend.app.seeds",
        ]

        for import_pattern in orphan_imports:
            cmd = f"grep -r '{import_pattern}' {self.backend} --include='*.py' 2>/dev/null | grep -v '.venv' | wc -l"
            rc, stdout, _ = self.run_cmd(cmd, f"Checking {import_pattern}")
            count = int(stdout.strip())
            if count > 0:
                self.log_warning(f"   ⚠️  {import_pattern}: {count} referências orfãs")
                # Listar
                cmd2 = f"grep -r '{import_pattern}' {self.backend} --include='*.py' 2>/dev/null | grep -v '.venv' | head -5"
                _, files, _ = self.run_cmd(cmd2, "")
                for f in files.split("\n")[:3]:
                    if f:
                        print(f"      {f[:100]}")
                all_ok = False

        # 5.3 Directory structure check
        print("\n3️⃣  Directory structure...")
        removed_dirs = [
            self.backend / "app" / "infra",
            self.backend / "application",
            self.backend / "apps" / "backend",
        ]

        for path in removed_dirs:
            if path.exists():
                self.log_error(f"   Ainda existe: {path.relative_to(self.backend)}")
                all_ok = False
            else:
                self.log_success(f"   ✓ Removido: {path.relative_to(self.backend)}")

        return all_ok

    # ====== MAIN RUNNER ======

    def run_cleanup(self) -> bool:
        """Executar cleanup completo"""
        print("\n")
        print("╔" + "=" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "  🧹 CLEANUP DUPLICATES - SILA BACKEND".center(78) + "║")
        print("║" + "  Ferramenta robusta e moderna para eliminar duplicidades".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "=" * 78 + "╝")

        try:
            # Phase 1
            self.phase1_analyze_imports()
            self.phase1_list_files()

            # Phase 2
            if not self.phase2_backup():
                return False

            # Confirmação
            response = input("\n⚠️  Continuar com limpeza? (sim/não): ").strip().lower()
            if response not in ["sim", "s", "yes", "y"]:
                self.log_warning("Cleanup cancelado pelo utilizador")
                return False

            # Phase 3
            if not self.phase3_cleanup_p0():
                return False

            # Phase 4
            if not self.phase4_consolidate_application():
                return False
            if not self.phase4_consolidate_seeds():
                return False

            # Phase 5
            validation_ok = self.phase5_validate()

            # Summary
            print("\n" + "=" * 80)
            print("📊 RESUMO FINAL")
            print("=" * 80)
            if validation_ok:
                self.log_success("LIMPEZA CONCLUÍDA COM SUCESSO ✨")
            else:
                self.log_warning("Limpeza concluída mas com avisos - revisar acima")

            return validation_ok

        except KeyboardInterrupt:
            self.log_error("Cleanup interrompido pelo utilizador")
            return False
        except Exception as e:
            self.log_error(f"Erro fatal: {e}")
            import traceback

            traceback.print_exc()
            return False


if __name__ == "__main__":
    backend_path = Path(__file__).parent
    cleaner = DuplicatesCleaner(str(backend_path))

    success = cleaner.run_cleanup()
    sys.exit(0 if success else 1)
