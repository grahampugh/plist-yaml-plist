# Convert plist <=> yaml and json => plist

This utility is designed to convert Apple `plist` files to `yaml`, or `yaml` files to `plist`. I/O is from regular files.

It can also convert `json` files to `plist`.

## Prerequisites

The python `ruamel` module is required, which is not installed by default on Macs. You can install it with `pip`, which you may also need to install first.

```bash
python -m ensurepip --user
python -m pip install ruamel --user
```

If you do not pre-install `ruamel`, the script will do it for you.

## Usage

A single command can be used to convert from plist to yaml or from yaml to plist. This depends on the file suffices being predictable:

```bash
plistyamlplist -h
Usage: ./plistyamlplist.py <input-file> [<output-file>]
```

You can supply the input-file as a glob (`*.yaml` or `*.json`) to convert an entire directory or subset of `yaml` or `json` files. This currently only work for converting from yaml to plist. Note that you have to escape the glob, i.e. write as `plistyamlplist /path/to/\*.yaml`.
Otherwise, each file can be used individually:

```bash
./plist_yaml.py -h
Usage: plist-yaml.py <input-file> [<output-file>]

./yaml_plist.py -h
Usage: yaml-plist.py <input-file> [<output-file>]
```

**Notes:**

1. With `plistyamlplist.py`, if you do not specify an `output-file` value, the script determines if the `input-file` is a `plist`, `yaml` or `json` file. If a `plist` file, the `input-file` name will be appended with `.yaml` for the output file. If a `yaml` or `json` file, the output file name will be the `input-file` name with `.yaml` or `json` removed.
2. With `plist_yaml.py`, if you do not specify an `output-file` value, the `input-file` name will be appended with `.yaml` for the output file.
3. With `yaml_plist.py`, if you do not specify an `output-file` value, and the `input-file` name ends with `.yaml`, the output file name will be the `input-file` name with `.yaml` removed.
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

## YAML/JSON folder

If you have a folder named `YAML`/`_YAML`, or `JSON`/`_JSON`, in your path, and you do not supply a destination, the script will determine if a corresponding folder exists in the path without `YAML`/`JSON`. For example, consider the following file:

```bash
/Users/myuser/gitrepo/YAML/product/com.something.plist.yaml
```

If the folder `/Users/myuser/gitrepo/product` exists, the converted file will be created/overwritten at:

```bash
/Users/myuser/gitrepo/product/com.something.plist
```

If the above folder does not exist, you will be prompted to create it.

If there is no `YAML`/`JSON` folder in the path, the converted file will be placed in the same folder.

## Credits

Elements of these scripts come from:

- [chaimleib/ppl](https://github.com/chaimleib/ppl)
- [asciidoctor/sublimetext-asciidoc](https://github.com/asciidoctor/sublimetext-asciidoc)
- [clean_nones](https://stackoverflow.com/questions/4255400/exclude-empty-null-values-from-json-serialization)
