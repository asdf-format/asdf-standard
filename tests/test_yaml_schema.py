import pytest

from common import load_yaml, YAML_SCHEMA_PATH, list_schema_paths, assert_yaml_header_and_footer


@pytest.mark.parametrize("path", list_schema_paths(YAML_SCHEMA_PATH))
def test_yaml_schema(path):
    assert_yaml_header_and_footer(path)

    # Asserting no exceptions here
    load_yaml(path)
