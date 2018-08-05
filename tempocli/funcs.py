import re

import click
import yaml


TIME_UNITS = {
    's': 1,
    'm': 60,
    'h': 3600,
    'd': 86400,
}

TIME_REGEX = re.compile(
    '^(?P<time>\d+)(?P<unit>({}))$'.format(
        '|'.join(TIME_UNITS.keys()),
    ),
)


def load_yaml(path):
    with click.open_file(path) as f:
        return yaml.safe_load(f.read())


def parse_short_time(time):
    match = TIME_REGEX.match(time)

    if not match:
        raise ValueError(
            'Could not parse time, allowed units ({})'.format(
                ', '.join(TIME_UNITS),
            ),
        )

    data = match.groupdict()

    return int(data['time']) * TIME_UNITS[data['unit']]
