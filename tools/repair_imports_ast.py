#!/usr/bin/env python3

import ast
from pathlib import Path

ROOT = Path("apps/backend/app")

OLD = "app.modules.justice.civil_registry"
NEW = "app.modules.justice.bounded_contexts"

changed_files = []


class ImportRewriter(ast.NodeTransformer):
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.startswith(OLD):
                alias.name = alias.name.replace(OLD, NEW)
        return node

    def visit_ImportFrom(self, node):
        if node.module and node.module.startswith(OLD):
            node.module = node.module.replace(OLD, NEW)
        return node


def rewrite_file(path: Path) -> None:
    try:
        source = path.read_text()
        tree = ast.parse(source)

        transformer = ImportRewriter()
        new_tree = transformer.visit(tree)

        new_code = ast.unparse(new_tree)

        if source != new_code:
            path.write_text(new_code)
            changed_files.append(str(path))
    except Exception:
        pass


for py in ROOT.rglob("*.py"):
    rewrite_file(py)

print("FILES REWRITTEN:", len(changed_files))
for f in changed_files:
    print(f)
