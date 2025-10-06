# Convert plist <=> yaml and json => plist

This utility is designed to convert Apple `plist` files to `yaml`, or `yaml` files to `plist`. I/O is from regular files.

It can also convert `json` files to `plist`.

## Installation
### Prerequisites

The python `ruamel.yaml` module is required, which is not installed by default on Macs. You can install it with `pip`, which you may also need to install first. A few other things need to be updated for ruamel to install:

```bash
python -m ensurepip --user
python -m pip install -U pip setuptools wheel ruamel.yaml<0.18.0 --user
```

If you do not pre-install `ruamel.yaml`, setup.py will do it for you.

#### Local git repo install
```bash
git clone git@github.com:grahampugh/plist-yaml-plist && cd plist-yaml-plist
python -m pip install .
```

#### Remote git repo install
A github ssh key is required to run `pip install -r requirements.txt`.

*requirements.txt*:
```txt
-e git+ssh://git@github.com/grahampugh/plist-yaml-plist#egg=plistyamlplist
```

## Usage

A single command can be used to convert from plist to yaml or from yaml to plist. This depends on the file suffices being predictable:

```bash
plistyamlplist -h
Usage: ./plistyamlplist.py <input-file> [<output-file>]
```

You can supply the input-file as a glob (`*.yaml` or `*.json`) to convert an entire directory or subset of `yaml` or `json` files. This currently only work for converting from yaml to plist. Note that you have to escape the glob, i.e. write as `plistyamlplist /path/to/\*.yaml`. Or, just supply a folder. The folder must be `_YAML` or `YAML` or a subfolder of one of these.
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

## Special handling of AutoPkg recipes

If you convert an AutoPkg recipe from `plist` to `yaml`, the following formatting is carried out:

- The different process dictionaries are ordered by Processor, Comment, Arguments (python3 only).
- The Input dictionary is ordered such that NAME is always at the top (python3 only).
- The items are ordered thus: Comment, Description, Identifier, ParentRecipe, MinimumVersion, Input, Process (python3 only).
- Blank lines are added for human readability. Specifically these are added above Input and Process dictionaries, and between each Processor dictionary.

You can also carry out reformatting of existing `yaml` recipes using the `yaml_tidy.py` script, or using `plistyamlplist` as in the following examples:

- Convert an AutoPkg recipe to yaml format:

  plistyamlplist /path/to/SomeRecipe.recipe

- Reformat a single `yaml`-based recipe:

  plistyamlplist /path/to/SomeRecipe.recipe.yaml --tidy

- Reformat a an entire folder structure containing `yaml`-based recipes:

  ```bash
  plistyamlplist /path/to/YAML/ --tidy
  # this will process all .recipe.yaml files in the folders within /path/to/YAML

  plistyamlplist /path/to/\_YAML/ --tidy
  # this will process all .recipe.yaml files in the folders within /path/to/_YAML

  plistyamlplist /path/to/YAML/subfolder/ --tidy
  # this will process all .recipe.yaml files in the folders within /path/to/_YAML/subfolder
  ```

## Testing

This project includes unit tests to verify the core conversion functionality. To run these tests:

```bash
python -m unittest discover tests -v
```

## Credits

Elements of these scripts come from:

- [chaimleib/ppl](https://github.com/chaimleib/ppl)
- [asciidoctor/sublimetext-asciidoc](https://github.com/asciidoctor/sublimetext-asciidoc)
- [clean_nones](https://stackoverflow.com/questions/4255400/exclude-empty-null-values-from-json-serialization)
