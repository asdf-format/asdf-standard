# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function

from collections import OrderedDict
import io
import json
import os
import sys
import textwrap

import yaml


def write_if_different(filename, data):
    """ Write `data` to `filename`, if the content of the file is different.

    Parameters
    ----------
    filename : str
        The file name to be written to.
    data : bytes
        The data to be written to `filename`.
    """
    data = data.encode('utf-8')

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
    if minimum is not None and maximum is not None:
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


def format_type(schema):
    if 'anyOf' in schema:
        return ' :soft:`or` '.join(format_type(x) for x in schema['anyOf'])
    elif 'allOf' in schema:
        return ' :soft:`and` '.join(format_type(x) for x in schema['allOf'])
    elif '$ref' in schema:
        basename = os.path.basename(schema['$ref'])
        return ':ref:`{0} <{1}>`'.format(basename, schema['$ref'])
    elif 'type' in schema:
        if isinstance(schema['type'], list):
            parts = [' or '.join(schema['type'])]
        else:
            parts = [schema['type']]
        if schema['type'] == 'string':
            range = format_range('*len*', '*len*', schema.get('minLength'),
                                 schema.get('maxLength'), False, False)
            if range is not None:
                parts.append(range)
            if 'pattern' in schema:
                parts.append('(:soft:`regex` :regexp:`{0}`)'.format(
                    schema['pattern'].encode('unicode_escape').replace(
                        '\\', '\\\\')))
            if 'format' in schema:
                parts.append('({0})'.format(schema['format']))
        elif schema['type'] in ('integer', 'number'):
            range = format_range('*x*', '', schema.get('minimum'),
                                 schema.get('maximum'),
                                 schema.get('exclusiveMinimum'),
                                 schema.get('exclusiveMaximum'))
            if range is not None:
                parts.append(range)
            # TODO: multipleOf
        elif schema['type'] == 'object':
            range = format_range('*len*', '*len*', schema.get('minProperties'),
                                 schema.get('maxProperties'), False, False)
            if range is not None:
                parts.append(range)
            # TODO: Dependencies
            # TODO: Pattern properties
        elif schema['type'] == 'array':
            items = schema.get('items')
            if schema.get('items') and isinstance(items, dict):
                if schema.get('uniqueItems'):
                    parts.append(':soft:`of unique`')
                else:
                    parts.append(':soft:`of`')
                parts.append(format_type(items))
            range = format_range('*len*', '*len*', schema.get('minItems'),
                                 schema.get('maxItems'), False, False)
            if range is not None:
                parts.append(range)

        if 'enum' in schema:
            parts.append(':soft:`from`')
            parts.append(json.dumps(schema['enum']))

        return ' '.join(parts)
    else:
        return ''


def reindent(content, indent):
    content = textwrap.dedent(content)
    lines = []
    for line in content.split('\n'):
        lines.append(indent + line)
    return '\n'.join(lines)


def recurse(o, name, schema, path, level, required=False):
    indent = '  ' * max(level, 0)

    o.write('\n\n')
    o.write(indent)
    o.write('.. _{0}:\n\n'.format(os.path.join(*path)))
    if level == 0:
        write_header(o, name, level)
    else:
        if name != 'items':
            o.write(indent)
            o.write(':category:`{0}`\n\n'.format(name))

    o.write(indent)
    o.write(":soft:`Type:` ")
    o.write(format_type(schema))
    o.write('.')
    if required:
        o.write(' Required.')
    o.write('\n\n')

    o.write(reindent(schema.get('title', ''), indent))
    o.write('\n\n')

    o.write(reindent(schema.get('description', ''), indent))
    o.write('\n\n')

    if 'default' in schema:
        o.write(indent)
        o.write(':soft:`Default:` {0}'.format(
            json.dumps(schema['default'])))
        o.write('\n\n')

    if schema.get('type') == 'object':
        o.write(indent)
        o.write(':category:`Properties:`\n\n')
        for key, val in schema.get('properties', {}).items():
            recurse(o, key, val, path + [key], level + 1,
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
                recurse(o, name, val, path + [name], level + 1)

    if 'examples' in schema:
        o.write(":category:`Examples:`\n\n")
        for description, example in schema['examples']:
            o.write(reindent(description + "::\n\n", indent))
            o.write(reindent(example, indent + '  '))
            o.write('\n\n')


def convert_schema_to_rst(src, dst):
    with open(src, 'rb') as fd:
        schema = yaml.safe_load(fd)
    with open(src, 'rb') as fd:
        yaml_content = fd.read()

    o = io.StringIO()

    id = schema.get('id', '#')
    name = os.path.basename(src[:-5])
    if 'title' in schema:
        name += ': ' + schema['title'].strip()
    recurse(o, name, schema, [id], 0)

    o.write(".. only:: html\n\n   :download:`Original schema in YAML <{0}>`\n".format(
        os.path.basename(src)))

    write_if_different(dst, yaml_content)
    write_if_different(dst[:-5] + ".rst", o.getvalue())


def construct_mapping(self, node, deep=False):
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


# TODO: Preserve ordering of dictionaries from original file


if __name__ == '__main__':
    src = sys.argv[-2].decode(sys.getfilesystemencoding())
    dst = sys.argv[-1].decode(sys.getfilesystemencoding())

    for root, dirs, files in os.walk(src):
        for fname in files:
            if not fname.endswith(".yaml"):
                continue
            src_path = os.path.join(root, fname)
            dst_path = os.path.join(
                dst, os.path.relpath(src_path, src))

            convert_schema_to_rst(src_path, dst_path)
