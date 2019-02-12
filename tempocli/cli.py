import os
import sys
import traceback

import arrow
import click
import dateutil.parser

from tempocli.client import TempoClient
from tempocli.funcs import get_env_opt
from tempocli.funcs import load_yaml
from tempocli.funcs import parse_short_time
from tqdm import tqdm


ENVVAR_PREFIX = 'TEMPOCLI'


class Tempo(object):
    def __init__(self, config, client, verbose):
        self.config = config
        self.client = client
        self.verbose = verbose


def common_template_options(f):
    f = click.option(
        '-t',
        '--template',
        help='Path to template file.',
        envvar='TEMPLATE',
        default='tempo_template.yml',
        type=click.Path(
            exists=True,
            dir_okay=False,
            resolve_path=True,
        ),
        show_default=True,
    )(f)

    return f


@click.group()
@click.version_option()
@click.option(
    '-c',
    '--config',
    help='Path to configuration file.',
    envvar='CONFIG',
    show_envvar=True,
    default=os.path.expanduser('~/.tempocli.yml'),
    type=click.Path(
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    show_default=True,
)
@click.option(
    '-v',
    '--verbose',
    help='Verbose output.',
    envvar='VERBOSE',
    show_envvar=True,
    count=True,
)
@click.option(
    '-r',
    '--max-retries',
    help='Max number of retries to perfom for failed requests. Setting to 0 disables retries.',
    envvar='MAX_RETRIES',
    default=10,
    show_default=True,
    type=int,
)
@click.option(
    '-w',
    '--workers',
    help='Number of workers to spawn.',
    envvar='WORKERS',
    show_envvar=True,
    default=10,
    show_default=True,
    type=int,
)
@click.pass_context
def cli(ctx, config, max_retries, workers, verbose):
    """Interact with Tempo time tracking from the command line."""

    config = load_yaml(config)

    token = get_env_opt('TOKEN')

    if token:
        config['token'] = token

    client = TempoClient(
        token=config['token'],
        max_workers=workers,
        max_retries=max_retries,
    )

    ctx.obj = Tempo(
        config=config,
        client=client,
        verbose=verbose,
    )


@cli.command()
@common_template_options
@click.pass_obj
def create(tempo, template):
    """Create worklogs from template."""

    futures = []
    error = False

    temp = load_yaml(template)

    for issue in temp['issues']:
        start = arrow.Arrow.fromdatetime(
            dateutil.parser.parse(issue['start_time']),
        )

        data = {
            'issueKey': issue['issue'],
            'timeSpentSeconds': parse_short_time(issue['time_spent']),
            'startDate': start.format('YYYY-MM-DD'),
            'startTime': start.format('HH:mm:ss'),
            'description': issue.get(
                'description',
                'Working on issue {}'.format(issue['issue']),
            ),
            'authorAccountId': issue.get('author_account_id', temp['author_account_id']),
        }

        # NOTE(awiddersheim): Load in any extra data overriding base
        # giving some flexibility to what can be created.
        data.update(issue.get('extras') or {})

        future = tempo.client.post_future(
            '/worklogs',
            json=data,
        )

        future.issue = (
            data['authorAccountId'],
            data['issueKey'],
            data['startDate'],
            data['startTime'],
        )

        futures.append(future)

    for future in tqdm(
        tempo.client.as_completed(futures),
        desc='Adding worklogs',
        total=len(futures),
        ncols=100,
    ):
        try:
            response = future.result()
            response.raise_for_status()
        except Exception as e:
            click.echo(
                'Could not create {}: {}'.format(
                    future.issue,
                    str(e),
                ),
                err=True,
            )

            if tempo.verbose:
                click.echo(traceback.format_exc(), err=True)

            error = True

    if error:
        sys.exit(1)


def main():  # pragma: no cover
    cli(
        auto_envvar_prefix=ENVVAR_PREFIX,
        prog_name='tempocli',
    )
