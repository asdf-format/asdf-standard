import pytest
from common import ROOT_PATH

from asdf_standard import _versioning


@pytest.mark.parametrize("version_type", ["stable", "unstable"])
def test_supported_versions_match_manifests(version_type):
    """Test that versions in versioning.*_core_schema_versions match the manifests"""
    MANIFESTS_PATH = ROOT_PATH / "resources" / version_type / "manifests" / "asdf-format.org" / "core"
    for version in getattr(_versioning, f"{version_type}_core_schema_versions"):
        assert (MANIFESTS_PATH / f"core-{version}.yaml").exists()
