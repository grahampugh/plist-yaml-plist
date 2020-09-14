#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""If this script is run directly, it takes an input file and an output file
from the command line. The input file must be in PLIST format. The output file
will be in YAML format:

plist_yaml.py <input-file> <output-file>

The output file can be omitted. In this case, the name of the output file is
taken from the input file, with .yaml added to the end.
"""

import sys
from collections import OrderedDict

try:
    from plistlib import Data  # Python 3
    from plistlib import load as load_plist
except ImportError:
    from plistlib import Data  # Python 2
    from plistlib import readPlist as load_plist

import yaml


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u"tag:yaml.org,2002:map", value)


def normalize_types(input_data):
    """This allows YAML and JSON to store Data fields as strings.

    However, this operation is irreversible. Only use if read-only
    access to the plist is required.
    """
    if isinstance(input_data, Data):
        return input_data.data
    if isinstance(input_data, list):
        retval = []
        for child in input_data:
            retval.append(normalize_types(child))
        return retval
    if isinstance(input_data, dict):
        retval = {}
        for key in input_data:
            retval[key] = normalize_types(input_data[key])
        return retval
    return input_data


def sort_autopkg_processes(recipe):
    """If input is an AutoPkg recipe, adjust the processor dictionaries such
    that the Arguments key is ordered last.

    This usually puts the Processor key first, which makes the process
    list more human-readable.
    """
    if "Process" in recipe:
        process = recipe["Process"]
        new_process = []
        for processor in process:
            if "Arguments" in processor:
                processor = OrderedDict(processor)
                processor.move_to_end("Arguments")
            new_process.append(processor)
        recipe["Process"] = new_process
    return recipe


def convert(xml):
    """Do the conversion."""
    yaml.add_representer(OrderedDict, represent_ordereddict)
    return yaml.dump(xml, width=float("inf"), default_flow_style=False)


def plist_yaml(in_path, out_path):
    """Convert plist to yaml."""
    with open(in_path, "rb") as in_file:
        input_data = load_plist(in_file)

    normalized = normalize_types(input_data)
    if sys.version_info.major == 3 and in_path.endswith((".recipe", ".recipe.plist")):
        normalized = sort_autopkg_processes(normalized)
    output = convert(normalized)

    out_file = open(out_path, "w")
    out_file.writelines(output)
    print("Wrote to : {}\n".format(out_path))


def main():
    """Get the command line inputs if running this script directly."""
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


if __name__ == "__main__":
    main()
