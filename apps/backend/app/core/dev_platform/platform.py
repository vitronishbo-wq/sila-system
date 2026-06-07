class SovereignDeveloperPlatform:
    def __init__(self, scaffolder, linter, guard, generator):
        self.scaffolder = scaffolder
        self.linter = linter
        self.guard = guard
        self.generator = generator

    def create_service(self, base_path, name):
        return self.scaffolder.create_service(base_path, name)

    def create_module(self, modules_path, name):
        return self.generator.generate(modules_path, name)
