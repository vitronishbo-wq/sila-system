# 🔄 Sila System - AI Development Workflow

Este documento detalha o ciclo de vida de desenvolvimento que a IA deve seguir para manter a cadência e qualidade do Sila System.

## 📈 Ciclo de Desenvolvimento Progressivo

A IA deve operar em ciclos pequenos e validados (Atomic Cycles).

### Fase 1: Análise e Reconhecimento
- **Mapeamento**: Localizar o módulo exato no `apps/backend/app/modules`.
- **Dependências**: Verificar se a mudança afeta outros módulos via `infrastructure/mappers.py`.
- **Contexto**: Ler o `__init__.py` do módulo para entender os pontos de exportação.

### Fase 2: Implementação (The DDD Way)
- **Novo Módulo?**: Inicie copiando o `apps/backend/TEMPLATE_DDD_MODULE.py`.
- **Mudança de Regra?**: Comece sempre pelo `domain/`.
- **Nova Funcionalidade?**:
    1. Defina o Caso de Uso no `application/commands.py`.
    2. Implemente a Entidade no `domain/entities.py`.
    3. Crie o Repositório no `infrastructure/repositories/`.
    4. Exponha o Endpoint no `presentation/router.py`.

### Fase 3: Persistência e Dados
- Se houver novos atributos ou modelos:
    1. Atualize o `infrastructure/models.py`.
    2. Execute `alembic revision --autogenerate -m "descrição"`.
    3. Revise o script gerado para garantir que não há deleções acidentais.

### Fase 4: Validação em Loop
1. **Teste Unitário**: Criar/atualizar teste na pasta `tests/` do módulo.
2. **Auto-Fix**: Se o `pytest` falhar, a IA deve analisar o traceback e corrigir imediatamente.
3. **Commit**: (Se configurado) Realizar commits atômicos para cada fase concluída.

---

## 🛠️ Ferramentas de Suporte ao Workflow

| Comando | Função |
| :--- | :--- |
| `make test-coverage` | Garante que o novo código está coberto por testes (>80%). |
| `bash setup_dev_env.sh` | Restaura o ambiente se houver falha de dependência. |
| `make typecheck` | Valida a consistência de tipos (Mypy). |

---
> [!TIP]
> Use a ferramenta `replace_file_content` para edições cirúrgicas. Evite substituir arquivos inteiros se apenas uma função for alterada.
