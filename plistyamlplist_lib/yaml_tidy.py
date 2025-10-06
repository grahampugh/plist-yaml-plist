#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""If this script is run directly, it takes an input file
from the command line. The input file must be in YAML format. The output file
will be in YAML format:

yaml_tidy.py <input-file>

The output file can be omitted. In this case, the input file will be overwritten.
"""

import subprocess
import sys

from collections import OrderedDict

try:
    from ruamel.yaml import dump, safe_load, add_representer
    from ruamel.yaml.nodes import MappingNode
    from ruamel.yaml.constructor import DuplicateKeyError
except ImportError:
    subprocess.check_call([sys.executable, "-m", "ensurepip", "--user"])
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-U",
            "pip",
            "setuptools",
            "wheel",
            "ruamel.yaml<0.18.0",
            "--user",
        ]
    )
    from ruamel.yaml import dump, safe_load, add_representer
    from ruamel.yaml.nodes import MappingNode
    from ruamel.yaml.constructor import DuplicateKeyError

from . import handle_autopkg_recipes
from . import represent_ordereddict
from . import convert_to_yaml


def tidy_yaml(in_path, out_path=""):
    """Tidy up yaml file."""
    if not in_path.endswith(".yaml"):
        print("Not processing {}\n".format(in_path))
        return

    try:
        with open(in_path, "r") as in_file:
            input_data = safe_load(in_file)
    except IOError:
        print("ERROR: {} not found".format(in_path))
        return
    except DuplicateKeyError:
        print("ERROR: Duplicate key found in {}\n".format(in_path))
        return

    # handle conversion of AutoPkg recipes
    if sys.version_info.major == 3 and in_path.endswith(".recipe.yaml"):
        input_data = handle_autopkg_recipes.optimise_autopkg_recipes(input_data)
        output = convert_to_yaml(input_data)
        output = handle_autopkg_recipes.format_autopkg_recipes(output)
    else:
        output = convert_to_yaml(input_data)

    if not out_path:
        out_path = in_path
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
        print("Usage: yaml_tidy.py <input-file> <output-file>")
        sys.exit(1)

    in_path = sys.argv[1]

    try:
        sys.argv[2]
    except Exception:
        out_path = in_path
    else:
        out_path = sys.argv[2]

    tidy_yaml(in_path, out_path)


if __name__ == "__main__":
    main()
