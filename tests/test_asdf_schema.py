import pytest

from jsonschema import ValidationError

from common import load_yaml, SCHEMAS_PATH, assert_yaml_header_and_footer


@pytest.mark.parametrize("path", SCHEMAS_PATH.glob("asdf-schema-*.yaml"))
def test_asdf_schema(path):
    assert_yaml_header_and_footer(path)

    # Asserting no exceptions here
    load_yaml(path)


@pytest.mark.parametrize("path", SCHEMAS_PATH.glob("asdf-schema-*.yaml"))
def test_nested_object_validation(path, create_validator):
    """
    Test that the validations are applied to nested objects.
    """
    metaschema = load_yaml(path)
    validator = create_validator(metaschema)

    schema = {
        "$schema": metaschema["id"],
        "type": "object",
        "properties": {
            "foo": {
                "datatype": "float32",
            },
        },
    }
    # No error here
    validator.validate(schema)

    schema = {
        "$schema": metaschema["id"],
        "type": "object",
        "properties": {
            "foo": {
                "datatype": "banana",
            },
        },
    }
    with pytest.raises(ValidationError, match="'banana' is not valid"):
        validator.validate(schema)

    schema = {
        "$schema": metaschema["id"],
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "foo": {
                    "ndim": "twelve",
                },
            },
        },
    }
    with pytest.raises(ValidationError):
        validator.validate(schema)
