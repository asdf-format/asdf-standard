from docutils import nodes
from jinja2 import Environment


template_env = Environment()
anyof_template = template_env.from_string("""
    <ul class="pagination">
        <li class="previous"><a class="page-link" href="#">Previous</a></li>
        {% for ref in hrefs %}
            <li class="page-item">
                <a class="page-link" href="#{{ ref }}">{{ loop.index }}</a>
            </li>
        {% endfor %}
        <li class="next"><a class="page-link" href="#">Next</a></li>
    </ul>
""")


class schema_title(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="schema_title">')

    def depart_html(self, node):
        self.body.append(r'</div>')


class schema_description(nodes.compound):

    def __init__(self, *args, top=False):
        self.top = top
        super().__init__(*args)

    def visit_html(self, node):
        if node.top:
            self.body.append(r'<div class="schema_description"><b>Description:</b>')
        else:
            self.body.append(r'<div class="property_description"')

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


class schema_property(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<li class="schema_property">')

    def depart_html(self, node):
        self.body.append(r'</li>')


class schema_property_name(nodes.line):

    def visit_html(self, node):
        self.body.append(r'<div class="schema_property_name">')

    def depart_html(self, node):
        self.body.append(r'</div>')


class schema_property_details(nodes.compound):

    def __init__(self, typ, required, *args, **kwargs):
        self.typ = typ
        self.required = required
        super().__init__(*args, **kwargs)

    def visit_html(self, node):
        self.body.append(r'<table><tr>')
        self.body.append(r'<td><b>{}</b></td>'.format(node.typ))
        if node.required:
            self.body.append(r'<td><em>Required</em></td>')

    def depart_html(self, node):
        self.body.append(r'</tr></table>')


class schema_anyof_header(nodes.compound):

    def __init__(self, *args, hrefs=[], **kwargs):
        self.hrefs = hrefs
        super().__init__(*args, **kwargs)

    def visit_html(self, node):
        self.body.append(anyof_template.render(hrefs=node.hrefs))

    def depart_html(self, node):
        # Everything is handled by the template
        pass


class schema_anyof_body(nodes.compound):

    def __init__(self, *args, hrefs=[], **kwargs):
        self.hrefs = hrefs
        super().__init__(*args, **kwargs)

    def visit_html(self, node):
        self.body.append(r'<div class="tab-content">')
        for i, ref in enumerate(node.hrefs):
            if i == 0:
                self.body.append(r'<div id={} class="tab-pane fade in active">'.format(ref))
            else:
                self.body.append(r'<div id={} class="tab-pane fade">'.format(ref))
            self.body.append(r'<h3>HEADER {}'.format(i+1))
            self.body.append(r'<p>Some stuff about {}</p>'.format(i+1))
            self.body.append(r'<p>The link here is "{}"'.format(ref))
            self.body.append(r'</div>')

    def depart_html(self, node):
        self.body.append(r'</dev>')


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
    schema_property,
    schema_property_name,
    schema_property_details,
    schema_anyof_header,
    schema_anyof_body,
    asdf_tree,
    asdf_tree_item,
]


__all__ = [klass.__name__ for klass in custom_nodes] + ['add_asdf_nodes']


def add_asdf_nodes(app):

    for node in custom_nodes:
        app.add_node(node, html=(node.visit_html, node.depart_html))
