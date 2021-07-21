from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AVpfZG9llVun2lpUbvT3TkMArQGmiHqinQ_y9H-hsV56bpkJz6sv5Y0IbPpDxSurQsPC4rAcF6JUXQVE"
        self.client_secret = "EIpxt_LgP5Ofy93IYWJm_eNmag8ntV6LrGLayqDlnLjdvWf4FM1G6WbVgz6t831S8Trq5VBKAGIfwTI-"

        

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        self.client = PayPalHttpClient(self.environment)