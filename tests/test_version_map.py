import re

import pytest
from common import (
    VALID_FILE_FORMAT_VERSIONS,
    VALID_YAML_VERSIONS,
    VERSION_MAP_PATHS,
    assert_yaml_header_and_footer,
    is_deprecated,
    load_yaml,
    path_to_id,
    split_id,
)
from packaging.version import Version

VALID_FILENAME_RE = re.compile(r"version_map-[0-9]+\.[0-9]+\.[0-9]+\.yaml")

SORTED_PATHS = sorted(VERSION_MAP_PATHS, key=lambda p: Version(split_id(path_to_id(p))[1]))

LATEST_PATH = SORTED_PATHS[-1]


@pytest.mark.parametrize("path", VERSION_MAP_PATHS)
def test_version_map(path):
    assert VALID_FILENAME_RE.match(path.name) is not None, f"{path.name} is an invalid version map filename"

    assert_yaml_header_and_footer(path)

    vm = load_yaml(path)

    assert set(vm.keys()) == {"FILE_FORMAT", "YAML_VERSION", "tags"}

    assert vm["FILE_FORMAT"] in VALID_FILE_FORMAT_VERSIONS
    assert vm["YAML_VERSION"] in VALID_YAML_VERSIONS

    assert len(vm["tags"].keys()) == len(set(vm["tags"].keys())), f"{path.name} contains duplicate tags"

    sorted_tags = sorted(list(vm["tags"].keys()))
    if sorted_tags != list(vm["tags"].keys()):
        sorted_list = "\n".join([f"""{tag}: {vm["tags"][tag]}""" for tag in sorted_tags])
        message = f"{path.name} tag list is not sorted.  Try this order instead:\n{sorted_list}"
        assert False, message


@pytest.mark.skip
@pytest.mark.parametrize("path, previous_path", zip(SORTED_PATHS[1:], SORTED_PATHS[0:-1]))
def test_version_map_tags_retained(path, previous_path):
    """
    Confirm that non-deprecated tags were not lost between
    successive version maps.
    """
    vm = load_yaml(path)
    prev_vm = load_yaml(previous_path)

    expected_tags = {t for t in prev_vm["tags"].keys() if not is_deprecated(t)}
    tags = set(vm["tags"].keys())
    if not expected_tags.issubset(tags):
        missing_tags = expected_tags - tags
        assert False, (
            f"{path.name} is missing schemas that were present in the "
            "previous version.  If this was intentional, update the deprecation "
            "list in tests/common.py, otherwise add the following missing schemas: "
            f"""{", ".join(missing_tags)}"""
        )
