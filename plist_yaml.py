#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
If this script is run directly, it takes an input file and an output file from
the command line. The input file must be in PLIST format.
The output file will be in YAML format:

plist_yaml.py <input-file> <output-file>

The output file can be omitted. In this case, the name of the output file is
taken from the input file, with .yaml added to the end.
"""

import sys
from os import path
from plistlib import Data, readPlist

import yaml


def normalize_types(input):
    """
    This allows YAML and JSON to store Data fields as strings. However, this
    operation is irreversible.  Only use if read-only access to the plist is
    required.
    """
    if isinstance(input, Data): return input.data
    if isinstance(input, list):
        retval = []
        for child in input:
            retval.append(normalize_types(child))
        return retval
    if isinstance(input, dict):
        retval = {}
        for key, child in input.iteritems():
            retval[key] = normalize_types(child)
        return retval
    return input


def convert(xml):
    """Do the conversion"""
    return yaml.dump(xml, width=float('inf'), default_flow_style=False)


def plist_yaml(in_path, out_path):
    """Convert plist to yaml"""
    in_file = open(in_path, 'r')
    input = readPlist(in_file)

    normalized = normalize_types(input)
    output = convert(normalized)

    out_file = open(out_path, 'w')
    out_file.writelines(output)


def main():
    """Get the command line inputs if running this script directly"""
    if len(sys.argv) < 2:
        print("Usage: plist_yaml.py <input-file> <output-file>")
        sys.exit(1)

    in_path = sys.argv[1]

    try:
        sys.argv[2]
    except Exception as e:
        out_path = "%s.yaml" % in_path
    else:
        out_path = sys.argv[2]

    plist_yaml(in_path, out_path)


if __name__ == '__main__':
    main()
