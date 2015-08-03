# Script to update the old versioning approach to the new one.
# Should be removed eventually.

import os
import re

root = './schemas/stsci.edu/asdf/0.1.0/'
for module in os.listdir(root) + ['.']:
    module_path = os.path.join(root, module)
    if not os.path.isdir(module_path):
        continue

    for filename in os.listdir(module_path):
        old_filepath = os.path.join(module_path, filename)
        if not os.path.isfile(old_filepath):
            continue
        new_filepath = os.path.join(
            './schemas/stsci.edu/asdf/', module, os.path.splitext(filename)[0] + '-0.1.0.yaml')

        with open(old_filepath, 'rb') as fd:
            content = fd.read()

        content = re.sub(
            r'[\'"]tag:stsci.edu:asdf/0\.1\.0/(?P<path>.*)[\'"]',
            r'"tag:stsci.edu:asdf/\g<path>-0.1.0"',
            content)

        content = re.sub(
            r'[\'"]http://stsci.edu/schemas/asdf/0\.1\.0/(?P<path>.*)[\'"]',
            r'"http://stsci.edu/schemas/asdf/\g<path>-0.1.0"',
            content)

        content = re.sub(
            r'!(?P<name>\S+)',
            r'!\g<name>-0.1.0',
            content)

        def ref_repl(match):
            name = match.groupdict('').get('name', '')
            anchor = match.groupdict('').get('anchor', '')
            if name:
                return '$ref: "{0}-0.1.0{1}"\n'.format(name, anchor)
            else:
                return '$ref: "{0}"\n'.format(anchor)

        content = re.sub(
            r'\$ref: (?P<q1>[\'"]?)(?P<name>\S*?)(?P<anchor>#\S+?)?(?P<q2>[\'"]?)\n',
            ref_repl,
            content)

        content = re.sub(
            'draft-01-0\.1\.0',
            'draft-01',
            content)

        new_dirpath = os.path.dirname(new_filepath)
        if not os.path.isdir(new_dirpath):
            os.makedirs(new_dirpath)
        with open(new_filepath, 'wb') as fd:
            fd.write(content)


for root, dirs, files in os.walk('source'):
    for filename in files:
        if not filename.endswith('.rst'):
            continue

        filepath = os.path.join(root, filename)

        with open(filepath, 'rb') as fd:
            content = fd.read()

        content = re.sub(
            r'stsci\.edu/asdf/0\.1\.0/(?P<name>\S+?)\.rst',
            r'stsci.edu/asdf/\g<name>-0.1.0.rst',
            content)

        content = re.sub(
            r'<http://stsci.edu/schemas/asdf/0\.1\.0/(?P<path>.*?)>',
            r'<http://stsci.edu/schemas/asdf/\g<path>-0.1.0>',
            content)

        with open(filepath, 'wb') as fd:
            fd.write(content)
