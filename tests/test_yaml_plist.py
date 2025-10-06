#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from plistyamlplist_lib.yaml_plist import yaml_plist, convert


class TestYamlPlist(unittest.TestCase):
    """Test yaml_plist module functions independently."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.sample_yaml = self.test_data_dir / "sample.yaml"

    def test_yaml_plist_conversion_detailed(self):
        """Test detailed YAML to plist conversion."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:
            temp_plist_path = temp_plist.name

        try:
            # Convert yaml to plist
            yaml_plist(str(self.sample_yaml), temp_plist_path)

            # Check that output file was created
            self.assertTrue(os.path.exists(temp_plist_path))

            # Check detailed plist structure
            with open(temp_plist_path, "r") as f:
                content = f.read()

                # Check XML structure
                self.assertIn('<?xml version="1.0"', content)
                self.assertIn("<!DOCTYPE plist", content)
                self.assertIn('<plist version="1.0">', content)
                self.assertIn("</plist>", content)

                # Check data content from sample.yaml
                self.assertIn("<key>name</key>", content)
                self.assertIn("<string>Test Application</string>", content)
                self.assertIn("<key>version</key>", content)
                self.assertIn("<string>1.0.0</string>", content)
                self.assertIn("<key>enabled</key>", content)
                self.assertIn("<true/>", content)

                # Check nested structure
                self.assertIn("<key>settings</key>", content)
                self.assertIn("<dict>", content)
                self.assertIn("<key>debug</key>", content)
                self.assertIn("<false/>", content)
                self.assertIn("<key>timeout</key>", content)
                self.assertIn("<integer>30</integer>", content)

                # Check array structure
                self.assertIn("<key>urls</key>", content)
                self.assertIn("<array>", content)
                self.assertIn("<string>https://example.com</string>", content)
                self.assertIn("<string>https://test.com</string>", content)

        finally:
            # Clean up
            if os.path.exists(temp_plist_path):
                os.unlink(temp_plist_path)

    def test_yaml_plist_with_nonexistent_file(self):
        """Test yaml_plist with nonexistent input file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:
            temp_plist_path = temp_plist.name

        try:
            # Should handle gracefully and return early
            yaml_plist("/nonexistent/file.yaml", temp_plist_path)

            # Output file should not contain valid plist data
            if os.path.exists(temp_plist_path):
                with open(temp_plist_path, "r") as f:
                    content = f.read()
                    # Should be empty or minimal
                    self.assertEqual(len(content.strip()), 0)

        finally:
            # Clean up
            if os.path.exists(temp_plist_path):
                os.unlink(temp_plist_path)

    def test_yaml_plist_with_invalid_output_path(self):
        """Test yaml_plist with invalid output path."""
        # Should handle gracefully without crashing
        yaml_plist(str(self.sample_yaml), "/invalid/path/output.plist")
        # No assertion needed - just checking it doesn't crash

    def test_convert_function_detailed(self):
        """Test convert function with various YAML data types."""
        test_data = {
            "string": "test_value",
            "integer": 123,
            "float": 45.67,
            "boolean_true": True,
            "boolean_false": False,
            "list": ["item1", "item2", 3],
            "nested_dict": {"nested_key": "nested_value"},
            # Note: plist format doesn't support None/null values
        }

        result = convert(test_data)

        # Should return a plist XML string
        self.assertIsInstance(result, str)
        self.assertIn('<?xml version="1.0"', result)
        self.assertIn("<plist", result)
        self.assertIn("</plist>", result)

        # Check that data is properly encoded
        self.assertIn("<key>string</key>", result)
        self.assertIn("<string>test_value</string>", result)
        self.assertIn("<key>integer</key>", result)
        self.assertIn("<integer>123</integer>", result)
        self.assertIn("<key>boolean_true</key>", result)
        self.assertIn("<true/>", result)
        self.assertIn("<key>boolean_false</key>", result)
        self.assertIn("<false/>", result)

        # Check array
        self.assertIn("<key>list</key>", result)
        self.assertIn("<array>", result)

        # Check nested dict
        self.assertIn("<key>nested_dict</key>", result)
        self.assertIn("<key>nested_key</key>", result)

    def test_yaml_plist_with_custom_yaml(self):
        """Test yaml_plist with custom YAML content."""
        yaml_content = """application:
  name: Custom App
  version: 3.0.0
  settings:
    theme: light
    notifications: true
    max_connections: 50
  features:
    - authentication
    - logging
    - monitoring
metadata:
  created_by: test
  environment: development"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp_yaml, tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:

            temp_yaml.write(yaml_content)
            temp_yaml_path = temp_yaml.name
            temp_plist_path = temp_plist.name

        try:
            # Convert custom YAML to plist
            yaml_plist(temp_yaml_path, temp_plist_path)

            # Verify conversion
            self.assertTrue(os.path.exists(temp_plist_path))

            with open(temp_plist_path, "r") as f:
                content = f.read()

                # Check structure
                self.assertIn("<key>application</key>", content)
                self.assertIn("<string>Custom App</string>", content)
                self.assertIn("<key>settings</key>", content)
                self.assertIn("<integer>50</integer>", content)

                # Check array
                self.assertIn("<key>features</key>", content)
                self.assertIn("<array>", content)
                self.assertIn("<string>authentication</string>", content)
                self.assertIn("<string>logging</string>", content)
                self.assertIn("<string>monitoring</string>", content)

                # Check metadata
                self.assertIn("<key>metadata</key>", content)
                self.assertIn("<string>development</string>", content)

        finally:
            # Clean up
            for path in [temp_yaml_path, temp_plist_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_yaml_plist_with_malformed_yaml(self):
        """Test yaml_plist with malformed YAML."""
        malformed_yaml = """name: Test App
version: 1.0.0
settings:
  debug: true
    invalid_indentation: bad
  timeout: 30"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp_yaml, tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:

            temp_yaml.write(malformed_yaml)
            temp_yaml_path = temp_yaml.name
            temp_plist_path = temp_plist.name

        try:
            # Should raise an exception for malformed YAML
            with self.assertRaises(Exception):
                yaml_plist(temp_yaml_path, temp_plist_path)

        finally:
            # Clean up
            for path in [temp_yaml_path, temp_plist_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_convert_with_empty_data(self):
        """Test convert function with empty data."""
        result = convert({})

        # Should return valid empty plist
        self.assertIsInstance(result, str)
        self.assertIn('<?xml version="1.0"', result)
        self.assertIn("<plist", result)
        self.assertIn("<dict/>", result)
        self.assertIn("</plist>", result)

    def test_convert_with_nested_structures(self):
        """Test convert function with deeply nested structures."""
        nested_data = {
            "level1": {
                "level2": {
                    "level3": {"level4": {"deep_value": "found", "deep_number": 42}}
                }
            }
        }

        result = convert(nested_data)

        # Should handle deep nesting
        self.assertIn("<key>level1</key>", result)
        self.assertIn("<key>level2</key>", result)
        self.assertIn("<key>level3</key>", result)
        self.assertIn("<key>level4</key>", result)
        self.assertIn("<key>deep_value</key>", result)
        self.assertIn("<string>found</string>", result)
        self.assertIn("<integer>42</integer>", result)


if __name__ == "__main__":
    unittest.main()
