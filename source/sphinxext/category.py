# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function


from docutils import nodes


class category(nodes.Element):
    pass


def category_role(name, rawtext, text, lineno, inliner,
                  options={}, content=[]):
    node = category(text)
    return [node], []


def visit_category_node_html(self, node):
    self.body.append('<span class="category">')
    self.body.append(node.rawsource)


def depart_category_node_html(self, node):
    self.body.append('</span>')


def visit_category_node_latex(self, node):
    self.body.append('\n\n\\textsf{%s}' % node.rawsource)


def depart_category_node_latex(self, node):
    pass


class soft(nodes.Element):
    pass


def soft_role(name, rawtext, text, lineno, inliner,
                  options={}, content=[]):
    node = soft(text)
    return [node], []


def visit_soft_node_html(self, node):
    self.body.append('<span class="soft">')
    self.body.append(node.rawsource)


def depart_soft_node_html(self, node):
    self.body.append('</span>')


def visit_soft_node_latex(self, node):
    self.body.append('\\textcolor[gray]{0.5}{%s}' % node.rawsource)


def depart_soft_node_latex(self, node):
    pass


def setup(app):
    app.add_node(
        category,
        html=(visit_category_node_html, depart_category_node_html),
        latex=(visit_category_node_latex, depart_category_node_latex)
    )

    app.add_role(
        'category', category_role)

    app.add_node(
        soft,
        html=(visit_soft_node_html, depart_soft_node_html),
        latex=(visit_soft_node_latex, depart_soft_node_latex)
    )

    app.add_role(
        'soft', soft_role)
