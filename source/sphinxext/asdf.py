from docutils import nodes
from docutils.parsers.rst import Directive


class AsdfSchema(Directive):
    def run(self):

        schema_path = self.state.document.settings.env.config.asdf_schema_path

        paragraph = nodes.paragraph(text="Here's where the schemas go")
        return [paragraph]


def setup(app):

    app.add_config_value('asdf_schema_path', 'schemas', 'env')
    app.add_config_value('floobyfloob', True, 'env')
    app.add_directive('asdf-schemas', AsdfSchema)

    return dict(version='0.1')
