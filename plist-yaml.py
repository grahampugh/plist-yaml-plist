#!/usr/bin/env python

import sys
import yaml
from os import path
from plistlib import readPlist, Data

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
    return yaml.dump(xml, width=float('inf'), default_flow_style=False)

if len(sys.argv) < 3:
    print("Usage: plist-yaml.py <input-file> <output-file>")
    sys.exit(1)

in_path = sys.argv[1]
out_path = sys.argv[2]

in_file = open(in_path, 'r')
out_file = open(out_path, 'w')

input = readPlist(in_file)
normalized = normalize_types(input)
output = convert(normalized)

out_file.writelines(output)
