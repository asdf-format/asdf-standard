import os
import re

import asdf

cfg = asdf.get_config()
resource_manager = cfg.resource_manager
all_extensions = cfg.extensions

all_standard_versions = sorted([str(v) for v in asdf.versioning.supported_versions])

all_schemas = {}
all_manifests = {}
manifests_by_extension_uri = {}
schema_uris_by_package_name = {}
schema_links_by_uri = {}
schema_versions_by_base_uri = {}
errors = []


def error(**kwargs):
    errors.append(kwargs)
    if "msg" in kwargs:
        print(f"ERROR: {kwargs['msg']}")


def split_uri_base_and_version(uri):
    # parts = asdf.util._patched_urllib_parse.urlparse(uri)
    # basename = os.path.basename(parts.path)
    m = re.match(r"^(?P<base>.*)-(?P<version>([0-9]+\.?){1,3}(-.*)?)$", uri)
    if m:
        version = m["version"]
        base = m["base"]
        assert "-".join((base, version)) == uri
    else:
        version = ""
        base = uri
    if len(version) and not version[0].isdigit():
        version = ""
        base = uri
    return base, version


def join_uri_base_and_version(base, version):
    if not version:
        return base
    return "-".join((base, version))


def latest_version(base):
    versions = schema_versions_by_base_uri[base]
    if len(versions) == 1:
        version = versions[0]
    else:
        version = sorted(versions)[-1]
    if not version:
        return base
    return "-".join((base, version))


for uri in resource_manager:
    schema = asdf.schema.load_schema(uri)
    if "id" not in schema:
        # FIXME version maps don't have id
        assert "FILE_FORMAT" in schema
    else:
        # FIXME not sure why the json-schema uri/id here has a fragment
        if not uri.startswith("http://json-schema.org/draft-04/schema"):
            if uri != schema["id"]:
                msg = f"id[{schema['id']}] does not match uri[{uri}]"
                error(msg=msg, uri=uri, schema_id=schema["id"])
    if uri in all_schemas:
        # don't duplicate uris
        msg = f"uri[{uri}] is registered >1 time"
        error(msg=msg, uri=uri)

    all_schemas[uri] = schema

    if not uri.startswith("http://json-schema.org/draft-04/schema"):
        parts = asdf.util._patched_urllib_parse.urlparse(uri)
        base_name = os.path.basename(parts.path)
        if "-" not in base_name:
            # jwst datamodel schemas are not versioned
            if not uri.startswith("http://stsci.edu/schemas/jwst_datamodel"):
                msg = f"uri[{uri}] is not versioned"
                error(msg=msg, uri=uri)
            base = uri
            version = ""
        else:
            base, version = split_uri_base_and_version(uri)
        if base not in schema_versions_by_base_uri:
            schema_versions_by_base_uri[base] = []
        if version in schema_versions_by_base_uri:
            raise Exception
        schema_versions_by_base_uri[base].append(version)

    if "extension_uri" in schema:
        all_manifests[uri] = schema
        extension_uri = schema["extension_uri"]
        # 2 manifests should not share uris
        if extension_uri in manifests_by_extension_uri:
            uri2 = manifests_by_extension_uri[extension_uri]["id"]
            msg = f"two manifests [{uri}, {uri2}] share the extension_uri[{extension_uri}]"
            error(msg=msg, uri=uri, extension_uri=extension_uri)
        manifests_by_extension_uri[extension_uri] = schema

    # record what packages provide schemas (so we can check if this changes)
    package_name = resource_manager._mappings_by_uri[uri].package_name
    if package_name not in schema_uris_by_package_name:
        schema_uris_by_package_name[package_name] = []
    schema_uris_by_package_name[package_name].append(uri)

    # get all external references for this schema ($ref, $schema, tag)
    links = []
    search = [(schema, ())]
    while search:
        item, path = search.pop()

        # step into item
        if isinstance(item, list):
            children = enumerate(item)
        elif isinstance(item, dict):
            # top level $schema
            if not path and "$schema" in item:
                links.append({"schema": item["$schema"], "path": path})

            if "$ref" in item:
                ref = item["$ref"]
                resolved = asdf.util._patched_urllib_parse.urljoin(uri, item["$ref"])
                # remove fragment
                resolved = asdf.util._patched_urllib_parse.urlunparse(
                    asdf.util._patched_urllib_parse.urlparse(resolved)._replace(fragment="")
                )
                local = resolved.startswith(uri)
                links.append(
                    {
                        "ref": ref,
                        "path": path,
                        "resolved": resolved,
                        "local": local,
                    }
                )
                children = []
            elif "tag" in item:
                # the yaml-schema defines tag, so don't treat it as a link
                if not uri.startswith("http://stsci.edu/schemas/yaml-schema/draft-01"):
                    links.append({"tag": item["tag"], "path": path})
                children = []
            else:
                children = item.items()
        else:
            children = []
        if children:
            for key, child in children:
                if isinstance(child, (list, dict)):
                    search.append((child, path + (key,)))
    schema_links_by_uri[uri] = links

# check tags and schemas in manifests
# first index all manifests by base, version
manifests_by_base_by_version = {}
for manifest_uri in all_manifests:
    base, version = split_uri_base_and_version(manifest_uri)
    if base not in manifests_by_base_by_version:
        manifests_by_base_by_version[base] = {}
    manifests_by_base_by_version[base][version] = manifest_uri

for base, versions in manifests_by_base_by_version.items():
    # for the most recent version of each manifest it should only reference the newest tags and schemas
    version = sorted(versions)[-1]
    manifest_uri = versions[version]
    manifest = all_manifests[manifest_uri]
    for tag_def in manifest["tags"]:
        tag_uri = tag_def["tag_uri"]
        schema_uris = tag_def["schema_uri"]
        # TODO

# check that all refs and schemas point to known schemas
for uri, links in schema_links_by_uri.items():
    for link in links:
        if "ref" in link:
            other_uri = link["resolved"]
        elif "schema" in link:
            other_uri = link["schema"]
        if other_uri.startswith("http://json-schema.org/draft-04/schema"):
            continue
        if other_uri not in all_schemas:
            msg = f"schema[{uri}] refers to unknown schema[{other_uri}]"
            error(msg=msg, uri=uri, other_uri=other_uri)

# check that the latest version of all schemas refer to the latest version of other schemas
# checking both '$ref' and '$schema'
for base_uri in schema_versions_by_base_uri:
    latest_uri = latest_version(base_uri)
    links = schema_links_by_uri[latest_uri]
    for link in links:
        if "ref" in link:
            other_uri = link["resolved"]
        elif "schema" in link:
            other_uri = link["schema"]
        elif "tag" in link:
            # TODO check tag links
            continue
        else:
            raise Exception(f"unknown link {link}")
        if other_uri.startswith("http://json-schema.org/draft-04/schema"):
            continue
        other_base_uri, _ = split_uri_base_and_version(other_uri)
        other_latest_uri = latest_version(other_base_uri)
        if other_uri != other_latest_uri:
            msg = f"schema [{latest_uri}] refers to out-dated schema [{other_uri}] instead of [{other_latest_uri}]"
            error(
                msg=msg,
                latest_uri=latest_uri,
                other_uri=other_uri,
                other_latest_uri=other_latest_uri,
            )

# we want maps (per version because of the tag use) for
# - TODO schema to schema (via $ref, $schema, tag)
# - schema to tag
# - tag to type [this isn't one-to-one]
# - TODO extension to schema (via tag)
# - extension to tag

tag_info_by_version = {}

for standard_version in all_standard_versions:
    # the extension manager allows tags/type to be overridden
    # track these separately
    extension_manager = asdf.AsdfFile(version=standard_version).extension_manager

    # also consider all extensions (even ones overridden)
    extensions = [e for e in all_extensions if standard_version in e.asdf_standard_requirement]

    # by uri so each entry here corresponds to a tag used in this version
    tag_info_by_uri = {}

    # look up all extensions for this version that define tags
    for extension in extensions:
        for tag_def in extension.tags:
            # multiple extensions might define tags
            if tag_def.tag_uri in tag_info_by_uri:
                tag_info = tag_info_by_uri[tag_def.tag_uri]
            else:
                tag_info = {
                    "extension_uris": [],
                    "schema_uris_by_extension_uri": {},
                }
            tag_info["extension_uris"].append(extension.extension_uri)
            tag_info["schema_uris_by_extension_uri"][extension.extension_uri] = tag_def.schema_uris
            tag_info_by_uri[tag_def.tag_uri] = tag_info

    for tag_uri in tag_info_by_uri:
        tag_info = tag_info_by_uri[tag_uri]
        try:
            converter = extension_manager.get_converter_for_tag(tag_uri)
        except KeyError:
            # some tags that are defined in extensions do not have converters
            # one example is "label_mapper". Mark these as not supported.
            tag_info["supported"] = False
            continue
        tag_info["supported"] = True
        tag_info["handling_extension_uri"] = converter._extension.extension_uri
        tag_info["types"] = []
        for typ in converter.types:
            if isinstance(typ, str):
                type_string = typ
            else:
                type_string = asdf.util.get_class_name(typ, False)
            tag_info["types"].append(type_string)

    tag_info_by_version[standard_version] = tag_info_by_uri

for previous_version, next_version in zip(all_standard_versions[:-1], all_standard_versions[1:]):
    assert next_version > previous_version
    previous_tag_info = tag_info_by_version[previous_version]
    next_tag_info = tag_info_by_version[next_version]

    # look for added/removed tags between these versions
    previous_tags_set = set(previous_tag_info.keys())
    next_tags_set = set(next_tag_info.keys())
    added_tags = next_tags_set.difference(previous_tags_set)
    removed_tags = previous_tags_set.difference(next_tags_set)
    # index added tags by base/version
    added_tags_by_base_by_version = {}
    for added_tag in added_tags:
        added_base, added_version = split_uri_base_and_version(added_tag)
        if added_base not in added_tags_by_base_by_version:
            added_tags_by_base_by_version[added_base] = {}
        added_tags_by_base_by_version[added_base][added_version] = added_tag
    for removed_tag in removed_tags:
        # look for an new version in added_tags
        removed_base, removed_version = split_uri_base_and_version(removed_tag)
        if removed_base not in added_tags_by_base_by_version:
            error(
                msg=f"Support for tag {removed_tag} was removed in version {next_version}",
                removed_tag=removed_tag,
                removed_version=next_version,
            )
        else:
            new_versions = added_tags_by_base_by_version[removed_base]
            # at least one of these versions should be newer
            for version in new_versions:
                if version > removed_version:
                    # print(f"In {next_version}: tag {removed_tag} replaced with newer version {new_versions[version]}")
                    pass

    # look for added/removed types between these versions
    previous_types = set(sum((i.get("types", []) for i in previous_tag_info.values()), start=[]))
    next_types = set(sum((i.get("types", []) for i in next_tag_info.values()), start=[]))
    removed_types = previous_types.difference(next_types)
    added_types = next_types.difference(previous_types)
    for added_type in added_types:
        # print(f"In {next_version}: support for type {added_type} added")
        pass
    for removed_type in removed_types:
        error(
            msg=f"Support for {removed_type} was removed in version {next_version}",
            removed_type=removed_type,
            removed_version=next_version,
        )

# check 'tag' links in schemas
for standard_version, tag_info in tag_info_by_version.items():
    if standard_version != "1.5.0":
        # TODO test against 1.6.0 and older versions?
        continue
    # use version info to check tag links
    for uri, links in schema_links_by_uri.items():
        if uri.startswith("http://json-schema.org/draft-04/schema"):
            continue
        base, _ = split_uri_base_and_version(uri)
        # only check the latest versions of all schemas
        # TODO should we update tag directives for old schemas?
        if uri != latest_version(base):
            continue
        for link in links:
            if "tag" not in link:
                # schema and ref links were checked above
                continue
            tag_pattern = link["tag"]
            if tag_pattern in tag_info:
                # this is a direct match with a known tag
                tags = [
                    tag_pattern,
                ]
            else:
                # wildcard
                matches = []
                for tag in tag_info:
                    if asdf.util.uri_match(tag_pattern, tag):
                        matches.append(tag)
                # it's ok to have multiple tags that match as
                # multiple extensions might be registered for different tag versions
                # it's not ok to have no tags match
                if not len(matches):
                    msg = f"In ASDF[{standard_version}] no tags match pattern[{tag_pattern}] for schema[{uri}]"
                    error(msg=msg, standard_version=standard_version, tag_pattern=tag_pattern, uri=uri)
                tags = matches

            # make sure one matching tag is supported
            supported = False
            for tag in tags:
                info = tag_info[tag]
                supported |= info["supported"]
            if not supported:
                msg = f"In ASDF[{standard_version}] schema[{uri}] does not mach any supported tags [{tags}] with pattern [{tag_pattern}]"
                error(msg=msg, standard_version=standard_version, uri=uri, tag_pattern=tag_pattern, tags=tags)

asdf.AsdfFile(
    {
        "versions": all_standard_versions,
        "schemas": all_schemas,
        "manifests": all_manifests,
        "manifests_by_extension_uri": manifests_by_extension_uri,
        "schema_links_by_uri": schema_links_by_uri,
        "schema_uris_by_package_name": schema_uris_by_package_name,
        "schema_versions_by_base_uri": schema_versions_by_base_uri,
        "tag_info_by_version": tag_info_by_version,
        "errors": errors,
    }
).write_to("asdf.asdf")
