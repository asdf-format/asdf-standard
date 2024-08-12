import os

import asdf
import numpy as np
import pytest

_REFFILE_PATH = os.path.join(os.path.dirname(__file__), "..", "reference_files")


def assert_tree_match(tree_a, tree_b):
    seen = set()

    def walk_trees(a, b):
        seen_key = (id(a), id(b))

        if seen_key in seen:
            return

        seen.add(seen_key)

        assert isinstance(a, type(b))
        if isinstance(a, dict):
            assert set(a.keys()) == set(b.keys())
            for k in a:
                walk_trees(a[k], b[k])
        elif isinstance(a, list):
            assert len(a) == len(b)
            for ai, bi in zip(a, b):
                walk_trees(ai, bi)
        elif isinstance(a, (np.ndarray, asdf.tags.core.ndarray.NDArrayType)):
            np.testing.assert_array_equal(a, b)
        else:
            assert a == b

    ignore_keys = {"asdf_library", "history"}
    walk_trees(
        {k: v for k, v in tree_a.items() if k not in ignore_keys},
        {k: v for k, v in tree_b.items() if k not in ignore_keys},
    )


@pytest.mark.parametrize(
    "a, b",
    [
        ({"l": [1, 2, 3]}, {"l": [1, 2, 3]}),
        ({"d": {"a": 1}}, {"d": {"a": 1}}),
        ({"ld": [{"a": 1}]}, {"ld": [{"a": 1}]}),
        ({"ld": [{"a": 1}]}, {"ld": [{"a": 1}]}),
        ({"dk": {"a": 1, "b": 2}}, {"dk": {"b": 2, "a": 1}}),
        ({"a": np.arange(3)}, {"a": np.arange(3)}),
        ({"la": [np.arange(3)]}, {"la": [np.arange(3)]}),
        ({"i": 1}, {"i": 1}),
        ({"s": "abc"}, {"s": "abc"}),
        ({"f": 1.0}, {"f": 1.0}),
        ({"i": 1}, {"i": 1, "asdf_library": None}),
        ({"i": 1}, {"i": 1, "history": None}),
    ],
)
def test_assert_tree_match(a, b):
    assert_tree_match(a, b)


@pytest.mark.parametrize(
    "a, b",
    [
        ({"l": [1, 2, 3]}, {"l": [1, 2]}),
        ({"l": [1, 2, 3]}, {"l": [1, 2, 4]}),
        ({"d": {"a": 1}}, {"d": {"a": 2}}),
        ({"d": {"a": 1}}, {"d": {"b": 1}}),
        ({"d": {"a": 1, "b": 2}}, {"d": {"a": 1}}),
        ({"d": {"a": 1}}, {"d": {"a": 1, "b": 2}}),
        ({"a": np.arange(3)}, {"a": np.arange(4)}),
        ({"la": [np.arange(3)]}, {"a": [np.arange(4)]}),
        ({"i": 1}, {"i": 2}),
        ({"s": "abc"}, {"s": "def"}),
        ({"f": 1.0}, {"f": 1.1}),
    ],
)
def test_assert_tree_match_fail(a, b):
    with pytest.raises(AssertionError):
        assert_tree_match(a, b)


def get_test_id(reference_file_path):
    """Helper function to return the informative part of a schema path"""
    path = os.path.normpath(str(reference_file_path))
    return os.path.sep.join(path.split(os.path.sep)[-3:])


def collect_reference_files():
    """Function used by pytest to collect ASDF reference files for testing."""
    for version in asdf.versioning.supported_versions:
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

    with asdf.open(asdf_path) as af_handle:
        af_handle.resolve_references()

        with asdf.open(yaml_path) as ref:
            # TODO strip asdf_library and history
            assert_tree_match(af_handle.tree, ref.tree)


def test_reference_files_exist():
    assert list(collect_reference_files())


@pytest.mark.parametrize("reference_file", collect_reference_files(), ids=get_test_id)
def test_reference_file(reference_file):
    name_without_ext, _ = os.path.splitext(reference_file)
    _compare_trees(name_without_ext)
