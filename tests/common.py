from pathlib import Path

from asdf_standard.tests.common import (
    MANIFESTS_PATH,
    SCHEMAS_PATH,
    get_latest_schemas,
    get_schema_ids,
    list_latest_schema_paths,
    list_schema_paths,
    load_yaml,
)

ROOT_PATH = Path(__file__).parent.parent
DOCS_SCHEMAS_PATH = ROOT_PATH / "docs" / "source" / "schemas"

SCHEMA_ID_PREFIX = "http://stsci.edu/schemas/asdf/"
MANIFEST_ID_PREFIX = "asdf://asdf-format.org/core/manifests/"


def add_schemas(path, prefix, result):
    with open(path) as f:
        content = f.read()

    lines = content.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].startswith(".. asdf-autoschemas::"):
            i += 1
            while i < len(lines) and (lines[i].strip() == "" or lines[i].startswith(" ")):
                possible_id = lines[i].strip()
                if len(possible_id) > 0:
                    result.append(f"{prefix}{possible_id}")
                i += 1
        else:
            i += 1


def list_legacy_schema_paths(path):
    paths = list_schema_paths(path)
    latest_paths = list_latest_schema_paths(path)

    return sorted(p for p in paths if p not in latest_paths)


def latest_schema_ids():
    return get_schema_ids(get_latest_schemas())


def legacy_schema_ids():
    return get_schema_ids([load_yaml(p) for p in list_legacy_schema_paths(SCHEMAS_PATH)])


def manifest_ids():
    return get_schema_ids([load_yaml(p) for p in list_schema_paths(MANIFESTS_PATH)])


def docs_schema_ids():
    result = []
    for path in DOCS_SCHEMAS_PATH.glob("**/*.rst"):
        if path != DOCS_SCHEMAS_PATH / "manifest.rst":
            add_schemas(path, SCHEMA_ID_PREFIX, result)
    return result


def docs_legacy_schema_ids():
    result = []
    for path in DOCS_SCHEMAS_PATH.glob("**/legacy.rst"):
        add_schemas(path, SCHEMA_ID_PREFIX, result)
    return result


def docs_manifest_ids():
    result = []
    for path in DOCS_SCHEMAS_PATH.glob("**/manifest.rst"):
        add_schemas(path, MANIFEST_ID_PREFIX, result)
    return result
