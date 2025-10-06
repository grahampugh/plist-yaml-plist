#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""If this script is run directly, it takes an input file and an output file
from the command line.
The input file must be in JSON format.
The output file will be in PLIST format:

json_plist.py <input-file> <output-file>

The output file can be omitted, so long as the input file ends with .yaml.
In this case, the name of the output file is
taken from the input file, with .json removed from the end.
For best results, the input file should therefore be named with .json as the suffix.
"""

import json
import sys
import os.path

try:  # python 3
    from plistlib import dumps as write_plist
except ImportError:  # python 2
    from plistlib import writePlistToString as write_plist


def clean_nones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    https://stackoverflow.com/questions/4255400/exclude-empty-null-values-from-json-serialization
    """
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {key: clean_nones(val) for key, val in value.items() if val is not None}
    else:
        return value


def convert(data):
    """Do the conversion"""
    data = clean_nones(data)
    return write_plist(data).decode()


def json_plist(in_path, out_path):
    """Convert json to plist."""
    try:
        with open(in_path, "r") as fp:
            input_data = json.load(fp)
    except IOError:
        print("ERROR: {} not found".format(in_path))
        return
    output = convert(input_data)

    try:
        with open(out_path, "w") as out_file:
            out_file.writelines(output)
        print("Wrote to : {}\n".format(out_path))
    except IOError:
        print("ERROR: could not create {} ".format(out_path))
        return


def main():
    """Get the command line inputs if running this script directly."""
    if len(sys.argv) < 2:
        print("Usage: json_plist.py <input-file> <output-file>")
        sys.exit(1)

    in_path = sys.argv[1]
    try:
        sys.argv[2]
    except Exception as e:
        print(e)  # TODO - temp to determine correct exception
        if in_path.endswith(".json"):
            filename, _ = os.path.splitext(in_path)
            out_path = filename
        else:
            print("Usage: json_plist.py <input-file> <output-file>")
            sys.exit(1)
    else:
        out_path = sys.argv[2]

    json_plist(in_path, out_path)


if __name__ == "__main__":
    main()
