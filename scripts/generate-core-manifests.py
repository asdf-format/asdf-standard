# Generate the file in resources/asdf-format.org/core/manifests/

import glob
import os

import yaml

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

SCHEMA_PATTERNS = [
    "schemas/stsci.edu/asdf/core/*.yaml",
    "schemas/stsci.edu/asdf/fits/*.yaml",
    "schemas/stsci.edu/asdf/time/*.yaml",
    "schemas/stsci.edu/asdf/unit/*.yaml",
    "schemas/stsci.edu/asdf/wcs/*.yaml",
]


def represent_string(dumper, data):
    if len(data.splitlines()) > 1:
        style = "|"
    else:
        style = None

    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.SafeDumper.add_representer(str, represent_string)

schemas_by_tag = {}
for pattern in SCHEMA_PATTERNS:
    for path in glob.glob(pattern):
        schema = yaml.safe_load(open(path).read())
        tag = "tag:stsci.edu:" + schema["id"].split("http://stsci.edu/schemas/")[-1]
        schemas_by_tag[tag] = schema

for path in sorted(glob.glob("schemas/stsci.edu/asdf/version_map-*.yaml")):
    version_map = yaml.safe_load(open(path).read())
    version = path.split("/")[-1].split("-")[-1].split(".yaml")[0]
    tags = sorted([k + "-" + str(v) for k, v in version_map["tags"].items() if "/transform/" not in k])

    tag_defs = []
    for tag in tags:
        schema = schemas_by_tag[tag]
        tag_def = {
            "tag_uri": tag,
            "schema_uri": schema["id"],
            "title": schema["title"].strip(),
            "description": schema["description"].strip(),
        }
        tag_defs.append(tag_def)

    manifest = {
        "id": f"asdf://asdf-format.org/core/manifests/core-{version}",
        "extension_uri": f"asdf://asdf-format.org/core/extensions/core-{version}",
        "title": f"Core extension {version}",
        "description": "Tags for ASDF core objects.",
        "asdf_standard_requirement": version,
        "tags": tag_defs,
    }

    with open(f"resources/asdf-format.org/core/manifests/core-{version}.yaml", "w") as f:
        yaml.dump(manifest, f, sort_keys=False, Dumper=yaml.SafeDumper)
