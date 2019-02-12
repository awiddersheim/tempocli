import pytest
import requests_mock

from tempocli.cli import ENVVAR_PREFIX
from tempocli.client import TempoClient
from tests.helpers import write_yaml


@pytest.fixture
def config(tmpdir):
    config = tmpdir.join('config.yml')

    write_yaml(
        config,
        {
            'token': 'foo',
        },
    )

    return config


@pytest.fixture
def tempo_client():
    return TempoClient(token='foo')  # noqa: S106


@pytest.fixture
def tempo_request(tempo_client):
    class CustomAdapter(requests_mock.adapter.Adapter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.complete_qs = True

        def register_uri(self, method, url, **kwargs):
            if isinstance(url, str):
                url = tempo_client.urljoin(url)

            kwargs.setdefault('complete_qs', self.complete_qs)

            return super().register_uri(method, url, **kwargs)

    with requests_mock.Mocker(adapter=CustomAdapter()) as mock:
        yield mock


@pytest.fixture
def cli_invoke(cli_runner):
    def func(*args, **kwargs):
        kwargs.setdefault('auto_envvar_prefix', ENVVAR_PREFIX)

        return cli_runner.invoke(*args, **kwargs)

    return func
