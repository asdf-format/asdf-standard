# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function

import six

from collections import OrderedDict
import io
import json
import os
import sys
import textwrap

import yaml

from md2rst import md2rst


def write_if_different(filename, data):
    """ Write `data` to `filename`, if the content of the file is different.

    Parameters
    ----------
    filename : str
        The file name to be written to.
    data : bytes
        The data to be written to `filename`.
    """
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    if os.path.exists(filename):
        with open(filename, 'rb') as fd:
            original_data = fd.read()
    else:
        original_data = None

    if original_data != data:
        print("Converting schema {0}".format(
            os.path.basename(filename)))
        with open(filename, 'wb') as fd:
            fd.write(data)


def write_header(o, content, level):
    """
    Write a reStructuredText header to the file.

    Parameters
    ----------
    o : output stream

    content : str
        The content of the header

    level : int
        The level of the header
    """
    levels = '=-~^.'
    if level >= len(levels):
        o.write('**{0}**\n\n'.format(content))
    else:
        o.write(content)
        o.write('\n')
        o.write(levels[level] * len(content))
        o.write('\n\n')


def format_range(var_middle, var_end, minimum, maximum,
                 exclusiveMinimum, exclusiveMaximum):
    """
    Formats an mathematical description of a range, for example, ``0 ≤
    x ≤ 2``.

    Parameters
    ----------
    var_middle : str or None
        The string to put in the middle of an expression, such as
        the ``x`` in ``0 ≤ x ≤ 2``.

    var_end : str or None
        The string to put at one end of a single comparision, such as
        the ``x`` in ``x ≤ 0``.

    minimum : number
        The minimum value.

    maximum : number
        The maximum value.

    exclusiveMinimum : bool
        If `True`, the range excludes the minimum value.

    exclusiveMaximum : bool
        If `True`, the range excludes the maximum value

    Returns
    -------
    expr : str
        The formatted range expression
    """
    if minimum is not None and maximum is not None:
        if minimum == maximum:
            part = '{0} = {1}'.format(var_middle, minimum)
        else:
            part = '{0} '.format(minimum)
            if exclusiveMinimum:
                part += '<'
            else:
                part += '≤'
            part += ' {0} '.format(var_middle)
            if exclusiveMaximum:
                part += '<'
            else:
                part += '≤'
            part += ' {0}'.format(maximum)
    elif minimum is not None:
        if var_end is not None:
            part = '{0} '.format(var_end)
        else:
            part = ''
        if exclusiveMinimum:
            part += '> {0}'.format(minimum)
        else:
            part += '≥ {0}'.format(minimum)
    elif maximum is not None:
        if var_end is not None:
            part = '{0} '.format(var_end)
        else:
            part = ''
        if exclusiveMaximum:
            part += '< {0}'.format(maximum)
        else:
            part += '≤ {0}'.format(maximum)
    else:
        return None
    return part


def format_type(schema, root):
    """
    Creates an English/mathematical description of a schema fragment.

    Parameters
    ----------
    schema : JSON schema fragment

    root : str
        The JSON path to the schema fragment.
    """
    if 'anyOf' in schema:
        return ' :soft:`or` '.join(
            format_type(x, root) for x in schema['anyOf'])

    elif 'allOf' in schema:
        return ' :soft:`and` '.join(
            format_type(x, root) for x in schema['allOf'])

    elif '$ref' in schema:
        ref = schema['$ref']
        if ref.startswith('#/'):
            return ':ref:`{0} <{1}/{2}>`'.format(ref[2:], root, ref[2:])
        else:
            basename = os.path.basename(schema['$ref'])
            # Link references to external schemas; currently used only to
            # linke to JSON Schema itself
            if schema['$ref'].startswith('http:'):
                return '`{0} <{1}>`__'.format(basename, schema['$ref'])
            else:
                return ':doc:`{0} <{1}>`'.format(basename, schema['$ref'])

    else:
        type = schema.get('type')
        if isinstance(type, list):
            parts = [' or '.join(type)]

        elif type is None:
            parts = ['any']

        else:
            parts = [type]

        if type == 'string':
            range = format_range('*len*', '*len*', schema.get('minLength'),
                                 schema.get('maxLength'), False, False)
            if range is not None or 'pattern' in schema or 'format' in schema:
                parts.append('(')
                if range is not None:
                    parts.append(range)
                if 'pattern' in schema:
                    pattern = schema['pattern'].encode('unicode_escape')
                    if six.PY3:
                        pattern = pattern.decode('ascii')
                    parts.append(':soft:`regex` :regexp:`{0}`'.format(pattern))
                if 'format' in schema:
                    parts.append(':soft:`format` {0}'.format(schema['format']))
                parts.append(')')

        elif type in ('integer', 'number'):
            range = format_range('*x*', '', schema.get('minimum'),
                                 schema.get('maximum'),
                                 schema.get('exclusiveMinimum'),
                                 schema.get('exclusiveMaximum'))
            if range is not None:
                parts.append(range)
            # TODO: multipleOf

        elif type == 'object':
            range = format_range('*len*', '*len*', schema.get('minProperties'),
                                 schema.get('maxProperties'), False, False)
            if range is not None:
                parts.append(range)
            # TODO: Dependencies
            # TODO: Pattern properties

        elif type == 'array':
            items = schema.get('items')
            if schema.get('items') and isinstance(items, dict):
                if schema.get('uniqueItems'):
                    parts.append(':soft:`of unique`')
                else:
                    parts.append(':soft:`of`')
                parts.append('(')
                parts.append(format_type(items, root))
                parts.append(')')
            range = format_range('*len*', '*len*', schema.get('minItems'),
                                 schema.get('maxItems'), False, False)
            if range is not None:
                parts.append(range)

        if parts == []:
            parts = 'any'

        if 'enum' in schema:
            parts.append(':soft:`from`')
            parts.append(json.dumps(schema['enum']))

        return ' '.join(parts)


def reindent(content, indent):
    """
    Reindent a string to the given number of spaces.
    """
    content = textwrap.dedent(content)
    lines = []
    for line in content.split('\n'):
        lines.append(indent + line)
    return '\n'.join(lines)


def recurse(o, name, schema, path, level, required=False):
    """
    Convert a schema fragment to reStructuredText.

    Parameters
    ----------
    o : output stream

    name : str
        Name of the entry

    schema : schema fragment

    path : list of str
        Path to schema fragment

    level : int
        Indentation level

    required : bool
        If `True` the entry is required by the schema and will be
        documented as such.
    """
    indent = '  ' * max(level, 0)

    o.write('\n\n')
    o.write(indent)
    o.write('.. _{0}:\n\n'.format(os.path.join(*path)))
    if level == 0:
        write_header(o, name, level)
    else:
        if name != 'items':
            o.write(indent)
            o.write(':entry:`{0}`\n\n'.format(name))

    o.write(indent)
    o.write(":soft:`Type:` ")
    o.write(format_type(schema, path[0]))
    o.write('.')
    if required:
        o.write(' Required.')
    o.write('\n\n')

    o.write(reindent(md2rst(schema.get('title', '')), indent))
    o.write('\n\n')

    o.write(reindent(md2rst(schema.get('description', '')), indent))
    o.write('\n\n')

    if 'default' in schema:
        o.write(indent)
        o.write(':soft:`Default:` {0}'.format(
            json.dumps(schema['default'])))
        o.write('\n\n')

    if 'definitions' in schema:
        o.write(indent)
        o.write(":category:`Definitions:`\n\n")
        for key, val in schema['definitions'].items():
            recurse(o, key, val, path + ['definitions', key], level + 1)

    if 'anyOf' in schema and len(schema['anyOf']) > 1:
        o.write(indent)
        o.write(':category:`Any of:`\n\n')
        for i, subschema in enumerate(schema['anyOf']):
            recurse(o, '—', subschema, path + ['anyOf', str(i)], level + 1)

    elif 'allOf' in schema and len(schema['allOf']) > 1:
        o.write(indent)
        o.write(':category:`All of:`\n\n')
        for i, subschema in enumerate(schema['allOf']):
            recurse(o, i, subschema, path + ['allOf', str(i)], level + 1)

    if schema.get('type') == 'object':
        if len(schema.get('properties', {})):
            o.write(indent)
            o.write(':category:`Properties:`\n\n')
            for key, val in schema.get('properties', {}).items():
                if key == '$ref':
                    continue
                recurse(o, key, val, path + ['properties', key], level + 1,
                        key in schema.get('required', []))

    elif schema.get('type') == 'array':
        o.write(indent)
        o.write(':category:`Items:`\n\n')
        items = schema.get('items')
        if isinstance(items, dict):
            recurse(o, 'items', items, path + ['items'], level + 1)
        elif isinstance(items, list):
            for i, val in enumerate(items):
                name = 'index[{0}]'.format(i)
                recurse(o, name, val, path + [str(i)], level + 1)

    if schema.get('examples'):
        o.write(indent)
        o.write(":category:`Examples:`\n\n")
        for description, example in schema['examples']:
            o.write(reindent(md2rst(description + "::\n\n"), indent))
            o.write(reindent(example, indent + '  '))
            o.write('\n\n')


def convert_schema_to_rst(src, dst):
    """
    Convert a YAML schema to reStructuredText.
    """
    with open(src, 'rb') as fd:
        schema = yaml.safe_load(fd)
    with open(src, 'rb') as fd:
        yaml_content = fd.read()

    if schema.get('$schema') not in (
            "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0",
            "http://stsci.edu/schemas/yaml-schema/draft-01",
            "http://json-schema.org/draft-04/schema"):
        return

    o = io.StringIO()

    id = schema.get('id', '#')
    name = os.path.basename(src[:-5])
    name = name[:name.rfind('-')]
    if 'title' in schema:
        name += ': ' + schema['title'].strip()
    recurse(o, name, schema, [id], 0)

    write_header(o, 'Original schema in YAML', 1)
    o.write(".. only:: html\n\n   :download:`[Download raw] <{0}>`\n".format(
        os.path.basename(src)))
    o.write(".. literalinclude:: {0}\n".format(os.path.basename(dst)))
    o.write("    :language: yaml\n")
    o.write("    :linenos:\n\n")

    write_if_different(dst, yaml_content)
    write_if_different(dst[:-5] + ".rst", o.getvalue().encode('utf-8'))


def construct_mapping(self, node, deep=False):
    """
    Make sure the properties are written out in the same order as the
    original file.
    """
    if not isinstance(node, yaml.MappingNode):
        raise yaml.constructor.ConstructorError(None, None,
                "expected a mapping node, but found %s" % node.id,
                node.start_mark)
    mapping = OrderedDict()
    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        try:
            hash(key)
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                "found unacceptable key (%s)" % exc, key_node.start_mark)
        value = self.construct_object(value_node, deep=deep)
        mapping[key] = value
    return mapping


yaml.SafeLoader.add_constructor(
    'tag:yaml.org,2002:map', construct_mapping)


def main(src, dst):
    for root, dirs, files in os.walk(src):
        for fname in files:
            if not fname.endswith(".yaml"):
                continue
            src_path = os.path.join(root, fname)
            dst_path = os.path.join(
                dst, os.path.relpath(src_path, src))

            convert_schema_to_rst(src_path, dst_path)


def decode_filename(fname):
    if six.PY3:
        return fname
    else:
        return fname.decode(sys.getfilesystemencoding())


if __name__ == '__main__':
    src = decode_filename(sys.argv[-2])
    dst = decode_filename(sys.argv[-1])

    sys.exit(main(src, dst))
