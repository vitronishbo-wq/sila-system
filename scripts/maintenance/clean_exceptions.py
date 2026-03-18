import os

BASE_MODULES_DIR = "apps/backend/app/modules"
FACTORY_IMPORT = "from apps.backend.core.exceptions.factory import ExceptionFactory\n"


def clean_module_exceptions() -> None:
    print("🚀 Iniciando expurgo de arquivos de exceção...")
    count = 0

    for module in os.listdir(BASE_MODULES_DIR):
        module_path = os.path.join(BASE_MODULES_DIR, module)
        if not os.path.isdir(module_path):
            continue

        potential_paths = [
            os.path.join(module_path, "domain", "exceptions.py"),
            os.path.join(module_path, "exceptions.py"),
        ]

        for exc_file in potential_paths:
            if os.path.exists(exc_file):
                module_name = module.replace("_", " ").title().replace(" ", "")

                new_content = [
                    '"""\n',
                    f"Auto-generated exceptions for {module_name} module\n",
                    '"""\n',
                    FACTORY_IMPORT,
                    f'\n_exc = ExceptionFactory.create_module_exceptions("{module_name}")\n\n',
                    f"{module_name}Exception = _exc.Base\n",
                    f"{module_name}NotFound = _exc.NotFound\n",
                    f"{module_name}ValidationError = _exc.ValidationError\n",
                    f"{module_name}Unauthorized = _exc.Unauthorized\n",
                    f"{module_name}Conflict = _exc.Conflict\n",
                    f"{module_name}InvalidState = _exc.InvalidState\n",
                    f"{module_name}InvalidStateError = _exc.InvalidStateError\n",
                ]

                with open(exc_file, "w", encoding="utf-8") as handle:
                    handle.writelines(new_content)

                print(f"✅ Consolidado: {module} -> {exc_file}")
                count += 1

    print(f"\n✨ Operação concluída! {count} arquivos limpos e padronizados.")


if __name__ == "__main__":
    clean_module_exceptions()
