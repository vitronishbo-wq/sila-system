class SILACommandLine:

    def __init__(self, dev_platform, cloud_control):

        self.dev_platform = dev_platform
        self.cloud_control = cloud_control

    def create_service(self, name):

        return self.dev_platform.create_service(

            "modules",
            name

        )

    def deploy_service(

        self,
        service,
        image

    ):

        return self.cloud_control.deploy(

            service,
            image

        )
