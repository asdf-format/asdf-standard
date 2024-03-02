import re
from pathlib import Path
from urllib.parse import urljoin

import yaml
from packaging.version import Version

ROOT_PATH = Path(__file__).parent.parent

RESOURCES_PATH = ROOT_PATH / "resources"

SCHEMAS_PATH = RESOURCES_PATH / "schemas" / "stsci.edu" / "asdf"
DOCS_PATH = ROOT_PATH / "docs" / "source"
DOCS_SCHEMAS_PATH = DOCS_PATH / "schemas"
YAML_SCHEMA_PATH = RESOURCES_PATH / "schemas" / "stsci.edu" / "yaml-schema"

MANIFESTS_PATH = RESOURCES_PATH / "manifests" / "asdf-format.org" / "core"

VERSION_MAP_PATHS = list(SCHEMAS_PATH.glob("version_map-*.yaml"))

VALID_YAML_VERSIONS = {"1.1"}
VALID_FILE_FORMAT_VERSIONS = {"1.0.0"}

VALID_SCHEMA_FILENAME_RE = re.compile(r"[a-z0-9_]+-[0-9]+\.[0-9]+\.[0-9]+\.yaml")

DEPRECATED_PATTERNS = {
    re.compile(".*/transform/.*"),
    re.compile(".*/wcs/.*"),
    re.compile(".*/core/column.*"),
    re.compile(".*/core/table.*"),
    re.compile(".*/core/subclass_metadata.*"),
    re.compile(".*/fits/.*"),
    re.compile(".*/table/.*"),
    re.compile(".*/unit/.*"),
    re.compile(".*/time/.*"),
}

METASCHEMA_ID = "http://stsci.edu/schemas/yaml-schema/draft-01"

YAML_TAG_RE = re.compile(r"![a-z/0-9_-]+-[0-9]+\.[0-9]+\.[0-9]")

DESCRIPTION_REF_RE = re.compile(r"\(ref:(.*?)\)")

SCHEMA_ID_PREFIX = "http://stsci.edu/schemas/asdf/"
MANIFEST_ID_PREFIX = "asdf://asdf-format.org/core/manifests/"


def load_yaml(path):
    with path.open() as f:
        return yaml.safe_load(f.read())


def assert_yaml_header_and_footer(path):
    with path.open() as f:
        content = f.read()

    assert any(
        content.startswith(f"%YAML {v}\n---\n") for v in VALID_YAML_VERSIONS
    ), f"{path.name} must start with a %YAML directive with a supported version"

    assert content.endswith("\n...\n"), f"{path.name} must end with '...' followed by a single newline"


def is_deprecated(schema_id_or_tag):
    return any(p.match(schema_id_or_tag) for p in DEPRECATED_PATTERNS)


def split_id(schema_id):
    return schema_id.rsplit("-", 1)


def yaml_tag_to_id(yaml_tag):
    return "http://stsci.edu/schemas/asdf/" + yaml_tag.replace("!", "")


def _relative_stem(path):
    return f"{str((path.parent).relative_to(SCHEMAS_PATH))}/{str(path.stem)}"


def path_to_tag(path):
    return f"tag:stsci.edu:asdf/{_relative_stem(path)}"


def tag_to_path(tag):
    assert tag.startswith("tag:stsci.edu:asdf/")

    return SCHEMAS_PATH / f"""{tag.split("tag:stsci.edu:asdf/")[-1]}.yaml"""


def tag_to_id(tag):
    assert tag.startswith("tag:stsci.edu:asdf/")

    return "http://stsci.edu/schemas/asdf/" + tag.split("tag:stsci.edu:asdf/")[-1]


def id_to_path(id):
    assert id.startswith("http://stsci.edu/schemas/asdf/")

    return SCHEMAS_PATH / f"""{id.split("http://stsci.edu/schemas/asdf/")[-1]}.yaml"""


def path_to_id(path):
    return f"http://stsci.edu/schemas/asdf/{_relative_stem(path)}"


def list_schema_paths(path):
    return sorted(p for p in path.glob("**/*.yaml") if not p.name.startswith("version_map-"))


def list_latest_schema_paths(path):
    paths = list_schema_paths(path)

    latest_by_id_base = {}
    for path in paths:
        schema_id = path_to_id(path)
        id_base, version = split_id(schema_id)
        if id_base in latest_by_id_base:
            if Version(version) > Version(latest_by_id_base[id_base][0]):
                latest_by_id_base[id_base] = (version, path)
        else:
            latest_by_id_base[id_base] = (version, path)

    return sorted(p for _, p in latest_by_id_base.values())


def list_legacy_schema_paths(path):
    paths = list_schema_paths(path)
    latest_paths = list_latest_schema_paths(path)

    return sorted(p for p in paths if p not in latest_paths)


def ref_to_id(schema_id, ref):
    return urljoin(schema_id, ref)


def list_refs(schema):
    refs = []
    if isinstance(schema, dict):
        for key, value in schema.items():
            if key == "$ref":
                refs.append(value)
            elif isinstance(value, dict) or isinstance(value, list):
                refs.extend(list_refs(value))
    elif isinstance(schema, list):
        for elem in schema:
            refs.extend(list_refs(elem))
    return refs


def list_example_ids(schema):
    if "examples" in schema:
        example_yaml_tags = set()
        for example in schema["examples"]:
            if len(example) == 1:
                example = example[0]
            elif len(example) == 2:
                example = example[1]
            elif len(example) > 2:
                example = example[2]
            else:
                raise RuntimeError(f"Invalid example: {example}")
            example_yaml_tags.update(YAML_TAG_RE.findall(example))
        return sorted({yaml_tag_to_id(yaml_tag) for yaml_tag in example_yaml_tags})
    else:
        return []


def list_description_ids(schema):
    result = set()
    if "description" in schema:
        for ref in DESCRIPTION_REF_RE.findall(schema["description"]):
            if not ref.startswith("http:"):
                ref = "http://stsci.edu/schemas/asdf/" + ref
            result.add(ref)
    return result
