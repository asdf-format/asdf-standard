"""
The transform schemas are deprecated, but we need to continue testing them
to ensure that older versions of the standard are supported.
"""
import pytest
from common import SCHEMAS_PATH, list_latest_schema_paths, list_schema_paths, load_yaml

SCHEMA_PATHS = [p for p in list_schema_paths(SCHEMAS_PATH / "transform")]
LATEST_SCHEMA_PATHS = [p for p in list_latest_schema_paths(SCHEMAS_PATH / "transform")]

BASE_SCHEMA_PATHS = [p for p in SCHEMA_PATHS if p.name.startswith("transform-")]
IMPL_SCHEMA_PATHS = [p for p in SCHEMA_PATHS if not p.name.startswith("transform-")]

REFS = {p.stem for p in SCHEMA_PATHS}


@pytest.mark.parametrize("path", IMPL_SCHEMA_PATHS)
def test_transform(path, assert_schema_correct):
    assert_schema_correct(path)

    if path.name != "domain-1.0.0.yaml":
        schema = load_yaml(path)

        message = f"{path.name} must include a base or other transform schema"
        if "allOf" in schema:
            assert any("$ref" in c and c["$ref"] in REFS for c in schema["allOf"]), message
        elif "$ref" in schema:
            assert schema["$ref"] in REFS, message
        else:
            assert False, message


@pytest.mark.parametrize("path", BASE_SCHEMA_PATHS)
def test_transform_base(path, assert_schema_correct):
    assert_schema_correct(path)


@pytest.mark.parametrize("path", LATEST_SCHEMA_PATHS)
def test_transform_latest(path, assert_latest_schema_correct):
    assert_latest_schema_correct(path)
