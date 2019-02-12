import copy

import pytest

from tempocli.cli import cli
from tempocli.cli import ENVVAR_PREFIX
from tests.helpers import write_yaml


def test_tempocli(cli_runner):
    result = cli_runner.invoke(cli)
    assert result.exit_code == 0
    assert 'Usage:' in result.output


@pytest.mark.freeze_time('2018-08-05')
class TestTempoCliCreate(object):
    data = {
        'author_account_id': 'foo',
        'issues': [
            {
                'issue': 'INT-8',
                'time_spent': '30m',
                'start_time': '09:30:00',
            },
        ],
    }

    @pytest.fixture
    def template_data(self):
        return copy.deepcopy(self.data)

    @pytest.fixture
    def template(self, tmpdir):
        return tmpdir.join('template.yml')

    @pytest.fixture
    def template_invoke(self, cli_invoke, config, template):
        _args = [
            '-vvv',
            '--config',
            config.strpath,
            'create',
            '--template',
            template.strpath,
        ]

        def func(args=None, **kwargs):
            _args.extend(args or [])

            return cli_invoke(cli, _args, **kwargs)

        return func

    def test_create_single(self, template, template_data, template_invoke, tempo_request):
        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = template_invoke()

        assert result.exit_code == 0
        assert request.called_once
        assert request.last_request.json() == {
            'authorAccountId': 'foo',
            'issueKey': self.data['issues'][0]['issue'],
            'timeSpentSeconds': 1800,
            'startDate': '2018-08-05',
            'startTime': self.data['issues'][0]['start_time'],
            'description': 'Working on issue {}'.format(self.data['issues'][0]['issue']),
        }

    def test_create_multiple(self, template, template_data, template_invoke, tempo_request):
        template_data['issues'].append({
            'issue': 'INT-10',
            'time_spent': '30m',
            'start_time': '09:30:00',
        })

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = template_invoke()

        assert result.exit_code == 0
        assert request.call_count == 2

    def test_create_author_override(self, template, template_data, template_invoke, tempo_request):
        template_data['issues'][0]['author_account_id'] = 'bar'

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = template_invoke()

        assert result.exit_code == 0
        assert request.called_once
        assert request.last_request.json()['authorAccountId'] == template_data['issues'][0]['author_account_id']

    def test_create_extras_override(self, template, template_data, template_invoke, tempo_request):
        template_data['issues'][0]['extras'] = {
            'authorAccountId': 'bar',
        }

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = template_invoke()

        assert result.exit_code == 0
        assert request.called_once
        assert request.last_request.json()['authorAccountId'] == template_data['issues'][0]['extras']['authorAccountId']

    def test_create_token_from_env(self, template, template_data, template_invoke, tempo_request):
        token = 'fromenv'  # noqa: S105

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = template_invoke(
            env={
                '{}_TOKEN'.format(ENVVAR_PREFIX): token,
            },
        )

        assert result.exit_code == 0
        assert request.called_once
        assert request.last_request.headers['Authorization'] == 'Bearer {}'.format(token)

    def test_create_future_date(self, template, template_data, template_invoke, tempo_request):
        template_data['issues'][0]['start_time'] = 'Monday at 11am'

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = template_invoke()

        assert result.exit_code == 0
        assert request.called_once
        assert request.last_request.json()['startDate'] == '2018-08-06'
        assert request.last_request.json()['startTime'] == '11:00:00'

    def test_create_http_error(self, template, template_data, template_invoke, tempo_request):
        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs', status_code=500)

        result = template_invoke()

        assert 'Could not create (\'foo\', \'INT-8\',' in result.output
        assert 'Traceback' in result.output
        assert result.exit_code == 1
        assert request.called_once
