#!/usr/bin/env python

"""
If this script is run directly, it takes an input file and an output file from
the command line. It detects if the input file is a YAML or a PLIST file,
and converts to the other format:

plistyamlplist.py <input-file> <output-file>

The output file can be omitted. In this case, the name of the output file is
taken from the input file, with .yaml added to or taken off the end.
"""

import sys
from os import path
from plist_yaml import plist_yaml
from yaml_plist import yaml_plist


def main():
    """Get the command line inputs if running this script directly"""
    if len(sys.argv) < 2:
        print("Usage: plistyamlplist.py <input-file> <output-file>")
        exit(1)

    in_path = sys.argv[1]
    try:
        sys.argv[2]
    except Exception as e:
        if in_path.endswith('.yaml') or in_path.endswith('.yml'):
            filename, file_extension = path.splitext(in_path)
            out_path = filename
        else:
            # rather than restrict by filename, check if the file is a plist by reading
            # the second line of the file for the PLIST declaration
            with open(in_path) as fp:
                for i, line in enumerate(fp):
                    if i == 1:
                        print line
                        if line.find('PLIST 1.0') == -1:
                            print("Usage: plistyamlplist.py <input-file> <output-file>")
                            exit(1)
                        else:
                            out_path = "{}.yaml".format(in_path)
                    elif i > 2:
                        break
    else:
        out_path = sys.argv[2]

    # auto-determine which direction the conversion should go
    if out_path.endswith('.yaml'):
        plist_yaml(in_path, out_path)
    else:
        yaml_plist(in_path, out_path)


if __name__ == '__main__':
    main()
