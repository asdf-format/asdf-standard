import posixpath

from docutils import nodes

from sphinx import addnodes
from sphinx.util.docutils import SphinxDirective


class AsdfSchemas(SphinxDirective):

    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self):

        dirname = posixpath.dirname(self.env.docname)
        schema_path = self.state.document.settings.env.config.asdf_schema_path

        schemas = [x.strip().split()[0] for x in self.content]

        source_path = posixpath.join(dirname, 'hello')

        tocnode = addnodes.toctree()
        tocnode['includefiles'] = [source_path]
        tocnode['entries'] = [(name, source_path) for name in schemas]
        tocnode['maxdepth'] = -1
        tocnode['glob'] = None

        paragraph = nodes.paragraph(text="Here's where the schemas go")
        return [paragraph, tocnode]


def find_autoasdf_directives(filename):

    return []


def autogenerate_schema_docs(app):

    # Read all source files

    # Look for all 'asdf-schema' directives and parse arguments

    # 

    schema_path = app.env.config.asdf_schema_path
    schema_path = posixpath.join(app.env.srcdir, schema_path)

    genfiles = [env.doc2path(x, base=None) for x in env.found_docs
                if os.path.isfile(env.doc2path(x))]

    if not genfiles:
        return

    ext = list(app.config.source_suffix)
    genfiles = [genfile + (not genfile.endswith(tuple(ext)) and ext[0] or '')
                for genfile in genfiles]

    for fn in genfiles:
        # Look for asdf-schema directive
        # Create documentation files based on contents of such directives
        schemas = find_autoasdf_directives(fn)

    with open(posixpath.join(app.srcdir, 'schemas', 'hello.rst'), 'w') as ff:
        ff.write('MY TITLE\n')
        ff.write('========\n')
        ff.write('HEY THERE\n')


def setup(app):

    # Describes a path relative to the sphinx source directory
    app.add_config_value('asdf_schema_path', 'schemas', 'env')
    app.add_directive('asdf-schemas', AsdfSchemas)

    app.connect('builder-inited', autogenerate_schema_docs)

    return dict(version='0.1')
