#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
If this script is run directly, it takes an input file and an output file from
the command lineThe input file must be in YAML format.
The output file will be in PLIST format:

yaml_plist.py <input-file> <output-file>

The output file can be omitted, so long as the input file ends with .yaml.
In this case, the name of the output file is
taken from the input file, with .yaml removed from the end.
For best results, the input file should therefore be named with
"""

import sys
import yaml
from os import path
from plistlib import writePlistToString


def convert(yaml):
    """Do the conversion"""
    lines = writePlistToString(yaml).splitlines()
    lines.append('')
    return "\n".join(lines)


def yaml_plist(in_path, out_path):
    """Convert yaml to plist"""
    in_file = open(in_path, 'r')
    out_file = open(out_path, 'w')

    input = yaml.safe_load(in_file)
    output = convert(input)

    out_file.writelines(output)


def main():
    """Get the command line inputs if running this script directly"""
    if len(sys.argv) < 2:
        print("Usage: yaml_plist.py <input-file> <output-file>")
        sys.exit(1)

    in_path = sys.argv[1]
    try:
        sys.argv[2]
    except Exception as e:
        if in_path.endswith('.yaml'):
            filename, file_extension = path.splitext(in_path)
            out_path = filename
        else:
            print("Usage: yaml_plist.py <input-file> <output-file>")
            sys.exit(1)
    else:
        out_path = sys.argv[2]

    yaml_plist(in_path, out_path)


if __name__ == '__main__':
    main()
