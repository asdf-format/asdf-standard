#!/usr/bin/env python

import os
import re
import subprocess as sp
import sys


def get_schemas(pattern):

    cmd = ["git", "grep", "--name-only"]
    output = sp.check_output(cmd + [pattern, "--", "schemas"]).decode("utf8")
    names = output.split()
    print(names)

    dedupe = dict()

    for name in names:
        version = re.findall(r"\d\.\d.\d", name)[0]
        basepath = name.split("-")[0]
        if basepath in dedupe and dedupe[basepath] > version:
            continue

        dedupe[basepath] = version

    return [f"{x}-{y}.yaml" for x, y in dedupe.items()]


def update_version(string):

    groups = re.search(r"((\d)\.(\d)\.(\d))", string).groups()
    bumped = int(groups[2]) + 1

    new_version = f"{groups[1]}.{bumped}.{groups[3]}"
    return re.sub(r"((\d)\.(\d)\.(\d))", new_version, string)


def create_updated_schema(schema, pattern, new_pattern):

    name = os.path.splitext(os.path.basename(schema))[0]
    updated = update_version(name)
    new_schema = re.sub(name, updated, schema)

    with open(new_schema, "w") as new_file:
        with open(schema) as old_file:
            for line in old_file:
                line = line.replace(pattern, new_pattern)
                line = line.replace(name, updated)
                new_file.write(line)


def main():

    if len(sys.argv) != 2:
        name = os.path.basename(sys.argv[0])
        sys.stderr.write(f"USAGE: {name} <pattern>\n")
        exit(1)

    pattern = sys.argv[1]
    new_pattern = update_version(pattern)
    schemas = get_schemas(pattern)

    for s in schemas:
        create_updated_schema(s, pattern, new_pattern)


if __name__ == "__main__":
    main()
