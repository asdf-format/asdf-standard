import asdf

cfg = asdf.get_config()
resource_manager = cfg.resource_manager
all_extensions = cfg.extensions

all_standard_versions = [str(v) for v in asdf.versioning.supported_versions]

all_schemas = {}
all_manifests = {}
manifests_by_extension_uri = {}
schema_uris_by_package_name = {}
schema_links_by_uri = {}

for uri in resource_manager:
    schema = asdf.schema.load_schema(uri)
    if "id" not in schema:
        # FIXME version maps don't have id
        assert "FILE_FORMAT" in schema
    else:
        # FIXME not sure why the uri/id here has a fragment
        if not uri.startswith("http://json-schema.org/draft-04/schema"):
            assert uri == schema["id"], (uri, schema["id"])  # sanity check
    if uri in all_schemas:
        # don't duplicate uris
        raise Exception
    all_schemas[uri] = schema
    if "extension_uri" in schema:
        all_manifests[uri] = schema
        extension_uri = schema["extension_uri"]
        # 2 manifests should not share uris
        if extension_uri in manifests_by_extension_uri:
            # TODO helpful error
            raise Exception
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
                links.append({"ref": item["$ref"], "path": path})
                children = []
            elif "tag" in item:
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

    # extensions and manifests do not have a 1-to-1 mapping because of asdf-astropy CompoundManifest
    # but that doesn't really matter as long as the extension_uri is unique and all the ones
    # defined in manifests are used, right? The id is used to load the manifest which defines
    # the extension_uri. This is 'compounded' in astropy where the core manifest is combined
    # with a special 'astropy' one (which is the one that should define the extension_uri).

    # extension_by_manifest_id = {}
    # for ext in all_extensions:
    #     delegate = ext.delegate
    #     if hasattr(delegate, '_manifest'):
    #         manifest_ids = [delegate._manifest['id'],]
    #     else:
    #         manifest_ids = [ext._manifest['id'] for ext in delegate._extensions]
    #     for manifest_id in manifest_ids:
    #         extension_by_manifest_id[manifest_id] = ext

    tag_info_by_version[standard_version] = tag_info_by_uri

# TODO check schemas with out-of-date (or missing) '$schema'

asdf.AsdfFile(
    {
        "versions": all_standard_versions,
        "schemas": all_schemas,
        "manifests": all_manifests,
        "manifests_by_extension_uri": manifests_by_extension_uri,
        "schema_links_by_uri": schema_links_by_uri,
        "schema_uris_by_package_name": schema_uris_by_package_name,
        "tag_info_by_version": tag_info_by_version,
    }
).write_to("asdf.asdf")
