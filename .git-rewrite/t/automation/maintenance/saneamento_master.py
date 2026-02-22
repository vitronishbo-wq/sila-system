#!/usr/bin/env python3
"""
Script Mestre de Saneamento do Projeto SILA_SYSTEM
Automatiza todas as ações de saneamento técnico identificadas.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_ROOT = PROJECT_ROOT / "backend"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
REPORT_DIR = SCRIPTS_DIR / "saneamento_reports"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Cores para output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SaneamentoMaster:
    """Orquestrador do processo de saneamento."""

    def __init__(self):
        self.report_dir = REPORT_DIR
        self.report_dir.mkdir(exist_ok=True)
        self.log_file = self.report_dir / f"saneamento_{TIMESTAMP}.log"
        self.results = {
            'timestamp': TIMESTAMP,
            'steps': [],
            'errors': [],
            'warnings': [],
            'success': True
        }

    def log(self, message: str, level: str = "INFO"):
        """Registra mensagem no log e console."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"

        # Console com cores
        if level == "ERROR":
            print(f"{Colors.FAIL}{log_msg}{Colors.ENDC}")
        elif level == "WARNING":
            print(f"{Colors.WARNING}{log_msg}{Colors.ENDC}")
        elif level == "SUCCESS":
            print(f"{Colors.OKGREEN}{log_msg}{Colors.ENDC}")
        elif level == "HEADER":
            print(f"{Colors.HEADER}{Colors.BOLD}{log_msg}{Colors.ENDC}")
        else:
            print(log_msg)

        # Arquivo de log
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')

    def run_script(self, script_path: Path, description: str) -> Tuple[bool, str]:
        """Executa um script Python e retorna resultado."""
        self.log(f"Executando: {description}", "INFO")

        try:
            result = subprocess.run([sys.executable, str(script_path)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout)

            if result.returncode == 0:
                self.log(f"✓ {description} - Concluído", "SUCCESS")
                return True, result.stdout
            else:
                self.log(f"✗ {description} - Falhou", "ERROR")
                self.log(f"Erro: {result.stderr}", "ERROR")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            self.log(f"✗ {description} - Timeout", "ERROR")
            return False, "Timeout após 5 minutos"
        except Exception as e:
            self.log(f"✗ {description} - Exceção: {str(e)}", "ERROR")
            return False, str(e)

    def step_1_corrigir_estrutura_modulos(self):
        """Passo 1: Corrigir estrutura de módulos."""
        self.log("=" * 80, "HEADER")
        self.log("PASSO 1: Corrigir Estrutura de Módulos", "HEADER")
        self.log("=" * 80, "HEADER")

        step_result = {
            'step': 1,
            'name': 'Corrigir estrutura de módulos',
            'actions': [],
            'success': True
        }

        # 1.1 - Verificar e corrigir estrutura de módulos
        script = SCRIPTS_DIR / "generate_modules_structure.py"
        if script.exists():
            success, output = self.run_script(script, "Gerar estrutura padrão de módulos")
            step_result['actions'].append({
                'action': 'generate_modules_structure',
                'success': success,
                'output': output[:500]  # Limitar tamanho
            })
            if not success:
                step_result['success'] = False

        # 1.2 - Verificar integridade dos módulos
        script = SCRIPTS_DIR / "check_module_integrity.py"
        if script.exists():
            success, output = self.run_script(script, "Verificar integridade dos módulos")
            step_result['actions'].append({
                'action': 'check_module_integrity',
                'success': success,
                'output': output[:500]
            })

        self.results['steps'].append(step_result)
        return step_result['success']

    def step_2_resolver_importacoes(self):
        """Passo 2: Resolver importações quebradas e ciclos."""
        self.log("=" * 80, "HEADER")
        self.log("PASSO 2: Resolver Importações e Dependências Cíclicas", "HEADER")
        self.log("=" * 80, "HEADER")

        step_result = {
            'step': 2,
            'name': 'Resolver importações',
            'actions': [],
            'success': True
        }

        scripts_to_run = [
            ("fix_imports.py", "Corrigir imports gerais"),
            ("fix_broken_imports.py", "Corrigir imports quebrados"),
            ("fix_auth_utils_imports.py", "Corrigir imports de auth_utils"),
            ("fix_security_imports.py", "Corrigir imports de security"),
            ("detect_and_fix_import_cycles.py", "Detectar e corrigir ciclos de importação"),
        ]

        for script_name, description in scripts_to_run:
            script = SCRIPTS_DIR / script_name
            if script.exists():
                success, output = self.run_script(script, description)
                step_result['actions'].append({
                    'action': script_name,
                    'success': success,
                    'output': output[:500]
                })
                if not success:
                    step_result['success'] = False
            else:
                self.log(f"⚠ Script não encontrado: {script_name}", "WARNING")

        self.results['steps'].append(step_result)
        return step_result['success']

    def step_3_padronizar_camadas(self):
        """Passo 3: Padronizar camadas por domínio."""
        self.log("=" * 80, "HEADER")
        self.log("PASSO 3: Padronizar Camadas por Domínio", "HEADER")
        self.log("=" * 80, "HEADER")

        step_result = {
            'step': 3,
            'name': 'Padronizar camadas',
            'actions': [],
            'success': True
        }

        # Garantir que todos os módulos tenham a estrutura completa
        script = SCRIPTS_DIR / "check_and_generate_modules.py"
        if script.exists():
            success, output = self.run_script(script, "Verificar e gerar estrutura de módulos")
            step_result['actions'].append({
                'action': 'check_and_generate_modules',
                'success': success,
                'output': output[:500]
            })
            if not success:
                step_result['success'] = False

        self.results['steps'].append(step_result)
        return step_result['success']

    def step_4_corrigir_arquivos_corrompidos(self):
        """Passo 4: Corrigir arquivos corrompidos."""
        self.log("=" * 80, "HEADER")
        self.log("PASSO 4: Corrigir Arquivos Corrompidos", "HEADER")
        self.log("=" * 80, "HEADER")

        step_result = {
            'step': 4,
            'name': 'Corrigir arquivos corrompidos',
            'actions': [],
            'success': True
        }

        scripts_to_run = [
            ("fix_encoding.py", "Corrigir encoding de arquivos"),
            ("fix_unterminated_strings.py", "Corrigir strings não terminadas"),
            ("fix_syntax_errors_targeted.py", "Corrigir erros de sintaxe"),
            ("validate_py_syntax.py", "Validar sintaxe Python"),
        ]

        for script_name, description in scripts_to_run:
            script = SCRIPTS_DIR / script_name
            if script.exists():
                success, output = self.run_script(script, description)
                step_result['actions'].append({
                    'action': script_name,
                    'success': success,
                    'output': output[:500]
                })
                if not success:
                    step_result['success'] = False
            else:
                self.log(f"⚠ Script não encontrado: {script_name}", "WARNING")

        self.results['steps'].append(step_result)
        return step_result['success']

    def step_5_validar_ambiente(self):
        """Passo 5: Validar e unificar variáveis de ambiente."""
        self.log("=" * 80, "HEADER")
        self.log("PASSO 5: Validar Variáveis de Ambiente", "HEADER")
        self.log("=" * 80, "HEADER")

        step_result = {
            'step': 5,
            'name': 'Validar ambiente',
            'actions': [],
            'success': True
        }

        scripts_to_run = [
            ("validate_env.py", "Validar variáveis de ambiente"),
            ("padronizar_envs.py", "Padronizar arquivos .env"),
            ("validar_env_critico.py", "Validar variáveis críticas"),
        ]

        for script_name, description in scripts_to_run:
            script = SCRIPTS_DIR / script_name
            if script.exists():
                success, output = self.run_script(script, description)
                step_result['actions'].append({
                    'action': script_name,
                    'success': success,
                    'output': output[:500]
                })
                if not success:
                    step_result['success'] = False
            else:
                self.log(f"⚠ Script não encontrado: {script_name}", "WARNING")

        self.results['steps'].append(step_result)
        return step_result['success']

    def step_6_harmonizar_frontend_backend(self):
        """Passo 6: Harmonizar frontend/backend."""
        self.log("=" * 80, "HEADER")
        self.log("PASSO 6: Harmonizar Frontend/Backend", "HEADER")
        self.log("=" * 80, "HEADER")

        step_result = {
            'step': 6,
            'name': 'Harmonizar frontend/backend',
            'actions': [],
            'success': True
        }

        script = SCRIPTS_DIR / "check-frontend-sync.py"
        if script.exists():
            success, output = self.run_script(script, "Verificar sincronização frontend/backend")
            step_result['actions'].append({
                'action': 'check-frontend-sync',
                'success': success,
                'output': output[:500]
            })
            if not success:
                step_result['success'] = False
        else:
            self.log("⚠ Script check-frontend-sync.py não encontrado", "WARNING")

        self.results['steps'].append(step_result)
        return step_result['success']

    def step_7_garantir_testes(self):
        """Passo 7: Garantir testes mínimos."""
        self.log("=" * 80, "HEADER")
        self.log("PASSO 7: Garantir Testes Mínimos", "HEADER")
        self.log("=" * 80, "HEADER")

        step_result = {
            'step': 7,
            'name': 'Garantir testes mínimos',
            'actions': [],
            'success': True
        }

        # Verificar se existe script de geração de testes
        test_scripts = [
            SCRIPTS_DIR / "tests" / "generate_tests_simple.py",
            SCRIPTS_DIR / "tests" / "generate_tests.py"
        ]

        for script in test_scripts:
            if script.exists():
                success, output = self.run_script(script, f"Gerar testes com {script.name}")
                step_result['actions'].append({
                    'action': script.name,
                    'success': success,
                    'output': output[:500]
                })
                break
        else:
            self.log("⚠ Nenhum script de geração de testes encontrado", "WARNING")

        self.results['steps'].append(step_result)
        return step_result['success']

    def generate_final_report(self):
        """Gera relatório final do saneamento."""
        self.log("=" * 80, "HEADER")
        self.log("GERANDO RELATÓRIO FINAL", "HEADER")
        self.log("=" * 80, "HEADER")

        # Salvar JSON
        json_report = self.report_dir / f"saneamento_report_{TIMESTAMP}.json"
        with open(json_report, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        # Gerar Markdown
        md_report = self.report_dir / f"saneamento_report_{TIMESTAMP}.md"
        with open(md_report, 'w', encoding='utf-8') as f:
            f.write(f"# Relatório de Saneamento - SILA System\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Resumo Executivo\n\n")

            total_steps = len(self.results['steps'])
            successful_steps = sum(1 for s in self.results['steps'] if s['success'])

            f.write(f"- **Total de passos:** {total_steps}\n")
            f.write(f"- **Passos bem-sucedidos:** {successful_steps}\n")
            f.write(f"- **Passos com falhas:** {total_steps - successful_steps}\n")
            f.write(f"- **Status geral:** {'✅ SUCESSO' if self.results['success'] else '❌ FALHAS DETECTADAS'}\n\n")

            f.write(f"## Detalhamento por Passo\n\n")

            for step in self.results['steps']:
                status_icon = "✅" if step['success'] else "❌"
                f.write(f"### {status_icon} Passo {step['step']}: {step['name']}\n\n")

                for action in step['actions']:
                    action_status = "✓" if action['success'] else "✗"
                    f.write(f"- **{action_status} {action['action']}**\n")
                    if not action['success']:
                        f.write(f"  - Erro: {action['output'][:200]}...\n")
                f.write("\n")

            if self.results['errors']:
                f.write(f"## ❌ Erros Encontrados\n\n")
                for error in self.results['errors']:
                    f.write(f"- {error}\n")
                f.write("\n")

            if self.results['warnings']:
                f.write(f"## ⚠️ Avisos\n\n")
                for warning in self.results['warnings']:
                    f.write(f"- {warning}\n")
                f.write("\n")

        self.log(f"Relatório JSON salvo em: {json_report}", "SUCCESS")
        self.log(f"Relatório Markdown salvo em: {md_report}", "SUCCESS")
        self.log(f"Log completo salvo em: {self.log_file}", "SUCCESS")

    def run(self):
        """Executa todos os passos do saneamento."""
        self.log("=" * 80, "HEADER")
        self.log("INICIANDO SANEAMENTO MASTER DO PROJETO SILA_SYSTEM", "HEADER")
        self.log("=" * 80, "HEADER")

        try:
            # Executar todos os passos
            self.step_1_corrigir_estrutura_modulos()
            self.step_2_resolver_importacoes()
            self.step_3_padronizar_camadas()
            self.step_4_corrigir_arquivos_corrompidos()
            self.step_5_validar_ambiente()
            self.step_6_harmonizar_frontend_backend()
            self.step_7_garantir_testes()

            # Verificar se houve falhas
            failed_steps = [s for s in self.results['steps'] if not s['success']]
            if failed_steps:
                self.results['success'] = False
                self.log(f"⚠ {len(failed_steps)} passos falharam", "WARNING")
            else:
                self.log("✓ Todos os passos concluídos com sucesso!", "SUCCESS")

        except Exception as e:
            self.log(f"Erro crítico durante saneamento: {str(e)}", "ERROR")
            self.results['success'] = False
            self.results['errors'].append(str(e))

        finally:
            # Sempre gerar relatório final
            self.generate_final_report()

        return self.results['success']


def main()
    """Função principal."""
    saneamento = SaneamentoMaster()
    success = saneamento.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()]
