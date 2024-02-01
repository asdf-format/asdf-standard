import sys

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

import asdf_standard


def get_resource_mappings():
    resources_root = importlib_resources.files("asdf_standard") / "resources"

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
        asdf_standard.DirectoryResourceMapping(
            resources_root / "manifests" / "asdf-format.org" / "unit",
            "asdf://asdf-format.org/unit/manifests/",
        ),
        asdf_standard.DirectoryResourceMapping(
            resources_root / "manifests" / "asdf-format.org" / "table",
            "asdf://asdf-format.org/table/manifests/",
        ),
        asdf_standard.DirectoryResourceMapping(
            resources_root / "manifests" / "asdf-format.org" / "time",
            "asdf://asdf-format.org/time/manifests/",
        ),
        asdf_standard.DirectoryResourceMapping(
            resources_root / "manifests" / "asdf-format.org" / "fits",
            "asdf://asdf-format.org/fits/manifests/",
        ),
    ]
