#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
from pathlib import Path
from collections import OrderedDict

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from plistyamlplist_lib import represent_ordereddict, convert_to_yaml

# Import YAML components for testing
try:
    from ruamel.yaml import YAML
    from ruamel.yaml.nodes import MappingNode, ScalarNode
    from ruamel.yaml.representer import RoundTripRepresenter
except ImportError:
    # Skip tests if ruamel.yaml is not available
    YAML = None


class MockDumper:
    """Mock dumper class for testing represent_ordereddict."""

    def __init__(self):
        self.represented_data = {}

    def represent_data(self, data):
        """Mock represent_data method that creates ScalarNode for simple data."""
        if isinstance(data, str):
            return ScalarNode(tag="tag:yaml.org,2002:str", value=data)
        elif isinstance(data, int):
            return ScalarNode(tag="tag:yaml.org,2002:int", value=str(data))
        elif isinstance(data, bool):
            # Use Python's string representation for consistency with actual behavior
            return ScalarNode(tag="tag:yaml.org,2002:bool", value=str(data))
        elif data is None:
            return ScalarNode(tag="tag:yaml.org,2002:null", value="null")
        else:
            # For complex data, just return a string representation
            return ScalarNode(tag="tag:yaml.org,2002:str", value=str(data))


@unittest.skipIf(YAML is None, "ruamel.yaml not available")
class TestRepresentOrderedDict(unittest.TestCase):
    """Test the shared represent_ordereddict utility function."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_dumper = MockDumper()

    def test_represent_ordereddict_basic(self):
        """Test basic functionality of represent_ordereddict."""
        test_data = OrderedDict(
            [("first", "value1"), ("second", "value2"), ("third", "value3")]
        )

        result = represent_ordereddict(self.mock_dumper, test_data)

        # Should return a MappingNode
        self.assertIsInstance(result, MappingNode)

        # Should have the correct tag
        self.assertEqual(result.tag, "tag:yaml.org,2002:map")

        # Should have the correct number of key-value pairs
        self.assertEqual(len(result.value), 3)

        # Check that all pairs are tuples of nodes
        for pair in result.value:
            self.assertIsInstance(pair, tuple)
            self.assertEqual(len(pair), 2)
            self.assertIsInstance(pair[0], ScalarNode)  # key node
            self.assertIsInstance(pair[1], ScalarNode)  # value node

    def test_represent_ordereddict_centralized(self):
        """Test that the centralized represent_ordereddict function works correctly."""
        test_data = OrderedDict(
            [("first", "value1"), ("second", "value2"), ("third", "value3")]
        )

        result = represent_ordereddict(self.mock_dumper, test_data)

        # Should return a MappingNode
        self.assertIsInstance(result, MappingNode)

        # Should have the correct tag
        self.assertEqual(result.tag, "tag:yaml.org,2002:map")

        # Should have the correct number of key-value pairs
        self.assertEqual(len(result.value), 3)

    def test_represent_ordereddict_preserves_order(self):
        """Test that represent_ordereddict preserves the order of keys."""
        test_data = OrderedDict(
            [("zebra", "last"), ("alpha", "first"), ("beta", "second")]
        )

        result = represent_ordereddict(self.mock_dumper, test_data)

        # Extract the key values from the result
        key_values = [pair[0].value for pair in result.value]

        # Should maintain the original order
        expected_order = ["zebra", "alpha", "beta"]
        self.assertEqual(key_values, expected_order)

    def test_represent_ordereddict_with_different_types(self):
        """Test represent_ordereddict with different data types."""
        test_data = OrderedDict(
            [
                ("string_key", "string_value"),
                ("int_key", 42),
                ("bool_key", True),
                ("none_key", None),
            ]
        )

        result = represent_ordereddict(self.mock_dumper, test_data)

        # Should handle all data types
        self.assertEqual(len(result.value), 4)

        # Check that each value was properly represented
        key_value_pairs = [(pair[0].value, pair[1].value) for pair in result.value]

        expected_pairs = [
            ("string_key", "string_value"),
            ("int_key", "42"),
            ("bool_key", "True"),  # Python's str(True) returns "True", not "true"
            ("none_key", "null"),
        ]

        self.assertEqual(key_value_pairs, expected_pairs)

    def test_represent_ordereddict_empty(self):
        """Test represent_ordereddict with empty OrderedDict."""
        test_data = OrderedDict()

        result = represent_ordereddict(self.mock_dumper, test_data)

        # Should return a MappingNode with empty value list
        self.assertIsInstance(result, MappingNode)
        self.assertEqual(result.tag, "tag:yaml.org,2002:map")
        self.assertEqual(len(result.value), 0)
        self.assertEqual(result.value, [])

    def test_represent_ordereddict_nested_structure(self):
        """Test represent_ordereddict with nested data structures."""
        nested_dict = {"nested_key": "nested_value"}
        nested_list = ["item1", "item2"]

        test_data = OrderedDict(
            [("simple", "value"), ("dict", nested_dict), ("list", nested_list)]
        )

        result = represent_ordereddict(self.mock_dumper, test_data)

        # Should handle nested structures (they get converted to strings by mock dumper)
        self.assertEqual(len(result.value), 3)

        # Check the keys
        keys = [pair[0].value for pair in result.value]
        self.assertEqual(keys, ["simple", "dict", "list"])

    def test_represent_ordereddict_single_item(self):
        """Test represent_ordereddict with single item."""
        test_data = OrderedDict([("only_key", "only_value")])

        result = represent_ordereddict(self.mock_dumper, test_data)

        # Should work with single item
        self.assertEqual(len(result.value), 1)
        key_node, value_node = result.value[0]
        self.assertEqual(key_node.value, "only_key")
        self.assertEqual(value_node.value, "only_value")

    def test_represent_ordereddict_consistency(self):
        """Test that represent_ordereddict produces consistent results."""
        test_data = OrderedDict([("key1", "value1"), ("key2", 42), ("key3", True)])

        result1 = represent_ordereddict(self.mock_dumper, test_data)
        result2 = represent_ordereddict(self.mock_dumper, test_data)

        # Multiple calls should produce identical results
        self.assertEqual(result1.tag, result2.tag)
        self.assertEqual(len(result1.value), len(result2.value))

        # Compare each key-value pair
        for pair1, pair2 in zip(result1.value, result2.value):
            self.assertEqual(pair1[0].value, pair2[0].value)  # keys
            self.assertEqual(pair1[1].value, pair2[1].value)  # values

    def test_represent_ordereddict_with_special_characters(self):
        """Test represent_ordereddict with special characters in keys and values."""
        test_data = OrderedDict(
            [
                ("key with spaces", "value with spaces"),
                ("key-with-dashes", "value-with-dashes"),
                ("key_with_underscores", "value_with_underscores"),
                ("key.with.dots", "value.with.dots"),
                ("key/with/slashes", "value/with/slashes"),
            ]
        )

        result = represent_ordereddict(self.mock_dumper, test_data)

        # Should handle special characters
        self.assertEqual(len(result.value), 5)

        # Verify all keys and values are preserved
        for i, (expected_key, expected_value) in enumerate(test_data.items()):
            key_node, value_node = result.value[i]
            self.assertEqual(key_node.value, expected_key)
            self.assertEqual(value_node.value, expected_value)


@unittest.skipIf(YAML is None, "ruamel.yaml not available")
class TestSharedUtilsIntegration(unittest.TestCase):
    """Integration tests for shared utility functions with actual YAML processing."""

    def test_integration_with_yaml_conversion(self):
        """Test represent_ordereddict integration with convert_to_yaml function."""

        test_data = OrderedDict(
            [("first", "alpha"), ("second", "beta"), ("third", "gamma")]
        )

        # This should use represent_ordereddict internally
        result = convert_to_yaml(test_data)

        # Should produce valid YAML
        self.assertIsInstance(result, str)
        self.assertIn("first: alpha", result)
        self.assertIn("second: beta", result)
        self.assertIn("third: gamma", result)

        # Order should be preserved in the output
        lines = result.strip().split("\n")
        self.assertTrue(any("first: alpha" in line for line in lines))
        self.assertTrue(any("second: beta" in line for line in lines))
        self.assertTrue(any("third: gamma" in line for line in lines))

    def test_integration_with_yaml_tidy_conversion(self):
        """Test represent_ordereddict integration with centralized convert_to_yaml function."""

        test_data = OrderedDict(
            [("name", "Test App"), ("version", "1.0.0"), ("enabled", True)]
        )

        # This should use represent_ordereddict internally
        result = convert_to_yaml(test_data)

        # Should produce valid YAML
        self.assertIsInstance(result, str)
        self.assertIn("name: Test App", result)
        self.assertIn("version: 1.0.0", result)
        self.assertIn("enabled: true", result)


if __name__ == "__main__":
    unittest.main()
