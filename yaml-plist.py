#!/usr/bin/env python
import sys
import yaml
from os import path
from plistlib import writePlistToString

def convert(yaml):
    lines = writePlistToString(yaml).splitlines()
    lines.append('')
    return "\n".join(lines)

if len(sys.argv) < 2:
    print("Usage: yaml-plist.py <input-file> <output-file>")
    sys.exit(1)

in_path = sys.argv[1]

try:
    sys.argv[2]
except Exception as e:
    if in_path.endswith('.yaml'):
        filename, file_extension = path.splitext(in_path)
        out_path = filename
    else:
        print("Usage: yaml-plist.py <input-file> <output-file>")
        sys.exit(1)
else:
    out_path = sys.argv[2]

in_file = open(in_path, 'r')
out_file = open(out_path, 'w')

input = yaml.safe_load(in_file)
output = convert(input)

out_file.writelines(output)
