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

try:
    from ruamel.yaml import safe_load
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
    from ruamel.yaml import safe_load
    from ruamel.yaml.constructor import DuplicateKeyError

from . import handle_autopkg_recipes
from . import convert_to_yaml


def tidy_yaml(in_path, out_path=""):
    """Tidy up yaml file."""
    if not in_path.endswith(".yaml"):
        print(f"Not processing {in_path}\n")
        return

    try:
        with open(in_path, "r", encoding="utf-8") as in_file:
            input_data = safe_load(in_file)
    except IOError:
        print(f"ERROR: {in_path} not found")
        return
    except DuplicateKeyError:
        print(f"ERROR: Duplicate key found in {in_path}\n")
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
        with open(out_path, "w", encoding="utf-8") as out_file:
            out_file.writelines(output)
        print(f"Wrote to : {out_path}\n")
    except IOError:
        print(f"ERROR: could not create {out_path}")
        return


def main():
    """Get the command line inputs if running this script directly."""
    if len(sys.argv) < 2:
        print("Usage: yaml_tidy.py <input-file> <output-file>")
        sys.exit(1)

    in_path = sys.argv[1]

    try:
        sys.argv[2]
    except IndexError:
        out_path = in_path
    else:
        out_path = sys.argv[2]

    tidy_yaml(in_path, out_path)


if __name__ == "__main__":
    main()
