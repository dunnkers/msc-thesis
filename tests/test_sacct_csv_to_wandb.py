from io import StringIO

import pytest
from src.sacct_csv_to_wandb import (
    construct_df,
    parse_duration_string,
    parse_memory_string,
)


def test_parse_duration_str():
    duration = parse_duration_string(None)
    assert duration is None

    duration = parse_duration_string("01:00:00")
    assert duration == 3600

    duration = parse_duration_string("1-00:00:00")
    assert duration == 86400

    duration = parse_duration_string("0-00:00:00.234")
    assert duration == 0.000234


def test_parse_memory_string():
    memory = parse_memory_string(None)
    assert memory is None

    memory = parse_memory_string("1000K")
    assert memory == 1

    memory = parse_memory_string("1G")
    assert memory == 1000


@pytest.fixture
def csv_input():
    file = open("tests/empty_sacct_job.csv")
    content = file.read()
    string = StringIO(content)
    return string


def test_empty_df_construction(csv_input):
    df = construct_df(csv_input)
    assert df is not None
