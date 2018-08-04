import concurrent.futures
import urllib.parse

import requests
import requests_futures.sessions


class FuturesSession(requests_futures.sessions.FuturesSession):
    def __init__(self, base_url, **kwargs):
        self.base_url = base_url

        super().__init__(**kwargs)

        self.headers['User-Agent'] = '{} {}'.format(
            'tempocli',
            self.headers['User-Agent'],
        )

        # NOTE(awiddersheim): Assign the session to the current object
        # instance so that subclassed methods like `request()` get
        # called properly.
        self.session = self

    def request(self, method, url, *args, **kwargs):
        url = self.urljoin(url)

        return requests.Session.request(self, method, url, *args, **kwargs)

    def request_future(self, *args, **kwargs):
        # NOTE(awiddersheim): This will actually call the subclassed
        # `request()` method since `self.session` is assigned to the
        # instance of this object.
        return super().request(*args, **kwargs)

    def get_future(self, *args, **kwargs):
        return self.request_future('GET', *args, **kwargs)

    def options_future(self, *args, **kwargs):
        return self.request_future('OPTIONS', *args, **kwargs)

    def head_future(self, *args, **kwargs):
        return self.request_future('HEAD', *args, **kwargs)

    def post_future(self, *args, **kwargs):
        return self.request_future('POST', *args, **kwargs)

    def put_future(self, *args, **kwargs):
        return self.request_future('PUT', *args, **kwargs)

    def patch_future(self, *args, **kwargs):
        return self.request_future('PATCH', *args, **kwargs)

    def delete_future(self, *args, **kwargs):
        return self.request_future('DELETE', *args, **kwargs)

    @staticmethod
    def as_completed(*args, **kwargs):
        return concurrent.futures.as_completed(*args, **kwargs)

    @staticmethod
    def wait(*args, **kwargs):
        return concurrent.futures.wait(*args, **kwargs)

    def urljoin(self, path):
        return urllib.parse.urljoin(
            '{}/'.format(self.base_url.rstrip('/')),
            path.lstrip('/'),
        )
