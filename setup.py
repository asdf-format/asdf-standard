#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

packages = find_packages(where="src")
packages.append("asdf_standard.resources")

package_dir = {
    "": "src",
    "asdf_standard.resources": "resources",
}


def package_yaml_files(directory):
    paths = sorted(Path(directory).rglob("*.yaml"))
    return [str(p.relative_to(directory)) for p in paths]


package_data = {
    "asdf_standard.resources": package_yaml_files("resources"),
}

setup(
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
)
