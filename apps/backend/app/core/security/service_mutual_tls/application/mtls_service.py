import ssl


class MutualTLSService:

    def __init__(self, certfile, keyfile, cafile):

        self.certfile = certfile
        self.keyfile = keyfile
        self.cafile = cafile

    def create_context(self):

        context = ssl.create_default_context(
            ssl.Purpose.CLIENT_AUTH,
            cafile=self.cafile
        )

        context.load_cert_chain(

            certfile=self.certfile,
            keyfile=self.keyfile,

        )

        context.verify_mode = ssl.CERT_REQUIRED

        return context
