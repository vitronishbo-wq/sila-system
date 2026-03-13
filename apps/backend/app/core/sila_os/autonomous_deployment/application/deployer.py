class AutonomousDeployment:

    def __init__(

        self,
        cloud_control

    ):

        self.cloud_control = cloud_control

    def deploy(

        self,
        service,
        image

    ):

        return self.cloud_control.deploy(

            service,
            image

        )
