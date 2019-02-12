import pytest

from tempocli.funcs import parse_short_time
from tempocli.funcs import TIME_UNITS


def test_parse_short_time():
    assert parse_short_time('30s') == 30
    assert parse_short_time('30m') == 30 * 60
    assert parse_short_time('30h') == 30 * 60 * 60


def test_parse_short_time_invalid():
    with pytest.raises(
        ValueError,
        match=r'Could not parse time, allowed units \({}\)'.format(
            ', '.join(TIME_UNITS.keys()),
        ),
    ):
        assert parse_short_time('30days')
