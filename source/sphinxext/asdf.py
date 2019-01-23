import os
import posixpath

from docutils import nodes
from docutils.frontend import OptionParser

from sphinx import addnodes
from sphinx.parsers import RSTParser
from sphinx.util.docutils import SphinxDirective, new_document


class schema_def(nodes.comment):
    pass


class AsdfSchemas(SphinxDirective):

    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def _process_asdf_toctree(self):

        dirname = posixpath.dirname(self.env.docname)
        schema_path = self.state.document.settings.env.config.asdf_schema_path
        srcdir = self.state.document.settings.env.srcdir

        schemas = [x.strip().split()[0] for x in self.content]

        links = []
        for name in self.content:
            schema = self.env.path2doc(name.strip().split()[0])
            link = posixpath.join('generated', schema)
            links.append((schema, link))

        from IPython import embed; embed()

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


def find_autoasdf_directives(env, filename):

    parser = RSTParser()
    settings = OptionParser(components=(RSTParser,)).get_default_values()
    settings.env = env
    document = new_document(filename, settings)

    with open(filename) as ff:
        parser.parse(ff.read(), document)

    return [x.children[0].astext() for x in document.traverse()
            if isinstance(x, schema_def)]


def create_schema_doc(schema_name, doc_path):

    os.makedirs(posixpath.dirname(doc_path), exist_ok=True)

    with open(doc_path, 'w') as ff:
        ff.write(schema_name + '\n')
        ff.write('=' * len(schema_name) + '\n')
        ff.write('Your message here\n')


def autogenerate_schema_docs(app):

    # Read all source files

    # Look for all 'asdf-schema' directives and parse arguments

    # 

    env = app.env

    schema_path = env.config.asdf_schema_path
    schema_path = posixpath.join(env.srcdir, schema_path)

    genfiles = [env.doc2path(x, base=None) for x in env.found_docs
                if posixpath.isfile(env.doc2path(x))]

    if not genfiles:
        return

    ext = list(app.config.source_suffix)
    genfiles = [genfile + (not genfile.endswith(tuple(ext)) and ext[0] or '')
                for genfile in genfiles]

    env.autoasdf_generate = True

    schemas = set()
    for fn in genfiles:
        # Create documentation files based on contents of asdf-schema directives
        path = posixpath.join(env.srcdir, fn)
        app.env.temp_data['docname'] = env.path2doc(path)
        schemas = schemas.union(find_autoasdf_directives(app.env, path))

    output_dir = posixpath.join(app.srcdir, 'generated')
    os.makedirs(output_dir, exist_ok=True)

    for s in schemas:
        realpath = posixpath.join(output_dir, s)
        if posixpath.exists(realpath):
            continue
        create_schema_doc(s, realpath)

    env.autoasdf_generate = False


def setup(app):

    # Describes a path relative to the sphinx source directory
    app.add_config_value('asdf_schema_path', 'schemas', 'env')
    app.add_directive('asdf-schemas', AsdfSchemas)

    app.connect('builder-inited', autogenerate_schema_docs)

    return dict(version='0.1')
