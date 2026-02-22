#!/usr/bin/env python3
"""
SQLITE COMPLETE REMOVAL AUTOMATION TOOL
=========================================

Ferramenta poderosa para remover completamente SQLite do projeto SILA
e reparar todos os danos causados.
"""

import os
import re
import sys
import json
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime

class ChangeType(Enum):
    """Tipos de mudancas realizadas"""
    FILE_MODIFIED = "file_modified"
    FILE_DELETED = "file_deleted"

@dataclass
class FileChange:
    """Representa uma mudanca em um arquivo"""
    file_path: str
    change_type: ChangeType
    pattern: str = ""
    replacements_count: int = 0
    
    def to_dict(self):
        return {
            "file_path": self.file_path,
            "change_type": self.change_type.value,
            "pattern": self.pattern,
            "replacements_count": self.replacements_count,
        }

@dataclass
class RemovalReport:
    """Relatorio completo da remocao"""
    timestamp: str
    total_files_scanned: int = 0
    files_modified: int = 0
    files_deleted: int = 0
    total_patterns_found: int = 0
    total_patterns_replaced: int = 0
    changes: List[FileChange] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    analysis_only: bool = True

class SQLiteRemovalEngine:
    """Motor principal de remocao de SQLite"""
    
    PATTERNS = {
        "imports": [
            (r"from sqlite3 import.*\n", ""),
            (r"import sqlite3\n", ""),
        ],
        "database_urls": [
            (r'sqlite:///:memory:', r'postgresql+asyncpg://localhost/sila_test'),
            (r'sqlite\+aiosqlite:///:memory:', r'postgresql+asyncpg://localhost/sila_test'),
            (r'sqlite:///\./([^"]*\.db)', r'postgresql+asyncpg://localhost/sila_test'),
            (r'sqlite\+aiosqlite:///\./([^"]*\.db)', r'postgresql+asyncpg://localhost/sila_test'),
        ],
        "comments": [
            (r'#.*in-memory SQLite.*\n', ""),
            (r'#.*SQLite database.*\n', ""),
        ],
    }
    
    IGNORE_PATHS = {
        ".git", ".venv", "venv", "__pycache__", ".pytest_cache", 
        "node_modules", ".next", "build", "dist",
    }
    
    def __init__(self, workspace_path: str, dry_run: bool = True):
        self.workspace = Path(workspace_path)
        self.dry_run = dry_run
        self.report = RemovalReport(timestamp=datetime.now().isoformat())
        self.backup_dir = None
        self.changes: Dict[str, FileChange] = {}
        
    def should_ignore_path(self, path: Path) -> bool:
        """Verifica se caminho deve ser ignorado"""
        for part in path.parts:
            if part in self.IGNORE_PATHS:
                return True
        return False
    
    def find_sqlite_references(self) -> Dict[str, List[Tuple[int, str]]]:
        """Encontra todas as referencias a SQLite no codebase"""
        references = {}
        python_files = list(self.workspace.rglob("*.py"))
        
        for file_path in python_files:
            if self.should_ignore_path(file_path) or not file_path.is_file():
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                if 'sqlite' in content.lower():
                    lines = content.split('\n')
                    sqlite_lines = [
                        (i+1, line) for i, line in enumerate(lines)
                        if 'sqlite' in line.lower()
                    ]
                    if sqlite_lines:
                        references[str(file_path)] = sqlite_lines
                        self.report.total_patterns_found += len(sqlite_lines)
            except Exception as e:
                self.report.warnings.append(f"Nao pude ler {file_path}: {str(e)}")
        
        return references
    
    def analyze(self) -> RemovalReport:
        """Analisa projeto sem fazer mudancas"""
        print("[*] Analisando projeto para referencias SQLite...\n")
        
        references = self.find_sqlite_references()
        self.report.total_files_scanned = len(references)
        
        print(f"[ANALISE] Referencias SQLite:")
        print(f"{'='*60}")
        print(f"Total de arquivos com SQLite: {len(references)}")
        print(f"Total de linhas com SQLite: {self.report.total_patterns_found}")
        print(f"\nArquivos afetados:\n")
        
        for file_path, lines in sorted(references.items()):
            rel_path = Path(file_path).relative_to(self.workspace)
            print(f"  [{len(lines):2d}] {rel_path}")
        
        self.report.analysis_only = True
        return self.report
    
    def create_backup(self) -> str:
        """Cria backup do workspace antes das mudancas"""
        backup_dir = Path(tempfile.gettempdir()) / f"sila_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        conftest = self.workspace / "apps" / "backend" / "conftest.py"
        if conftest.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(conftest, backup_dir / "conftest.py.bak")
        
        print(f"[+] Backup criado em: {backup_dir}")
        self.backup_dir = backup_dir
        return str(backup_dir)
    
    def execute_removal(self) -> RemovalReport:
        """Executa remocao de SQLite"""
        print("\n[*] Executando remocao de SQLite...\n")
        
        references = self.find_sqlite_references()
        
        if not self.dry_run:
            self.create_backup()
        
        python_files = list(self.workspace.rglob("*.py"))
        
        for file_path in python_files:
            if self.should_ignore_path(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    original_content = f.read()
                
                if 'sqlite' not in original_content.lower():
                    continue
                
                new_content = original_content
                replacements = 0
                
                for pattern, replacement in self.PATTERNS["imports"]:
                    match = re.findall(pattern, new_content)
                    if match:
                        new_content = re.sub(pattern, replacement, new_content)
                        replacements += len(match)
                
                for pattern, replacement in self.PATTERNS["database_urls"]:
                    matches = re.findall(pattern, new_content)
                    if matches:
                        new_content = re.sub(pattern, replacement, new_content)
                        replacements += len(matches)
                
                for pattern, replacement in self.PATTERNS["comments"]:
                    matches = re.findall(pattern, new_content)
                    if matches:
                        new_content = re.sub(pattern, replacement, new_content)
                        replacements += len(matches)
                
                if replacements > 0:
                    if not self.dry_run:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                    
                    change = FileChange(
                        file_path=str(file_path),
                        change_type=ChangeType.FILE_MODIFIED,
                        pattern="sqlite_removal",
                        replacements_count=replacements,
                    )
                    self.changes[str(file_path)] = change
                    self.report.changes.append(change)
                    self.report.files_modified += 1
                    self.report.total_patterns_replaced += replacements
                    
                    rel_path = file_path.relative_to(self.workspace)
                    print(f"[OK] {rel_path}: {replacements} mudancas")
            
            except Exception as e:
                self.report.errors.append(f"Erro ao processar {file_path}: {str(e)}")
                print(f"[ERROR] {e}")
        
        self._process_env_files()
        self._cleanup_sqlite_files()
        
        self.report.analysis_only = False
        return self.report
    
    def _process_env_files(self):
        """Processa arquivos .env*"""
        env_files = [
            self.workspace / ".env.test",
            self.workspace / ".env.development",
        ]
        
        for env_file in env_files:
            if not env_file.exists():
                continue
            
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'sqlite' not in content.lower():
                continue
            
            new_content = content
            replacements = 0
            
            patterns = [
                (r'DATABASE_URL=postgresql+asyncpg://localhost/sila_test', 'DATABASE_URL=postgresql+asyncpg://localhost/sila_test'),
                (r'ASYNC_DATABASE_URL=sqlite\+aiopostgresql+asyncpg://localhost/sila_test', 'ASYNC_DATABASE_URL=postgresql+asyncpg://localhost/sila_test'),
            ]
            
            for pattern, replacement in patterns:
                if re.search(pattern, new_content):
                    new_content = re.sub(pattern, replacement, new_content)
                    replacements += 1
            
            if replacements > 0 and not self.dry_run:
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[OK] {env_file.name}: {replacements} mudancas")
    
    def _cleanup_sqlite_files(self):
        """Remove arquivos de banco SQLite deixados para tras"""
        db_files = list(self.workspace.rglob("*.db"))
        
        for db_file in db_files:
            if self.should_ignore_path(db_file):
                continue
            
            try:
                if not self.dry_run:
                    os.remove(db_file)
                    change = FileChange(
                        file_path=str(db_file),
                        change_type=ChangeType.FILE_DELETED,
                        pattern="sqlite_db_file",
                    )
                    self.report.changes.append(change)
                    self.report.files_deleted += 1
                
                rel_path = db_file.relative_to(self.workspace)
                print(f"[DEL] {rel_path}")
            except Exception as e:
                self.report.errors.append(f"Nao pude remover {db_file}: {str(e)}")
    
    def validate(self) -> bool:
        """Valida se SQLite foi completamente removido"""
        print("\n[*] Validando remocao de SQLite...\n")
        
        references = self.find_sqlite_references()
        
        if not references:
            print("[OK] SUCESSO! Nenhuma referencia a SQLite encontrada.")
            return True
        else:
            print(f"[!] AVISO: Ainda existem {len(references)} arquivo(s) com referencias SQLite")
            return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ferramenta automatica de remocao de SQLite"
    )
    
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Apenas analisa referencias SQLite"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Executa remocao completa de SQLite"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Valida se SQLite foi completamente removido"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=str(Path(__file__).parent.parent.parent),
        help="Caminho do workspace"
    )
    
    args = parser.parse_args()
    
    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"[ERROR] Workspace nao encontrado: {workspace}")
        sys.exit(1)
    
    print(f"\n[*] Analisando workspace: {workspace}\n")
    
    if args.analyze:
        engine = SQLiteRemovalEngine(str(workspace), dry_run=True)
        report = engine.analyze()
    
    elif args.execute:
        engine = SQLiteRemovalEngine(str(workspace), dry_run=False)
        report = engine.execute_removal()
        print(f"\n[+] Relatorio Final:")
        print(f"    Arquivos modificados: {report.files_modified}")
        print(f"    Padroes removidos: {report.total_patterns_replaced}")
        print(f"    Erros: {len(report.errors)}")
    
    elif args.validate:
        engine = SQLiteRemovalEngine(str(workspace))
        success = engine.validate()
        sys.exit(0 if success else 1)
    
    print("\n[+] Processo concluido!\n")

if __name__ == "__main__":
    main()
