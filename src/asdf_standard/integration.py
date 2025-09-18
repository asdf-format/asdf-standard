import importlib.resources as importlib_resources

import asdf_standard
from asdf_standard._versioning import get_unstable_supported


def get_resource_mappings():
    resources_root = importlib_resources.files("asdf_standard") / "resources"

    resources = [
        asdf_standard.DirectoryResourceMapping(
            resources_root / "stable" / "schemas" / "stsci.edu", "http://stsci.edu/schemas/", recursive=True
        ),
        asdf_standard.DirectoryResourceMapping(
            resources_root / "stable" / "schemas" / "asdf-format.org" / "core", "asdf://asdf-format.org/core/schemas/"
        ),
        asdf_standard.DirectoryResourceMapping(
            resources_root / "stable" / "manifests" / "asdf-format.org" / "core",
            "asdf://asdf-format.org/core/manifests/",
        ),
        asdf_standard.DirectoryResourceMapping(
            resources_root / "stable" / "manifests" / "asdf-format.org" / "astronomy",
            "asdf://asdf-format.org/astronomy/manifests/",
        ),
    ]

    if get_unstable_supported():
        # TODO register dev resources and warn?
        resources.extend(
            [
                asdf_standard.DirectoryResourceMapping(
                    resources_root / "unstable" / "schemas" / "stsci.edu", "http://stsci.edu/schemas/", recursive=True
                ),
                # asdf_standard.DirectoryResourceMapping(
                #     resources_root / "dev" / "schemas" / "asdf-format.org" / "core", "asdf://asdf-format.org/core/schemas/"
                # ),
                asdf_standard.DirectoryResourceMapping(
                    resources_root / "unstable" / "manifests" / "asdf-format.org" / "core",
                    "asdf://asdf-format.org/core/manifests/",
                ),
                # asdf_standard.DirectoryResourceMapping(
                #     resources_root / "dev" / "manifests" / "asdf-format.org" / "astronomy",
                #     "asdf://asdf-format.org/astronomy/manifests/",
                # ),
            ]
        )

    return resources
