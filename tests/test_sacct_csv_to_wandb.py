from io import StringIO

import pytest
from src.sacct_csv_to_wandb import construct_df


@pytest.fixture
def csv_input():
    file = open("tests/empty_sacct_job.csv")
    content = file.read()
    string = StringIO(content)
    return string


def test_df_construction(csv_input):
    df = construct_df(csv_input)
    assert df is not None
