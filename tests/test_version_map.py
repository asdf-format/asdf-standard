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
def test_version_map(path, schema_tags):
    assert VALID_FILENAME_RE.match(path.name) is not None, f"{path.name} is an invalid version map filename"

    assert_yaml_header_and_footer(path)

    vm = load_yaml(path)

    assert set(vm.keys()) == {"FILE_FORMAT", "YAML_VERSION", "tags"}

    assert vm["FILE_FORMAT"] in VALID_FILE_FORMAT_VERSIONS
    assert vm["YAML_VERSION"] in VALID_YAML_VERSIONS

    for tag_base, tag_version in vm["tags"].items():
        tag = f"{tag_base}-{tag_version}"
        if "time" not in tag and "core" not in tag:
            assert tag in schema_tags, f"{path.name} specifies missing tag {tag}"

    assert len(vm["tags"].keys()) == len(set(vm["tags"].keys())), f"{path.name} contains duplicate tags"

    sorted_tags = sorted(list(vm["tags"].keys()))
    if sorted_tags != list(vm["tags"].keys()):
        sorted_list = "\n".join([f"""{tag}: {vm["tags"][tag]}""" for tag in sorted_tags])
        message = f"{path.name} tag list is not sorted.  Try this order instead:\n{sorted_list}"
        assert False, message


def test_latest_version_map(latest_schema_tags):
    """
    The current latest version map has some special requirements.
    """
    vm = load_yaml(LATEST_PATH)

    tag_base_to_version = dict([tag.rsplit("-", 1) for tag in latest_schema_tags])

    expected_tag_bases = set([t for t in tag_base_to_version.keys() if not is_deprecated(t)])
    vm_tag_bases = set(vm["tags"].keys())
    if not expected_tag_bases.issubset(vm_tag_bases):
        missing_tag_bases = expected_tag_bases - vm_tag_bases
        insert_list = "\n".join(
            sorted(f"""{tag_base}-{tag_base_to_version[tag_base]}""" for tag_base in missing_tag_bases)
        )
        message = (
            f"{LATEST_PATH.name} must include the latest version of "
            "every non-deprecated schema with a tag.  Update the deprecation "
            "list in tests/common.py, or add the following missing schemas: \n"
            f"{insert_list}"
        )
        assert False, message

    incorrect_tag_bases = sorted([tag for tag in expected_tag_bases if vm["tags"][tag] != tag_base_to_version[tag]])
    if len(incorrect_tag_bases) > 0:
        update_list = "\n".join(
            [f"""{tag}: {vm["tags"][tag]} --> {tag_base_to_version[tag]}""" for tag in incorrect_tag_bases]
        )
        message = (
            f"{LATEST_PATH.name} must include the latest version of "
            "every non-deprecated schema with a tag.  Update the following: \n"
            f"{update_list}"
        )
        assert False, message


@pytest.mark.parametrize("path, previous_path", zip(SORTED_PATHS[1:], SORTED_PATHS[0:-1]))
def test_version_map_tags_retained(path, previous_path):
    """
    Confirm that non-deprecated tags were not lost between
    successive version maps.
    """
    vm = load_yaml(path)
    prev_vm = load_yaml(previous_path)

    expected_tags = set([t for t in prev_vm["tags"].keys() if not is_deprecated(t)])
    tags = set(vm["tags"].keys())
    if not expected_tags.issubset(tags):
        missing_tags = expected_tags - tags
        assert False, (
            f"{path.name} is missing schemas that were present in the "
            "previous version.  If this was intentional, update the deprecation "
            "list in tests/common.py, otherwise add the following missing schemas: "
            f"""{", ".join(missing_tags)}"""
        )
