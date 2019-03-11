from docutils import nodes
from jinja2 import Environment


template_env = Environment()
carousel_header_template = template_env.from_string("""
    <div class="{{ top_class }}">
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

headerlink_template = template_env.from_string("""
  <a class="headerlink" name="{{ name }}" href="#{{ name }}" title="{{ title }}">¶</a>
    """)


class schema_title(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="schema_title">')

    def depart_html(self, node):
        self.body.append(r'</div>')


class toc_link(nodes.line):

    def visit_html(self, node):
        text = node[0].title()
        self.body.append('<a class="toc-link" href="#{}">'.format(text))

    def depart_html(self, node):
        self.body.append('</a>')


class schema_header_title(nodes.line):

    def visit_html(self, node):
        self.body.append('<h4>')

    def depart_html(self, node):
        self.body.append('</h4>')


class schema_description(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<div class="property_description"')

    def depart_html(self, node):
        self.body.append(r'</div>')


class section_header(nodes.line):

    def visit_html(self, node):
        self.body.append(r'<h3 class="section-header">')

    def depart_html(self, node):
        self.body.append(headerlink_template.render(name=node[0].title()))
        self.body.append(r'</h3>')


class schema_properties(nodes.compound):
    def visit_html(self, node):
        self.body.append(r'<div class="schema_properties">')

    def depart_html(self, node):
        self.body.append(r'</div>')


class schema_property(nodes.compound):

    def visit_html(self, node):
        self.body.append(r'<li class="list-group-item">')

    def depart_html(self, node):
        self.body.append(r'</li>')


class schema_property_name(nodes.line):

    def visit_html(self, node):
        self.body.append(r'<div class="schema_property_name">')

    def depart_html(self, node):
        self.body.append(r'</div>')


class schema_property_details(nodes.compound):

    def __init__(self, typ, required, ref=None, *args, **kwargs):
        self.typ = typ
        self.ref = ref
        self.required = required
        super().__init__(*args, **kwargs)

    def visit_html(self, node):
        self.body.append(r'<table><tr>')
        self.body.append('<td><b>')
        if node.ref is not None:
            self.body.append('<a href={}>{}</a>'.format(node.ref, node.typ))
        else:
            self.body.append(node.typ)
        self.body.append('</b></td>')
        if node.required:
            self.body.append(r'<td><em>Required</em></td>')

    def depart_html(self, node):
        self.body.append(r'</tr></table>')


class asdf_tree(nodes.bullet_list):

    def visit_html(self, node):
        self.body.append(r'<ul class="list-group">')

    def depart_html(self, node):
        self.body.append(r'</ul>')


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


class schema_combiner_body(nodes.bullet_list):

    def visit_html(self, node):
        self.body.append('<ul class="combiner-list">')

    def depart_html(self, node):
        self.body.append('</ul>')


class schema_combiner_item(nodes.list_item):

    def visit_html(self, node):
        self.body.append('<li class="combiner-list-item">')

    def depart_html(self, node):
        self.body.append('</li>')


custom_nodes = [
    schema_title,
    toc_link,
    schema_header_title,
    schema_description,
    schema_properties,
    schema_property,
    schema_property_name,
    schema_property_details,
    schema_combiner_body,
    schema_combiner_item,
    section_header,
    asdf_tree,
    asdf_ref,
    example_section,
    example_item,
    example_description,
]


__all__ = [klass.__name__ for klass in custom_nodes] + ['add_asdf_nodes']


def add_asdf_nodes(app):

    for node in custom_nodes:
        app.add_node(node, html=(node.visit_html, node.depart_html))
