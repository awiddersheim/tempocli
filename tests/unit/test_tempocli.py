import copy

import pytest

from tempocli.cli import cli
from tests.helpers import write_yaml


def test_tempocli(cli_runner):
    result = cli_runner.invoke(cli)
    assert result.exit_code == 0
    assert 'Usage:' in result.output


@pytest.mark.freeze_time('2018-08-05')
class TestTempoCliCreate(object):
    data = {
        'author': 'foo',
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

    def invoke(self, runner, config, template):
        return runner.invoke(
            cli,
            [
                '-vvv',
                '--config',
                config,
                'create',
                '--template',
                template,
            ],
        )

    def test_create_single(self, cli_runner, config, template, template_data, tempo_request):
        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = self.invoke(cli_runner, config, template)

        assert result.exit_code == 0
        assert not result.output
        assert request.called_once
        assert request.last_request.json() == {
            'authorUsername': 'foo',
            'issueKey': self.data['issues'][0]['issue'],
            'timeSpentSeconds': 1800,
            'startDate': '2018-08-05',
            'startTime': self.data['issues'][0]['start_time'],
            'description': 'Working on issue {}'.format(self.data['issues'][0]['issue']),
        }

    def test_create_multiple(self, cli_runner, config, template, template_data, tempo_request):
        template_data['issues'].append({
            'issue': 'INT-10',
            'time_spent': '30m',
            'start_time': '09:30:00',
        })

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = self.invoke(cli_runner, config, template)

        assert result.exit_code == 0
        assert not result.output
        assert request.call_count == 2

    def test_create_author_override(self, cli_runner, config, template, template_data, tempo_request):
        template_data['issues'][0]['author'] = 'bar'

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = self.invoke(cli_runner, config, template)

        assert result.exit_code == 0
        assert not result.output
        assert request.called_once
        assert request.last_request.json()['authorUsername'] == template_data['issues'][0]['author']

    def test_create_extras_override(self, cli_runner, config, template, template_data, tempo_request):
        template_data['issues'][0]['extras'] = {
            'authorUsername': 'bar',
        }

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = self.invoke(cli_runner, config, template)

        assert result.exit_code == 0
        assert not result.output
        assert request.called_once
        assert request.last_request.json()['authorUsername'] == template_data['issues'][0]['extras']['authorUsername']

    def test_create_future_date(self, cli_runner, config, template, template_data, tempo_request):
        template_data['issues'][0]['start_time'] = 'Monday at 11am'

        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs')

        result = self.invoke(cli_runner, config, template)

        assert result.exit_code == 0
        assert not result.output
        assert request.called_once
        assert request.last_request.json()['startDate'] == '2018-08-06'
        assert request.last_request.json()['startTime'] == '11:00:00'

    def test_create_http_error(self, cli_runner, config, template, template_data, tempo_request):
        write_yaml(template, template_data)

        request = tempo_request.post('/worklogs', status_code=500)

        result = self.invoke(cli_runner, config, template)

        assert 'Could not create (\'foo\', \'INT-8\',' in result.output
        assert 'Traceback' in result.output
        assert result.exit_code == 1
        assert request.called_once
