class SILAOperatingSystem:
    def __init__(self, cli, sdk, portal, deployment):
        self.cli = cli
        self.sdk = sdk
        self.portal = portal
        self.deployment = deployment

    def register_service(self, name, endpoint):
        self.portal.register_service(name, endpoint)

    def list_services(self):
        return self.portal.list_services()
