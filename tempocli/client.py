from tempocli.requests import FuturesSession
from urllib3.util import Retry

DEFAULT_TEMPO_BASE_URL = 'https://api.tempo.io/core/3'


class TempoClient(FuturesSession):
    def __init__(self, token, base_url=DEFAULT_TEMPO_BASE_URL, max_retries=10, **kwargs):
        self.token = token
        self.max_retries = max_retries

        kwargs.setdefault('adapter_kwargs', {})

        if self.max_retries:
            kwargs['adapter_kwargs']['max_retries'] = Retry(
                total=self.max_retries,
                backoff_factor=0.1,
                method_whitelist=frozenset([
                    'HEAD',
                    'TRACE',
                    'GET',
                    'POST',
                    'PUT',
                    'OPTIONS',
                    'DELETE',
                ]),
                status_forcelist=[429],
            )

        super().__init__(base_url, **kwargs)

        self.headers['Authorization'] = 'Bearer {}'.format(self.token)
