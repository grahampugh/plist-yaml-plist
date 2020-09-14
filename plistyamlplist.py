#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""If this script is run directly, it takes an input file and an output file
from the command line. It detects if the input file is a YAML or a PLIST file,
and converts to the other format:

plistyamlplist.py <input-file> <output-file>

The output file can be omitted. In this case, the name of the output file is
taken from the input file, with .yaml added to or taken off the end.
"""

import sys
import os
import glob


from plistyamlplist_lib.plist_yaml import plist_yaml
from plistyamlplist_lib.yaml_plist import yaml_plist


def usage():
    """print help."""
    print("Usage: plistyamlplist.py <input-file> <output-file>\n")
    print(
        "If <input-file> is a PLIST and <output-file> is omitted,\n"
        "<input-file> is converted to <input-file>.yaml\n"
    )
    print(
        "If <input-file> ends in .yaml or .yml and <output-file> is omitted,\n"
        "<input-file>.yaml is converted to PLIST format with name <input-file>\n"
    )


def check_if_plist(in_path):
    """rather than restrict by filename, check if the file is a plist by
    reading the second line of the file for the PLIST declaration."""
    with open(in_path) as fp:
        for i, line in enumerate(fp):
            if i == 1:
                # print line
                if line.find("PLIST 1.0") == -1:
                    is_plist = False
                else:
                    is_plist = True
            elif i > 2:
                break
    return is_plist


def check_for_yaml_folder(check_path):
    """Check folder hierarchy for a YAML folder. Output to same folder structure outwith YAML
    folder if it exists,
    e.g. /path/to/YAML/folder/subfolder/my.plist.yaml ==> /path/to/folder/subfolder/my.plist
    Note there is no reverse option at this time"""
    check_abspath = os.path.abspath(check_path)
    if "YAML" in check_abspath:
        print("YAML folder exists : {}".format(check_abspath))
        top_path, base_path = check_abspath.split("YAML/")
        out_path = os.path.dirname(os.path.join(top_path, base_path))
        if os.path.exists(out_path):
            print("Path exists : {}".format(out_path))
            return out_path
        else:
            print("Path does not exist : {}".format(out_path))
            print("Please create this folder and try again")
            exit(1)


def get_out_path(in_path):
    """determine the out_path when none given"""
    if in_path.endswith(".yaml") or in_path.endswith(".yml"):
        out_dir = check_for_yaml_folder(in_path)
        if out_dir:
            filename, _ = os.path.splitext(os.path.basename(in_path))
            out_path = os.path.join(out_dir, filename)
        else:
            filename, _ = os.path.splitext(os.path.abspath(in_path))
            out_path = filename
    else:
        if check_if_plist(in_path):
            out_path = "{}.yaml".format(in_path)
        else:
            print("\nERROR: File is neither PLIST nor YAML format.\n")
            usage()
            exit(1)
    return out_path


def main():
    """get the command line inputs if running this script directly."""
    if len(sys.argv) < 2:
        usage()
        exit(1)

    in_path = sys.argv[1]

    # auto-determine which direction the conversion should go
    if in_path.endswith(".yaml"):
        # allow for converting whole folders if a glob is provided
        _, glob_files = os.path.split(in_path)
        if "*" in glob_files:
            glob_files = glob.glob(in_path)
            for glob_file in glob_files:
                out_path = get_out_path(glob_file)
                yaml_plist(glob_file, out_path)
        else:
            try:
                sys.argv[2]
            except IndexError:
                out_path = get_out_path(in_path)
            else:
                out_path = sys.argv[2]
            yaml_plist(in_path, out_path)
    else:
        if check_if_plist(in_path):
            try:
                sys.argv[2]
            except IndexError:
                out_path = get_out_path(in_path)
            else:
                out_path = sys.argv[2]
            plist_yaml(in_path, out_path)
        else:
            print("\nERROR: Input File is neither PLIST nor YAML format.\n")
            usage()
            exit(1)


if __name__ == "__main__":
    main()
