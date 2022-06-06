import collections

from common import is_deprecated

EXCEPTIONS = {"tag:stsci.edu:asdf/asdf-schema-1.0.0"}


def test_docs_schema_links(latest_schema_ids, legacy_schema_ids, docs_schema_ids, docs_legacy_schema_ids):
    """
    Confirm that the latest versions of all non-deprecated schemas
    are represented in the documentation.
    """
    expected_schema_ids = set()
    for schema_id in latest_schema_ids:
        if not is_deprecated(schema_id):
            expected_schema_ids.add(schema_id)

    extra_legacy_docs_ids = set(docs_legacy_schema_ids) - legacy_schema_ids - EXCEPTIONS
    if len(extra_legacy_docs_ids) > 0:
        remove_list = "\n".join(sorted(list(extra_legacy_docs_ids)))
        message = (
            "Only the legacy documentation should link to old versions of schemas. "
            "Remove or update the following links: \n"
            f"{remove_list}"
        )
        assert False, message

    extra_docs_ids = set(docs_schema_ids) - expected_schema_ids - EXCEPTIONS - set(docs_legacy_schema_ids)
    if len(extra_docs_ids) > 0:
        remove_list = "\n".join(sorted(list(extra_docs_ids)))
        message = (
            "The main documentation should not link to old versions of schemas. "
            "Remove or update the following links to the legacy documentation: \n"
            f"{remove_list}"
        )
        assert False, message

    missing_docs_ids = expected_schema_ids - set(docs_schema_ids) - EXCEPTIONS
    if len(missing_docs_ids) > 0:
        insert_list = "\n".join(sorted(list(missing_docs_ids)))
        message = (
            "The documentation must include a link to the latest version of "
            "every non-deprecated schema with a tag.  Update the deprecation "
            "list in tests/common.py, or add links to the following missing schemas: \n"
            f"{insert_list}"
        )
        assert False, message

    counter = collections.Counter(docs_schema_ids)
    if max(counter.values()) > 1:
        remove_list = "\n".join(sorted([tag for tag, count in counter.items() if count > 1]))
        message = "The documentation contains duplicate links to the following schemas: \n" f"{remove_list}"
        assert False, message
