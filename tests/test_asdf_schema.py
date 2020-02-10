import pytest

from common import load_yaml, SCHEMAS_PATH, assert_yaml_header_and_footer


@pytest.mark.parametrize("path", SCHEMAS_PATH.glob("asdf-schema-*.yaml"))
def test_asdf_schema(path):
    assert_yaml_header_and_footer(path)

    # Asserting no exceptions here
    load_yaml(path)
