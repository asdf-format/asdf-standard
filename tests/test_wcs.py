"""
The WCS schemas are deprecated, but we need to continue testing them
to ensure that older versions of the standard are supported.
"""
import pytest

from common import SCHEMAS_PATH, list_schema_paths, list_latest_schema_paths


@pytest.mark.parametrize("path", list_schema_paths(SCHEMAS_PATH / "wcs"))
def test_wcs(path, assert_schema_correct):
    assert_schema_correct(path)


@pytest.mark.parametrize("path", list_latest_schema_paths(SCHEMAS_PATH / "wcs"))
def test_wcs_latest(path, assert_latest_schema_correct):
    assert_latest_schema_correct(path)
