import os

import pytest
from asdf import open as asdf_open
from asdf import versioning
from asdf._tests._helpers import assert_tree_match

_REFFILE_PATH = os.path.join(os.path.dirname(__file__), "..", "reference_files")


def get_test_id(reference_file_path):
    """Helper function to return the informative part of a schema path"""
    path = os.path.normpath(str(reference_file_path))
    return os.path.sep.join(path.split(os.path.sep)[-3:])


def collect_reference_files():
    """Function used by pytest to collect ASDF reference files for testing."""
    for version in versioning.supported_versions:
        version_dir = os.path.join(_REFFILE_PATH, str(version))
        if os.path.exists(version_dir):
            for filename in os.listdir(version_dir):
                if filename.endswith(".asdf"):
                    filepath = os.path.join(version_dir, filename)
                    basename, _ = os.path.splitext(filepath)
                    if os.path.exists(basename + ".yaml"):
                        yield filepath


def _compare_trees(name_without_ext):
    asdf_path = name_without_ext + ".asdf"
    yaml_path = name_without_ext + ".yaml"

    with asdf_open(asdf_path) as af_handle:
        af_handle.resolve_references()

        with asdf_open(yaml_path) as ref:
            assert_tree_match(af_handle.tree, ref.tree)


def test_reference_files_exist():
    assert list(collect_reference_files())


@pytest.mark.parametrize("reference_file", collect_reference_files(), ids=get_test_id)
def test_reference_file(reference_file):
    name_without_ext, _ = os.path.splitext(reference_file)
    _compare_trees(name_without_ext)
