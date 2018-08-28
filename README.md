Convert plist <=> yaml
======================

This utility is designed to convert Apple `plist` files to `yaml`, or `yaml` files to `plist`. I/O is from regular files.

# Prerequisites

The `pyyaml` module is required, which is not installed by default on Macs. You can install it with `pip`, which you may also need to install first.

```
$ sudo python -m ensurepip
$ pip install pyyaml
```

# Usage

```
$ ./plist-yaml.py -h
Usage: plist-yaml.py <input-file> <output-file>

$ ./yaml-plist.py -h
Usage: yaml-plist.py <input-file> <output-file>
```
Note that you may have to first convert a binary plist to text format using `plutil`.

# Examples

To convert a plist file to yaml:

```
$ plutil -convert xml1 ~/Library/Preferences/com.something.plist
$ ./plist-yaml.py ~/Library/Preferences/com.something.plist ~/Downloads/com.something.yaml
```

To convert a yaml file to a plist file:

```
$ ./yaml-plist.py ~/Downloads/com.something.yaml ~/Downloads/com.something.plist
```

# Credits

Elements of these scripts come from [chaimleib/ppl](https://github.com/chaimleib/ppl) and [asciidoctor/sublimetext-asciidoc](https://github.com/asciidoctor/sublimetext-asciidoc)
