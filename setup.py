#!/usr/bin/env python3

from setuptools import setup, find_packages

from plistyamlplist_lib.version import __version__

VERSION = __version__

setup(
    name="plistyamlplist",
    version=VERSION,
    packages=find_packages(include=["plistyamlplist_lib", "plistyamlplist_lib.*"]),
    install_requires=["ruamel.yaml"],
)
