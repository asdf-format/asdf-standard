import pytest

from common import SCHEMAS_PATH, list_schema_paths, list_latest_schema_paths


@pytest.mark.parametrize("path", list_schema_paths(SCHEMAS_PATH / "fits"))
def test_fits(path, assert_schema_correct):
    assert_schema_correct(path)


@pytest.mark.parametrize("path", list_latest_schema_paths(SCHEMAS_PATH / "fits"))
def test_fits_latest(path, assert_latest_schema_correct):
    assert_latest_schema_correct(path)
