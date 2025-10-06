#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import tempfile
import os
import sys
import json
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from plistyamlplist_lib.json_plist import json_plist, clean_nones, convert


class TestJsonPlist(unittest.TestCase):
    """Test json_plist module functions independently."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.sample_json = self.test_data_dir / "sample.json"

    def test_json_plist_conversion_detailed(self):
        """Test detailed JSON to plist conversion."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:
            temp_plist_path = temp_plist.name

        try:
            # Convert json to plist
            json_plist(str(self.sample_json), temp_plist_path)

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

                # Check data content
                self.assertIn("<key>name</key>", content)
                self.assertIn("<string>Test Application</string>", content)
                self.assertIn("<key>enabled</key>", content)
                self.assertIn("<true/>", content)
                self.assertIn("<key>settings</key>", content)
                self.assertIn("<key>timeout</key>", content)
                self.assertIn("<integer>30</integer>", content)

        finally:
            # Clean up
            if os.path.exists(temp_plist_path):
                os.unlink(temp_plist_path)

    def test_json_plist_with_nonexistent_file(self):
        """Test json_plist with nonexistent input file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:
            temp_plist_path = temp_plist.name

        try:
            # Should handle gracefully
            json_plist("/nonexistent/file.json", temp_plist_path)

            # Output file should not be created or should be empty
            if os.path.exists(temp_plist_path):
                with open(temp_plist_path, "r") as f:
                    content = f.read()
                    # Should be empty or minimal
                    self.assertEqual(len(content.strip()), 0)

        finally:
            # Clean up
            if os.path.exists(temp_plist_path):
                os.unlink(temp_plist_path)

    def test_json_plist_with_invalid_output_path(self):
        """Test json_plist with invalid output path."""
        # Should handle gracefully without crashing
        json_plist(str(self.sample_json), "/invalid/path/output.plist")
        # No assertion needed - just checking it doesn't crash

    def test_clean_nones_comprehensive(self):
        """Test clean_nones function comprehensively."""
        test_data = {
            "keep_string": "value",
            "keep_number": 42,
            "keep_boolean": True,
            "remove_none": None,
            "keep_empty_string": "",
            "keep_zero": 0,
            "keep_false": False,
            "nested_dict": {
                "keep_nested": "nested_value",
                "remove_nested_none": None,
                "deeply_nested": {"keep_deep": "deep_value", "remove_deep_none": None},
            },
            "list_with_nones": [1, None, "keep", None, 3, None],
            "empty_list": [],
            "list_of_dicts": [
                {"keep": "value1", "remove": None},
                {"keep": "value2", "remove": None},
                None,  # This None should be removed
            ],
        }

        result = clean_nones(test_data)

        # Check that None values are removed
        self.assertNotIn("remove_none", result)
        self.assertNotIn("remove_nested_none", result["nested_dict"])
        self.assertNotIn("remove_deep_none", result["nested_dict"]["deeply_nested"])

        # Check that non-None values are kept
        self.assertEqual(result["keep_string"], "value")
        self.assertEqual(result["keep_number"], 42)
        self.assertEqual(result["keep_boolean"], True)
        self.assertEqual(result["keep_empty_string"], "")
        self.assertEqual(result["keep_zero"], 0)
        self.assertEqual(result["keep_false"], False)

        # Check nested structures
        self.assertEqual(result["nested_dict"]["keep_nested"], "nested_value")
        self.assertEqual(
            result["nested_dict"]["deeply_nested"]["keep_deep"], "deep_value"
        )

        # Check list handling
        self.assertEqual(result["list_with_nones"], [1, "keep", 3])
        self.assertEqual(result["empty_list"], [])

        # Check list of dicts
        self.assertEqual(len(result["list_of_dicts"]), 2)  # None item removed
        self.assertNotIn("remove", result["list_of_dicts"][0])
        self.assertNotIn("remove", result["list_of_dicts"][1])

    def test_clean_nones_with_primitives(self):
        """Test clean_nones with primitive values."""
        # Should return primitive values unchanged
        self.assertEqual(clean_nones("string"), "string")
        self.assertEqual(clean_nones(42), 42)
        self.assertEqual(clean_nones(True), True)
        self.assertEqual(clean_nones(False), False)
        self.assertIsNone(clean_nones(None))

    def test_convert_function_detailed(self):
        """Test convert function with various data types."""
        test_data = {
            "string": "test_value",
            "integer": 123,
            "float": 45.67,
            "boolean_true": True,
            "boolean_false": False,
            "list": ["item1", "item2", 3],
            "nested_dict": {"nested_key": "nested_value"},
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

    def test_convert_with_none_values(self):
        """Test convert function after clean_nones processing."""
        test_data = {"keep": "value", "remove": None}

        # Clean nones first (as done in the actual function)
        cleaned_data = clean_nones(test_data)
        result = convert(cleaned_data)

        # Should not contain the None value
        self.assertNotIn("remove", result)
        self.assertIn("<key>keep</key>", result)
        self.assertIn("<string>value</string>", result)


class TestJsonPlistIntegration(unittest.TestCase):
    """Test json_plist integration with actual JSON files."""

    def test_with_complex_json(self):
        """Test with a more complex JSON structure."""
        complex_json = {
            "app_info": {
                "name": "Complex App",
                "version": "2.1.0",
                "features": ["feature1", "feature2", "feature3"],
            },
            "settings": {
                "ui": {"theme": "dark", "language": "en"},
                "performance": {"cache_size": 100, "timeout": 5000},
            },
            "metadata": {
                "created": "2023-01-01",
                "modified": None,  # This should be removed
                "tags": ["tag1", None, "tag2"],  # None should be removed
            },
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_json, tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:

            json.dump(complex_json, temp_json)
            temp_json_path = temp_json.name
            temp_plist_path = temp_plist.name

        try:
            # Convert complex JSON to plist
            json_plist(temp_json_path, temp_plist_path)

            # Verify conversion
            self.assertTrue(os.path.exists(temp_plist_path))

            with open(temp_plist_path, "r") as f:
                content = f.read()

                # Check structure
                self.assertIn("<key>app_info</key>", content)
                self.assertIn("<string>Complex App</string>", content)
                self.assertIn("<key>features</key>", content)
                self.assertIn("<array>", content)

                # Check that None values were removed
                self.assertNotIn("modified", content)
                # Tags array should only have 2 items (None removed)
                tag_count = content.count("<string>tag")
                self.assertEqual(tag_count, 2)

        finally:
            # Clean up
            for path in [temp_json_path, temp_plist_path]:
                if os.path.exists(path):
                    os.unlink(path)


if __name__ == "__main__":
    unittest.main()
