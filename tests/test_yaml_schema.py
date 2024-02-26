import asdf
import pytest
from asdf.exceptions import ValidationError
from common import YAML_SCHEMA_PATH, assert_yaml_header_and_footer, list_schema_paths, load_yaml


@pytest.mark.parametrize("path", list_schema_paths(YAML_SCHEMA_PATH))
def test_yaml_schema(path):
    assert_yaml_header_and_footer(path)

    # Asserting no exceptions here
    load_yaml(path)


@pytest.mark.parametrize("path", YAML_SCHEMA_PATH.glob("*.yaml"))
def test_nested_object_validation(path):
    """
    Test that the validations are applied to nested objects.
    """
    metaschema = load_yaml(path)
    validator = asdf.schema.get_validator(schema=metaschema)

    schema = {"$schema": metaschema["id"], "type": "object", "properties": {"foo": {"flowStyle": "block"}}}
    # No error here
    validator.validate(schema)

    schema = {"$schema": metaschema["id"], "type": "object", "properties": {"foo": {"flowStyle": "funky"}}}
    with pytest.raises(ValidationError, match="'funky' is not one of"):
        validator.validate(schema)

    schema = {
        "$schema": metaschema["id"],
        "type": "array",
        "items": {"type": "object", "properties": {"foo": {"propertyOrder": "a,b,c,d"}}},
    }
    with pytest.raises(ValidationError):
        validator.validate(schema)
