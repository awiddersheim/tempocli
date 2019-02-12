from tempocli.requests import FuturesSession

DEFAULT_TEMPO_BASE_URL = 'https://api.tempo.io/core/3/worklogs'


class TempoClient(FuturesSession):
    def __init__(self, token, base_url=DEFAULT_TEMPO_BASE_URL, **kwargs):
        self.token = token

        super().__init__(base_url, **kwargs)

        self.headers['Authorization'] = 'Bearer {}'.format(self.token)
