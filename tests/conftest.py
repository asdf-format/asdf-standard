import pytest
import glob
from common import (
    DOCS_SCHEMAS_PATH,
    DOCS_SCHEMAS_LIST,
    MANIFEST_ID_PREFIX,
    MANIFESTS_PATH,
    METASCHEMA_ID,
    SCHEMA_ID_PREFIX,
    SCHEMAS_PATH,
    VALID_SCHEMA_FILENAME_RE,
    YAML_SCHEMA_PATH,
    assert_yaml_header_and_footer,
    is_deprecated,
    list_description_ids,
    list_example_ids,
    list_latest_schema_paths,
    list_legacy_schema_paths,
    list_refs,
    list_schema_paths,
    load_yaml,
    path_to_id,
    path_to_tag,
    ref_to_id,
    split_id,
)


@pytest.fixture(scope="session")
def schemas():
    return [load_yaml(p) for p in list_schema_paths(SCHEMAS_PATH)]


@pytest.fixture(scope="session")
def manifests():
    return [load_yaml(p) for p in list_schema_paths(MANIFESTS_PATH)]


@pytest.fixture(scope="session")
def yaml_schemas():
    return [load_yaml(p) for p in list_schema_paths(YAML_SCHEMA_PATH)]


@pytest.fixture(scope="session")
def latest_schemas():
    return [load_yaml(p) for p in list_latest_schema_paths(SCHEMAS_PATH)]


@pytest.fixture(scope="session")
def legacy_schemas():
    return [load_yaml(p) for p in list_legacy_schema_paths(SCHEMAS_PATH)]


def get_schema_ids(schemas):
    result = set()
    for schema in schemas:
        if "id" in schema:
            result.add(schema["id"])
    return result


@pytest.fixture(scope="session")
def latest_schema_ids(latest_schemas):
    return get_schema_ids(latest_schemas)


@pytest.fixture(scope="session")
def legacy_schema_ids(legacy_schemas):
    return get_schema_ids(legacy_schemas)


@pytest.fixture(scope="session")
def manifest_ids(manifests):
    return get_schema_ids(manifests)


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


@pytest.fixture(scope="session")
def docs_schema_ids():
    result = []
    for fname in DOCS_SCHEMAS_LIST:
        path = glob.glob(f"{DOCS_SCHEMAS_PATH}/{fname}")[0]
        if path != DOCS_SCHEMAS_PATH / "manifest.rst":
            add_schemas(path, SCHEMA_ID_PREFIX, result)
    return result


@pytest.fixture(scope="session")
def docs_legacy_schema_ids():
    result = []
    for path in DOCS_SCHEMAS_PATH.glob("**/legacy.rst"):
        add_schemas(path, SCHEMA_ID_PREFIX, result)
    return result


@pytest.fixture(scope="session")
def docs_manifest_ids():
    result = []
    for path in DOCS_SCHEMAS_PATH.glob("**/manifest.rst"):
        add_schemas(path, MANIFEST_ID_PREFIX, result)
    return result


@pytest.fixture(scope="session")
def id_to_schema(schemas):
    result = {}
    for schema in schemas:
        if "id" in schema:
            if schema["id"] not in result:
                result[schema["id"]] = []
            result[schema["id"]].append(schema)
    return result


@pytest.fixture(scope="session")
def assert_schema_correct(id_to_schema):
    def _assert_schema_correct(path):
        __tracebackhide__ = True

        assert VALID_SCHEMA_FILENAME_RE.match(path.name) is not None, f"{path.name} is an invalid schema filename"

        assert_yaml_header_and_footer(path)

        schema = load_yaml(path)

        assert "$schema" in schema, f"{path.name} is missing $schema key"
        assert schema["$schema"] == METASCHEMA_ID, f"{path.name} has wrong $schema value (expected {METASCHEMA_ID})"

        expected_id = path_to_id(path)
        expected_tag = path_to_tag(path)

        assert "id" in schema, f"{path.name} is missing id key (expected {expected_id})"
        assert schema["id"] == expected_id, f"{path.name} id doesn't match filename (expected {expected_id})"

        if "tag" in schema:
            assert schema["tag"] == expected_tag, f"{path.name} tag doesn't match filename (expected {expected_tag})"

        assert "title" in schema, f"{path.name} is missing title key"
        assert len(schema["title"].strip()) > 0, f"{path.name} title must have content"

        assert "description" in schema, f"{path.name} is missing description key"
        assert len(schema["description"].strip()) > 0, f"{path.name} description must have content"

        assert len(id_to_schema[schema["id"]]) == 1, f"{path.name} does not have a unique id"

        id_base, _ = split_id(schema["id"])
        for example_id in list_example_ids(schema):
            example_id_base, _ = split_id(example_id)
            if example_id_base == id_base and example_id != schema["id"]:
                assert False, f"{path.name} contains an example with an outdated tag"

        for description_id in list_description_ids(schema):
            if len(description_id.rsplit("-", 1)) > 1:
                description_id_base, _ = split_id(description_id)
                if description_id_base == id_base and description_id != schema["id"]:
                    assert False, f"{path.name} descriptioon contains an outdated ref"

    return _assert_schema_correct


@pytest.fixture(scope="session")
def assert_latest_schema_correct(latest_schema_ids):
    def _assert_latest_schema_correct(path):
        __tracebackhide__ = True

        schema = load_yaml(path)

        if is_deprecated(schema["id"]):
            return

        refs = [r.split("#")[0] for r in list_refs(schema) if not r.startswith("#") and not r == METASCHEMA_ID]
        for ref in refs:
            ref_id = ref_to_id(schema["id"], ref)
            assert ref_id in latest_schema_ids, (
                f"{path.name} is the latest version of a schema, " f"but references {ref}, which is not latest"
            )

        for example_id in list_example_ids(schema):
            assert example_id in latest_schema_ids, (
                f"{path.name} is the latest version of a schema, "
                f"but its examples include {example_id}, which is not latest"
            )

        for description_id in list_description_ids(schema):
            if len(description_id.rsplit("-", 1)) > 1:
                assert description_id in latest_schema_ids, (
                    f"{path.name} is the latest version of a schema, "
                    f"but its description includes a ref to {description_id}, "
                    "which is not latest"
                )

    return _assert_latest_schema_correct
