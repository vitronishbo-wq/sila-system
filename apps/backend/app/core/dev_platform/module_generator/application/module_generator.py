import os


class ModuleGenerator:

    def generate(

        self,
        modules_path,
        module_name

    ):

        module_path = os.path.join(

            modules_path,
            module_name

        )

        structure = [

            "api",
            "application",
            "domain",
            "infrastructure",
            "tests"

        ]

        os.makedirs(module_path, exist_ok=True)

        for folder in structure:

            os.makedirs(

                os.path.join(module_path, folder),
                exist_ok=True

            )

        return module_path
