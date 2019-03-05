from docutils import nodes
from jinja2 import Environment


template_env = Environment()
carousel_header_template = template_env.from_string("""
    <div class="{{ top_class }}">
    {% if title %}
      <h3>{{ title }}</h3>
    {% endif %}
      <div id="{{ carousel_name }}" class="carousel slide" data-interval="false" data-wrap="false">
        <ol class="carousel-indicators">
        {% for i in range(num) %}
            <li class="{{ top_class }}-indicator" data-target="#{{ carousel_name }}" data-slide-to="{{ i }}"></li>
        {% endfor %}
        </ol>
        <div class="carousel-inner">
""")


carousel_control_template = template_env.from_string("""
  <a class="left carousel-control" href="#{{ carousel_name }}" role="button" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left black" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </a>
  <a class="right carousel-control" href="#{{ carousel_name }}" role="button" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right black" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </a>
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
        self.body.append(r'<div class="schema_properties"><h3>Schema Definition</h3>')

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


class asdf_ref(nodes.line):

    def visit_html(self, node):
        self.body.append(r'<div class="asdf_ref">')

    def depart_html(self, node):
        self.body.append(r'</div>')


class carousel_section(nodes.compound):
    carousel_name = ''
    top_class = ''
    title = ''
    description = ''

    def __init__(self, *args, num=0, **kwargs):
        self.num = num
        super().__init__(*args, **kwargs)

    def visit_html(self, node):
        self.body.append(carousel_header_template.render(
            top_class=node.top_class,
            carousel_name=node.carousel_name,
            title=node.title,
            description=node.description,
            num=node.num))

    def depart_html(self, node):
        self.body.append(r'</div>')
        self.body.append(carousel_control_template.render(
            carousel_name=node.carousel_name))
        self.body.append(r'</div></div>')


class example_section(carousel_section):
    carousel_name = 'schemaExampleCarousel'
    top_class = 'example-section'
    title = 'Examples'


class example_item(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="item example-item">')

    def depart_html(self, node):
        self.body.append(r'</div>')

class example_description(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="example-description">')

    def depart_html(self, node):
        self.body.append(r'</div>')


class schema_anyof_carousel(carousel_section):
    carousel_name = 'anyofCarousel'
    top_class = 'anyof-carousel'


class schema_anyof_item(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="item anyof-item">')

    def depart_html(self, node):
        self.body.append(r'</div>')


custom_nodes = [
    schema_title,
    schema_description,
    schema_properties,
    schema_property,
    schema_property_name,
    schema_property_details,
    schema_anyof_carousel,
    schema_anyof_item,
    asdf_tree,
    asdf_tree_item,
    asdf_ref,
    example_section,
    example_item,
    example_description,
]


__all__ = [klass.__name__ for klass in custom_nodes] + ['add_asdf_nodes']


def add_asdf_nodes(app):

    for node in custom_nodes:
        app.add_node(node, html=(node.visit_html, node.depart_html))
