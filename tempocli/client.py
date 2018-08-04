from tempocli.requests import FuturesSession


class TempoClient(FuturesSession):
    def __init__(self, base_url, token, **kwargs):
        self.token = token

        super().__init__(base_url, **kwargs)

        self.headers['Authorization'] = 'Bearer {}'.format(self.token)
