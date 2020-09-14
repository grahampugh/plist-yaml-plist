# Convert plist <=> yaml

This utility is designed to convert Apple `plist` files to `yaml`, or `yaml` files to `plist`. I/O is from regular files.

## Prerequisites

The python `yaml` module is required, which is not installed by default on Macs. You can install it with `pip`, which you may also need to install first.

```bash
sudo python -m ensurepip
pip install pyyaml
```

## Usage

A single command can be used to convert from plist to yaml or from yaml to plist. This depends on the file suffices being predictable:

```bash
plistyamlplist -h
Usage: ./plistyamlplist.py <input-file> [<output-file>]
```

You can supply the input-file as a glob (`*.yaml`) to convert an entire directory or subset of yaml files at once. This currently only work for converting from yaml to plist.

Otherwise, each file can be used individually:

```bash
./plist_yaml.py -h
Usage: plist-yaml.py <input-file> [<output-file>]

./yaml_plist.py -h
Usage: yaml-plist.py <input-file> [<output-file>]
```

**Notes:**

1. With `plistyamlplist.py`, if you do not specify an `output-file` value, the script determines if the `input-file` is
   a plist or yaml file. If a plist file, the `input-file` name will be appended with `.yaml` for the output file. If a
   yaml file, the output file name will be the `input-file` name with `.yaml` removed.
2. With `plist_yaml.py`, if you do not specify an `output-file` value, the `input-file` name will be appended with
   `.yaml` for the output file.
3. With `yaml_plist.py`, if you do not specify an `output-file` value, and the `input-file` name ends with `.yaml`,
   the output file name will be the `input-file` name with `.yaml` removed.
4. With `plist_yaml.py`, you may have to first convert a binary plist to text format using `plutil`.

## Examples

To convert a plist file to yaml:

```bash
plutil -convert xml1 ~/Library/Preferences/com.something.plist
./plistyamlplist.py ~/Library/Preferences/com.something.plist ~/Downloads/com.something.yaml
```

```bash
./plistyamlplist.py ~/Library/Preferences/com.something.plist
# this will output to `~/Library/Preferences/com.something.plist.yaml'
```

To convert a yaml file to a plist file:

```bash
./plistyamlplist.py ~/Downloads/com.something.yaml ~/Downloads/com.something.plist
```

```bash
$ ./plistyamlplist.py ~/Downloads/com.something.plist.yaml
# this will output to `~/Downloads/com.something.plist'
```

## YAML folder

If you have a folder named `YAML` in your path, and you do not supply a destination, the script
will determine if a corresponding folder exists in the path without 'YAML'. For example, consider the following file:

```bash
/Users/myuser/gitrepo/YAML/product/com.something.plist.yaml
```

If the folder `/Users/myuser/gitrepo/product` exists, the converted file will be created/overwritten at:

```bash
/Users/myuser/gitrepo/product/com.something.plist
```

If the above folder does not exist, you will be prompted to create it.

If there is no `YAML` folder in the path, the converted file will be placed in the same folder.

## Credits

Elements of these scripts come from:

- [chaimleib/ppl](https://github.com/chaimleib/ppl)
- [asciidoctor/sublimetext-asciidoc](https://github.com/asciidoctor/sublimetext-asciidoc)
