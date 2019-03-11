import os
import posixpath

import yaml

from docutils import nodes
from docutils.frontend import OptionParser
from docutils.statemachine import ViewList

from sphinx import addnodes
from sphinx.parsers import RSTParser
from sphinx.util.fileutil import copy_asset
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.docutils import SphinxDirective, new_document

from .md2rst import md2rst
from .nodes import (add_asdf_nodes, toc_link, schema_header_title,
                    schema_title, schema_description, schema_properties,
                    schema_property, schema_property_name,
                    schema_property_details, schema_anyof_body,
                    schema_anyof_item, section_header, asdf_tree, asdf_ref,
                    example_section, example_item, example_description)


SCHEMA_DEF_SECTION_TITLE = 'Schema Definitions'
EXAMPLE_SECTION_TITLE = 'Examples'
ORIGINAL_SCHEMA_SECTION_TITLE = 'Original Schema'


class schema_def(nodes.comment):
    pass


class AsdfSchemas(SphinxDirective):

    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def _process_asdf_toctree(self):

        links = []
        for name in self.content:
            if not name:
                continue
            schema = self.env.path2doc(name.strip() + '.rst')
            link = posixpath.join('generated', schema)
            links.append((schema, link))

        tocnode = addnodes.toctree()
        tocnode['includefiles'] = [x[1] for x in links]
        tocnode['entries'] = links
        tocnode['maxdepth'] = -1
        tocnode['glob'] = None

        paragraph = nodes.paragraph(text="Here's where the schemas go")
        return [paragraph, tocnode]


    def run(self):

        # This is the case when we are actually using Sphinx to generate
        # documentation
        if not getattr(self.env, 'autoasdf_generate', False):
            return self._process_asdf_toctree()

        # This case allows us to use docutils to parse input documents during
        # the 'builder-inited' phase so that we can determine which new
        # document need to be created by 'autogenerate_schema_docs'. This seems
        # much cleaner than writing a custom parser to extract the schema
        # information.
        return [schema_def(text=c.strip().split()[0]) for c in self.content]


class AsdfSchema(SphinxDirective):

    has_content = True

    def run(self):

        self.schema_name = self.content[0]
        schema_dir = self.state.document.settings.env.config.asdf_schema_path
        srcdir = self.state.document.settings.env.srcdir

        schema_file = posixpath.join(srcdir, schema_dir, self.schema_name) + '.yaml'

        with open(schema_file) as ff:
            raw_content = ff.read()
            schema = yaml.safe_load(raw_content)

        title = self._parse_title(schema.get('title', ''), schema_file)

        docnodes = [title]

        description = schema.get('description', '')
        if description:
            docnodes.append(schema_header_title(text='Description'))
            docnodes.append(self._parse_description(description, schema_file))

        docnodes.append(schema_header_title(text='Outline'))
        docnodes.append(self._create_toc(schema))

        docnodes.append(section_header(text=SCHEMA_DEF_SECTION_TITLE))
        docnodes.append(self._process_properties(schema))

        examples = schema.get('examples', [])
        if examples:
            docnodes.append(section_header(text=EXAMPLE_SECTION_TITLE))
            docnodes.append(self._process_examples(examples, schema_file))

        docnodes.append(section_header(text=ORIGINAL_SCHEMA_SECTION_TITLE))
        docnodes.append(nodes.literal_block(text=raw_content))

        return docnodes

    def _create_toc(self, schema):

        toc = nodes.compound()
        toc.append(toc_link(text=SCHEMA_DEF_SECTION_TITLE))
        if 'examples' in schema:
            toc.append(toc_link(text=EXAMPLE_SECTION_TITLE))
        toc.append(toc_link(text=ORIGINAL_SCHEMA_SECTION_TITLE))
        return toc

    def _markdown_to_nodes(self, text, filename):
        rst = ViewList()
        for i, line in enumerate(md2rst(text).split('\n')):
            rst.append(line, filename, i+1)

        node = nodes.section()
        node.document = self.state.document

        nested_parse_with_titles(self.state, rst, node)

        return node.children

    def _parse_title(self, title, filename):
        nodes = self._markdown_to_nodes(title, filename)
        return schema_title(None, *nodes)

    def _parse_description(self, description, filename):
        nodes = self._markdown_to_nodes(description, filename)
        return schema_description(None, *nodes)

    def _create_ref_node(self, ref):
        treenodes = asdf_tree()
        treenodes.append(asdf_ref(text=ref))
        return treenodes

    def _process_validation_keywords(self, schema, typename=None):
        node_list = []
        typename = typename or schema['type']

        if typename == 'string':
            if not ('minLength' in schema or 'maxLength' in schema):
                node_list.append(nodes.emphasis(text='No length restriction'))
            if schema.get('minLength', 0):
                text = 'Minimum length: {}'.format(schema['minLength'])
                node_list.append(nodes.line(text=text))
            if 'maxLength' in schema:
                text = 'Maximum length: {}'.format(schema['maxLength'])
                node_list.append(nodes.line(text=text))
            if 'pattern' in schema:
                node_list.append(nodes.line(text='Must match the following pattern:'))
                node_list.append(nodes.literal_block(text=schema['pattern']))

        elif typename == 'array':
            if not ('minItems' in schema or 'maxItems' in schema):
                node_list.append(nodes.emphasis(text='No length restriction'))
            if schema.get('minItems', 0):
                text = 'Minimum length: {}'.format(schema['minItems'])
                node_list.append(nodes.line(text=text))
            if 'maxItems' in schema:
                text = 'Maximum length: {}'.format(schema['maxItems'])
                node_list.append(nodes.line(text=text))

        # TODO: numerical validation keywords

        return node_list

    def _process_top_type(self, schema):
        tree = nodes.compound()
        prop = nodes.compound()
        typename = schema['type']
        prop.append(schema_property_name(text=typename))
        prop.extend(self._process_validation_keywords(schema))
        tree.append(prop)
        return tree

    def _process_properties(self, schema, nodetype=schema_properties):
        if 'properties' in schema:
            treenodes = asdf_tree()
            required = schema.get('required', [])
            for key, node in schema['properties'].items():
                treenodes.append(self._create_top_property(key, node,
                                                           key in required))
            comment = nodes.line(text='This type is an object with the following properties:')
            return nodetype(None, *[comment, treenodes])
        elif 'type' in schema:
            details = self._process_top_type(schema)
            return nodetype(None, details)
        elif 'anyOf' in schema:
            children = self._create_schema_anyof(schema['anyOf'])
            return nodetype(None, *children)
        elif '$ref' in schema:
            comment = nodes.line(text='This schema node is a reference:')
            ref = self._create_ref_node(schema['$ref'])
            return nodetype(None, *[comment, ref])
        # TODO: handle case of top-level allOf
        else:
            text = nodes.emphasis(text='This node has no type definition')
            return nodetype(None, text)

    def _create_schema_anyof(self, items, key=None):
        body = schema_anyof_body(num=len(items))
        for i, tree in enumerate(items):
            body.append(self._process_properties(tree, nodetype=schema_anyof_item))

        text = 'This node must validate against **any** of the following'
        text_nodes = self._markdown_to_nodes(text, '')
        return text_nodes + [body]

    def _create_reference(self, refname):
        return refname + '.html'

    def _create_top_property(self, name, tree, required):

        description = tree.get('description', '')

        if '$ref' in tree:
            # TODO: make the reference a link
            typ = tree.get('$ref')
            ref = self._create_reference(typ)
        else:
            typ = tree.get('type', 'object')
            ref = None

        prop = schema_property()
        prop.append(schema_property_name(text=name))
        prop.append(schema_property_details(typ, required, ref))
        prop.append(self._parse_description(description, ''))
        if typ != 'object':
            prop.extend(self._process_validation_keywords(tree, typename=typ))
        else:
            prop.append(self._process_properties(tree))
        return prop

    def _process_examples(self, tree, filename):
        examples = example_section(num=len(tree))
        for i, example in enumerate(tree):
            node = example_item()
            desc_text = self._markdown_to_nodes(example[0]+':', filename)
            description = example_description(None, *desc_text)
            node.append(description)
            node.append(nodes.literal_block(text=example[1]))
            examples.append(node)
        return examples


def find_autoasdf_directives(env, filename):

    parser = RSTParser()
    settings = OptionParser(components=(RSTParser,)).get_default_values()
    settings.env = env
    document = new_document(filename, settings)

    with open(filename) as ff:
        parser.parse(ff.read(), document)

    return [x.children[0].astext() for x in document.traverse()
            if isinstance(x, schema_def)]


def find_autoschema_references(app, genfiles):

    # We set this environment variable to indicate that the AsdfSchemas
    # directive should be parsed as a simple list of schema references
    # rather than as the toctree that will be generated when the documentation
    # is actually built.
    app.env.autoasdf_generate = True

    schemas = set()
    for fn in genfiles:
        # Create documentation files based on contents of asdf-schema directives
        path = posixpath.join(app.env.srcdir, fn)
        app.env.temp_data['docname'] = app.env.path2doc(path)
        schemas = schemas.union(find_autoasdf_directives(app.env, path))

    # Unset this variable now that we're done.
    app.env.autoasdf_generate = False

    return list(schemas)


def create_schema_docs(app, schemas):

    output_dir = posixpath.join(app.srcdir, 'generated')
    os.makedirs(output_dir, exist_ok=True)

    for schema_name in schemas:
        doc_path = posixpath.join(output_dir, schema_name + '.rst')

        if posixpath.exists(doc_path):
            continue

        os.makedirs(posixpath.dirname(doc_path), exist_ok=True)

        with open(doc_path, 'w') as ff:
            ff.write(schema_name + '\n')
            ff.write('=' * len(schema_name) + '\n\n')
            ff.write('.. asdf-schema::\n\n')
            ff.write('    {}\n'.format(schema_name))


def autogenerate_schema_docs(app):

    env = app.env

    genfiles = [env.doc2path(x, base=None) for x in env.found_docs
                if posixpath.isfile(env.doc2path(x))]

    if not genfiles:
        return

    ext = list(app.config.source_suffix)
    genfiles = [genfile + (not genfile.endswith(tuple(ext)) and ext[0] or '')
                for genfile in genfiles]

    # Read all source documentation files and parse all asdf-schema directives
    schemas = find_autoschema_references(app, genfiles)
    # Create the documentation files that correspond to the schemas listed
    create_schema_docs(app, schemas)


def on_build_finished(app, exc):
    if exc is None:
        for asset in ['asdf_schema.css', 'asdf.js']:
            src = posixpath.join(posixpath.dirname(__file__), asset)
            dst = posixpath.join(app.outdir, '_static')
            copy_asset(src, dst)


def setup(app):

    # Describes a path relative to the sphinx source directory
    app.add_config_value('asdf_schema_path', 'schemas', 'env')
    app.add_directive('asdf-autoschemas', AsdfSchemas)
    app.add_directive('asdf-schema', AsdfSchema)

    add_asdf_nodes(app)

    app.add_css_file('asdf_schema.css')
    app.add_javascript('asdf.js')

    app.connect('builder-inited', autogenerate_schema_docs)
    app.connect('build-finished', on_build_finished)

    return dict(version='0.1')
