import asdf
import pytest
from common import MANIFESTS_PATH, RESOURCES_PATH, load_yaml

MANIFEST_PATHS = sorted(MANIFESTS_PATH.glob("*.yaml"))
MANIFEST_SCHEMA_PATH = RESOURCES_PATH / "schemas" / "asdf-format.org" / "core" / "extension_manifest-1.0.0.yaml"
MANIFEST_SCHEMA_ID = "asdf://asdf-format.org/core/schemas/extension_manifest-1.0.0"


@pytest.mark.parametrize("path", MANIFEST_PATHS)
def test_manifest(path):
    manifest = load_yaml(path)

    with asdf.config_context() as config:
        config.add_resource_mapping({MANIFEST_SCHEMA_ID: MANIFEST_SCHEMA_PATH.read_bytes()})

        manifest_schema = asdf.schema.load_schema(MANIFEST_SCHEMA_ID)
        asdf.schema.validate(manifest, schema=manifest_schema)

    assert "title" in manifest
    assert "description" in manifest

    for tag in manifest["tags"]:
        assert "title" in tag
        assert "description" in tag
