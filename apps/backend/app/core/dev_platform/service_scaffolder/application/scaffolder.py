import os


class ServiceScaffolder:

    def create_service(

        self,
        base_path,
        service_name

    ):

        service_path = os.path.join(base_path, service_name)

        structure = [

            "api",
            "domain",
            "application",
            "infrastructure",
            "tests"

        ]

        os.makedirs(service_path, exist_ok=True)

        for folder in structure:

            os.makedirs(

                os.path.join(service_path, folder),
                exist_ok=True

            )

        return service_path
