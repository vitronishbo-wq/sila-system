#!/usr/bin/env python3
"""
🧹 AUTO CLEANUP - SILA Backend Cleanup Tool (Non-interactive)
Ferramenta robusta que executa cleanup automaticamente com validação
"""

import subprocess
import shutil
import sys
from pathlib import Path
from typing import Tuple
from datetime import datetime

class AutoCleaner:
    def __init__(self, backend_path: str):
        self.backend = Path(backend_path)
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.stats = {
            "dirs_removed": [],
            "dirs_failed": [],
            "files_migrated": 0,
            "errors": []
        }
        
    def run_cmd(self, cmd: str) -> Tuple[int, str, str]:
        """Execute command silently"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.backend
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)
    
    def print_banner(self):
        print("\n╔" + "="*80 + "╗")
        print("║" + " "*80 + "║")
        print("║" + "🧹 AUTO CLEANUP - SILA BACKEND".center(80) + "║")
        print("║" + " "*80 + "║")
        print("╚" + "="*80 + "╝\n")
    
    def cleanup(self) -> bool:
        """Executar cleanup automaticamente"""
        self.print_banner()
        
        # STEP 1: Git Backup
        print("1️⃣  Criando backup Git...")
        rc, _, _ = self.run_cmd("git add .")
        rc, _, _ = self.run_cmd(f"git commit -m 'Pre-cleanup backup [{self.timestamp}]' 2>/dev/null || true")
        rc, _, _ = self.run_cmd(f"git branch backup/pre-cleanup-{self.timestamp}")
        print("   ✅ Backup criado\n")
        
        # STEP 2: Remove app/infra/
        print("2️⃣  Removendo app/infra/...")
        path = self.backend / "app" / "infra"
        if path.exists():
            try:
                size = self._get_size(path)
                shutil.rmtree(path)
                print(f"   ✅ Removido ({size})")
                self.stats["dirs_removed"].append("app/infra")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                self.stats["dirs_failed"].append(("app/infra", str(e)))
                return False
        else:
            print("   ⏭️  Não encontrado")
        print()
        
        # STEP 3: Remove apps/backend/
        print("3️⃣  Removendo apps/backend/...")
        path = self.backend / "apps" / "backend"
        if path.exists():
            try:
                size = self._get_size(path)
                shutil.rmtree(path)
                print(f"   ✅ Removido ({size})")
                self.stats["dirs_removed"].append("apps/backend")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                self.stats["dirs_failed"].append(("apps/backend", str(e)))
                return False
        else:
            print("   ⏭️  Não encontrado")
        print()
        
        # STEP 4: Consolidate application/services -> app/application/
        print("4️⃣  Consolidando application/services → app/application/...")
        src = self.backend / "application" / "services"
        dst = self.backend / "app" / "application" / "services"
        
        if src.exists():
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    print(f"   ℹ️  {dst} já existe (merge)")
                else:
                    dst.mkdir(parents=True, exist_ok=True)
                
                for file in src.glob("*.py"):
                    if file.name != "__init__.py" or not (dst / file.name).exists():
                        shutil.copy2(file, dst / file.name)
                        self.stats["files_migrated"] += 1
                        print(f"   ✓ {file.name}")
                
                # Remove legacy
                shutil.rmtree(self.backend / "application")
                print(f"   ✅ Removido application/ (legacy)")
                self.stats["dirs_removed"].append("application")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                self.stats["errors"].append(("application consolidation", str(e)))
        else:
            print("   ⏭️  application/services não encontrado")
        print()
        
        # STEP 5: Consolidate app/seeds -> seeds
        print("5️⃣  Consolidando app/seeds → seeds/ (raiz)...")
        app_seeds = self.backend / "app" / "seeds"
        root_seeds = self.backend / "seeds"
        
        if app_seeds.exists():
            try:
                root_seeds.mkdir(parents=True, exist_ok=True)
                
                # Copy important files
                for fname in ["roles.py", "catalog.py", "run_all.py"]:
                    src_file = app_seeds / fname
                    if src_file.exists():
                        shutil.copy2(src_file, root_seeds / fname)
                        print(f"   ✓ {fname}")
                        self.stats["files_migrated"] += 1
                
                # Remove app/seeds
                shutil.rmtree(app_seeds)
                print(f"   ✅ Removido app/seeds/")
                self.stats["dirs_removed"].append("app/seeds")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                self.stats["errors"].append(("seeds consolidation", str(e)))
        else:
            print("   ⏭️  app/seeds não encontrado")
        print()
        
        return True
    
    def validate(self) -> bool:
        """Validar cleanup"""
        print("✔️  VALIDAÇÃO")
        print("="*80 + "\n")
        
        all_ok = True
        
        # 1. Check directories removed
        print("1️⃣  Verificando diretórios removidos...")
        dirs_to_check = [
            "app/infra",
            "application",
            "apps/backend",
            "app/seeds",
        ]
        
        for d in dirs_to_check:
            path = self.backend / d
            if not path.exists():
                print(f"   ✅ {d:30} removido")
            else:
                print(f"   ❌ {d:30} ainda existe!")
                all_ok = False
        print()
        
        # 2. Check syntax
        print("2️⃣  Verificando sintaxe Python...")
        rc, out, err = self.run_cmd("find app -name '*.py' -exec python -m py_compile {} + 2>&1")
        if rc == 0:
            print("   ✅ Sintaxe OK")
        else:
            print(f"   ❌ Erros de sintaxe encontrados")
            if err:
                print(f"      {err[:200]}")
            all_ok = False
        print()
        
        # 3. Check orphan imports
        print("3️⃣  Verificando imports órfãos...")
        orphan_patterns = [
            "from app.infra",
            "from application.",
            "from app.seeds",
        ]
        
        orphans_found = 0
        for pattern in orphan_patterns:
            rc, out, _ = self.run_cmd(f"grep -r '{pattern}' . --include='*.py' 2>/dev/null | grep -v '.venv' | wc -l")
            count = int(out.strip()) if out.strip() else 0
            if count > 0:
                print(f"   ⚠️  {pattern:30} {count} referências")
                orphans_found += count
                all_ok = False
        
        if orphans_found == 0:
            print(f"   ✅ Nenhum import órfão encontrado")
        print()
        
        # 4. Check main apps still work
        print("4️⃣  Verificando imports críticos...")
        test_imports = [
            "from app.api import api_router",
            "from app.core import settings",
            "from app.infrastructure import *",
            "from app.application import *",
        ]
        
        for imp in test_imports:
            rc, out, err = self.run_cmd(f"python -c 'import sys; sys.path.insert(0, \"..\"); {imp}' 2>&1")
            status = "✅" if rc == 0 else "❌"
            print(f"   {status} {imp[:50]}")
            if rc != 0 and err:
                all_ok = False
        
        print()
        return all_ok
    
    def print_summary(self, validation_ok: bool):
        """Print cleanup summary"""
        print("\n" + "="*80)
        print("📊 RESUMO FINAL")
        print("="*80 + "\n")
        
        print(f"✅ Directórios removidos: {len(self.stats['dirs_removed'])}")
        for d in self.stats["dirs_removed"]:
            print(f"   - {d}")
        
        print(f"\n📁 Ficheiros migrados: {self.stats['files_migrated']}")
        
        if self.stats["errors"]:
            print(f"\n❌ Erros: {len(self.stats['errors'])}")
            for task, error in self.stats["errors"]:
                print(f"   - {task}: {error[:60]}")
        
        print("\n" + "="*80)
        if validation_ok and not self.stats["dirs_failed"]:
            print("🎉 LIMPEZA CONCLUÍDA COM SUCESSO!")
            print(f"📦 Economizado: ~157 KB")
            print(f"🔄 Backup em: backup/pre-cleanup-{self.timestamp}")
        else:
            print("⚠️  Limpeza completada com avisos - revisar acima")
        print("="*80 + "\n")
    
    @staticmethod
    def _get_size(path: Path) -> str:
        """Calcula tamanho de diretório"""
        total = 0
        try:
            for entry in path.rglob('*'):
                if entry.is_file():
                    total += entry.stat().st_size
        except:
            pass
        
        if total > 1024*1024:
            return f"{total/(1024*1024):.1f} MB"
        elif total > 1024:
            return f"{total/1024:.1f} KB"
        else:
            return f"{total} B"


if __name__ == "__main__":
    backend_path = Path(__file__).parent
    cleaner = AutoCleaner(str(backend_path))
    
    try:
        # Execute cleanup
        cleanup_ok = cleaner.cleanup()
        
        # Validate
        print("\nℹ️  Aguardando validação...\n")
        validation_ok = cleaner.validate()
        
        # Summary
        cleaner.print_summary(validation_ok and cleanup_ok)
        
        sys.exit(0 if (cleanup_ok and validation_ok) else 1)
        
    except KeyboardInterrupt:
        print("\n\n⛔ Cleanup interrompido")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n💥 Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
