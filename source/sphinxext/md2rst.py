# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

"""
Implements a markdown to reST converter using the mistune markdown
parser.
"""

import re
import textwrap

import mistune


class BlockLexer(mistune.BlockLexer):
    # Adds math support

    def __init__(self, *args, **kwargs):
        super(BlockLexer, self).__init__(*args, **kwargs)
        self.enable_math()

    def enable_math(self):
        self.rules.block_math = re.compile(r'^\$\$(.*?)\$\$', re.DOTALL)
        self.default_rules = ['block_math'] + mistune.BlockLexer.default_rules

    def parse_block_math(self, m):
        self.tokens.append({
            'type': 'block_math',
            'text': m.group(1)
        })


class Markdown(mistune.Markdown):
    def output_block_math(self):
        return self.renderer.block_math(self.token['text'])


class InlineLexer(mistune.InlineLexer):
    # Adds math support

    default_rules = ['math'] + mistune.InlineLexer.default_rules

    def __init__(self, *args, **kwargs):
        super(InlineLexer, self).__init__(*args, **kwargs)
        self.enable_math()

    def enable_math(self):
        self.rules.text = re.compile(
            r'^[\s\S]+?(?=[\\<!\[_*`~$]|https?://| {2,}\n|$)')
        self.rules.math = re.compile(r'^\$(.+?)\$')
        self.default_rules = ['math'] + mistune.InlineLexer.default_rules

    def output_math(self, m):
        return self.renderer.math(m.group(1))


class RstRenderer(object):
    """The default HTML renderer for rendering Markdown.
    """
    def __init__(self, **kwargs):
        self.options = kwargs
        self.levels = kwargs.get('levels', '*=-^"+:~')

    def _indented(self, content):
        content = textwrap.dedent(content)
        return '\n'.join('   ' + line for line in content.split('\n'))

    def _directive(self, name, content, args=[], attributes={}):
        out = '.. %s:: %s\n' % (name, ', '.join(args))
        for key, val in attributes.items():
            out += '    :%s: %s\n' % (key, val)
        out += '\n'
        out += self._indented(content)
        out += '\n\n'
        return out

    def placeholder(self):
        return ''

    def block_code(self, code, lang=None):
        code = code.rstrip('\n')
        if lang:
            langs = lang
        else:
            langs = []
        return self._directive('code', code, langs)

    def block_quote(self, text):
        return self._indented(text)

    def block_html(self, html):
        if self.options.get('skip_html'):
            return ''
        return self._directive('raw', html, ['html'])

    def header(self, text, level, raw=None):
        return '%s\n%s\n\n' % (text, self.levels[level] * len(text))

    def hrule(self):
        return '\n\n--------\n\n'

    def list(self, body, ordered=True):
        if ordered:
            body = ('\n' + body).replace('\n- ', '\n#.')
        return body

    def list_item(self, text):
        return textwrap.fill(
            text, initial_indent='-  ', subsequent_indent='   ') + '\n\n'

    def paragraph(self, text):
        return '%s\n\n' % text

    def table(self, header, body):
        raise NotImplementedError()

    def table_row(self, content):
        raise NotImplementedError()

    def table_cell(self, content, **flags):
        raise NotImplementedError()

    def double_emphasis(self, text):
        return '**%s**' % text

    def emphasis(self, text):
        return '*%s*' % text

    def codespan(self, text):
        return ':code:`%s`' % text

    def linebreak(self):
        return ''

    def strikethrough(self, text):
        return text

    def text(self, text):
        return text

    def autolink(self, link, is_email=False):
        text = link
        if is_email:
            link = 'mailto:%s' % link
        if link.startswith('ref:'):
            return ':ref:`%s <%s>`' % (text, link[4:])
        return '`%s <%s>`__' % (text, link)

    def link(self, link, title, text):
        if link.startswith('javascript:'):
            link = ''
        if link.startswith('ref:'):
            return ':ref:`%s <%s>`' % (text, link[4:])
        return '`%s <%s>`__' % (text, link)

    def image(self, src, title, text):
        if src.startswith('javascript:'):
            src = ''
        options = {}
        if text:
            options['alt'] = text
        return self._directive('image', '', [src], options)

    def tag(self, html):
        if self.options.get('skip_html'):
            return ''
        return ":raw:`%s`" % html

    def newline(self):
        return ''

    def footnote_ref(self, key, index):
        raise NotImplementedError()

    def footnote_item(self, key, text):
        raise NotImplementedError()

    def footnotes(self, text):
        raise NotImplementedError()

    def math(self, text):
        return ':math:`%s`' % text

    def block_math(self, text):
        return self._directive('math', text)


def md2rst(content):
    """
    Convert the given string in markdown to a string of reST.
    """
    renderer = RstRenderer()
    md = Markdown(
        block=BlockLexer, inline=InlineLexer, renderer=renderer)
    return md.render(content)
