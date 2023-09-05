import pytest
from common import SCHEMAS_PATH, list_latest_schema_paths, list_schema_paths


@pytest.mark.parametrize("path", list_schema_paths(SCHEMAS_PATH / "time"))
def test_time(path, assert_schema_correct):
    assert_schema_correct(path)


@pytest.mark.parametrize("path", list_latest_schema_paths(SCHEMAS_PATH / "time"))
def test_time_latest(path, assert_latest_schema_correct):
    assert_latest_schema_correct(path)
