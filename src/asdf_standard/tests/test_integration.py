from pathlib import Path

import asdf
import pytest
import yaml


def get_resources():
    resources_root = Path(__file__).parent.parent.parent.parent / "resources"

    return {str(path.relative_to(resources_root)): path for path in resources_root.glob("**/*.yaml")}


RESOURCES = get_resources()


@pytest.mark.parametrize("resource", RESOURCES)
def test_resource(resource):
    resource_path = RESOURCES[resource]
    resource_manager = asdf.get_config().resource_manager

    with resource_path.open("rb") as f:
        resource_content = f.read()
    resource = yaml.safe_load(resource_content)

    if "version_map" not in str(resource_path.stem):
        resource_uri = resource["id"]
        assert resource_manager[resource_uri] == resource_content


def get_manifests():
    manifests_root = Path(__file__).parent.parent.parent.parent / "resources" / "manifests" / "asdf-format.org"

    return {str(path.relative_to(manifests_root)): path for path in manifests_root.glob("**/*.yaml")}


MANIFESTS = get_manifests()


@pytest.mark.parametrize("manifest", MANIFESTS)
def test_manifest(manifest):
    manifest_path = MANIFESTS[manifest]
    resource_manager = asdf.get_config().resource_manager

    with manifest_path.open("rb") as f:
        manifest_content = f.read()
    manifest = yaml.safe_load(manifest_content)

    manifest_schema = asdf.schema.load_schema("asdf://asdf-format.org/core/schemas/extension_manifest-1.0.0")

    # The manifest must be valid against its own schema:
    asdf.schema.validate(manifest, schema=manifest_schema)

    for tag_definition in manifest["tags"]:
        # The tag's schema must be available:
        assert tag_definition["schema_uri"] in resource_manager
