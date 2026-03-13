class ArchitectureGuard:

    FORBIDDEN_IMPORTS = [

        "core.iam"

    ]

    def scan_imports(

        self,
        file_content

    ):

        violations = []

        for forbidden in self.FORBIDDEN_IMPORTS:

            if forbidden in file_content:

                violations.append(forbidden)

        return violations
