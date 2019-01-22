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


def autogenerate_schema_docs(app):

    with open(posixpath.join(app.srcdir, 'schemas', 'hello.rst'), 'w') as ff:
        ff.write('MY TITLE\n')
        ff.write('========\n')
        ff.write('HEY THERE\n')


def setup(app):

    app.add_config_value('asdf_schema_path', 'schemas', 'env')
    app.add_directive('asdf-schemas', AsdfSchemas)

    app.connect('builder-inited', autogenerate_schema_docs)

    return dict(version='0.1')
