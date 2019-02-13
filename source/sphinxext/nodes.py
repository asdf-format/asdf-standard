from docutils import nodes


class schema_title(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="schema_title">')

    def depart_html(self, node):
        self.body.append(r'</div>')


class schema_description(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="schema_description"><b>Description:</b>')

    def depart_html(self, node):
        self.body.append(r'</div>')


class schema_properties(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="schema_properties"><h3>Properties</h3>')
        self.body.append(r'<p>{}</p>'.format(
            "These are the top-level properties for this schema"
        ))

    def depart_html(self, node):
        self.body.append(r'</div>')


class asdf_tree(nodes.bullet_list):

    def visit_html(self, node):
        self.body.append(r'<ul class="asdf_tree">')

    def depart_html(self, node):
        self.body.append(r'</ul>')


class asdf_tree_item(nodes.line):

    def visit_html(self, node):
        self.body.append(r'<li class="asdf_tree_item">')

    def depart_html(self, node):
        self.body.append(r'</li>')


custom_nodes = [
    schema_title,
    schema_description,
    schema_properties,
    asdf_tree,
    asdf_tree_item,
]


__all__ = [klass.__name__ for klass in custom_nodes] + ['add_asdf_nodes']


def add_asdf_nodes(app):

    for node in custom_nodes:
        app.add_node(node, html=(node.visit_html, node.depart_html))
