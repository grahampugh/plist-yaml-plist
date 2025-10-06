#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shared utilities for plist-yaml-plist conversion library.
"""

try:
    from ruamel.yaml.nodes import MappingNode
    from ruamel.yaml import dump, add_representer
    from collections import OrderedDict
except ImportError:
    # Handle case where ruamel.yaml is not available
    MappingNode = None
    dump = None
    add_representer = None
    OrderedDict = None


def represent_ordereddict(dumper, data):
    """
    Custom representer for OrderedDict objects in YAML output.

    This function ensures that OrderedDict objects maintain their key order
    when converted to YAML format, which is crucial for preserving the
    structure of plist files.

    Args:
        dumper: The YAML dumper object
        data: OrderedDict to be represented

    Returns:
        MappingNode: A YAML mapping node preserving the original order
    """
    if MappingNode is None:
        raise ImportError("ruamel.yaml is required for YAML processing")

    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return MappingNode("tag:yaml.org,2002:map", value)


def convert_to_yaml(data):
    """
    Convert data to YAML format with OrderedDict support.

    This function converts Python data structures to YAML format while
    preserving the order of OrderedDict objects. It's used by both
    plist_yaml and yaml_tidy modules for consistent YAML output.

    Args:
        data: Python data structure to convert to YAML

    Returns:
        str: YAML representation of the data

    Raises:
        ImportError: If ruamel.yaml is not available
    """
    if dump is None or add_representer is None or OrderedDict is None:
        raise ImportError("ruamel.yaml is required for YAML processing")

    add_representer(OrderedDict, represent_ordereddict)
    return dump(data, width=float("inf"), default_flow_style=False)
