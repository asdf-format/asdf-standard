import sys

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

import asdf_standard


def get_resource_mappings():
    resources_root = importlib_resources.files(asdf_standard) / "resources"
    if not resources_root.is_dir():
        raise RuntimeError("Missing resources directory")

    return [
        asdf_standard.DirectoryResourceMapping(
            resources_root / "schemas" / "stsci.edu", "http://stsci.edu/schemas/", recursive=True
        ),
        asdf_standard.DirectoryResourceMapping(
            resources_root / "schemas" / "asdf-format.org" / "core", "asdf://asdf-format.org/core/schemas/"
        ),
        asdf_standard.DirectoryResourceMapping(
            resources_root / "manifests" / "asdf-format.org" / "core",
            "asdf://asdf-format.org/core/manifests/",
        ),
    ]
