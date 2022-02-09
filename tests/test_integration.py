from pathlib import Path

import asdf
import yaml


def test_resources():
    resources_root = Path(__file__).parent.parent / "resources"
    resource_manager = asdf.get_config().resource_manager

    for resource_path in resources_root.glob("**/*.yaml"):
        with resource_path.open("rb") as f:
            resource_content = f.read()
        resource = yaml.safe_load(resource_content)

        if "version_map" not in str(resource_path.stem):
            resource_uri = resource["id"]
            assert resource_manager[resource_uri] == resource_content


def test_manifests():
    manifests_root = Path(__file__).parent.parent / "resources" / "manifests" / "asdf-format.org"
    resource_manager = asdf.get_config().resource_manager

    for manifest_path in manifests_root.glob("*.yaml"):
        with manifest_path.open("rb") as f:
            manifest_content = f.read()
        manifest = yaml.safe_load(manifest_content)

        manifest_schema = asdf.schema.load_schema("asdf://asdf-format.org/core/schemas/extension_manifest-1.0.0")

        # The manifest must be valid against its own schema:
        asdf.schema.validate(manifest, schema=manifest_schema)

        for tag_definition in manifest["tags"]:
            # The tag's schema must be available:
            assert tag_definition["schema_uri"] in resource_manager
