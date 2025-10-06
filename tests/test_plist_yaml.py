#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from plistyamlplist_lib.plist_yaml import plist_yaml, normalize_types
from plistyamlplist_lib import convert_to_yaml
from plistyamlplist_lib.yaml_plist import yaml_plist
from plistyamlplist_lib.json_plist import json_plist, clean_nones


class TestPlistYaml(unittest.TestCase):
    """Test plist to YAML conversion functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.sample_plist = self.test_data_dir / "sample.plist"
        self.sample_yaml = self.test_data_dir / "sample.yaml"

    def test_plist_to_yaml_conversion(self):
        """Test basic plist to YAML conversion."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp_yaml:
            temp_yaml_path = temp_yaml.name

        try:
            # Convert plist to yaml
            plist_yaml(str(self.sample_plist), temp_yaml_path)

            # Check that output file was created
            self.assertTrue(os.path.exists(temp_yaml_path))

            # Check that output file has content
            with open(temp_yaml_path, "r") as f:
                content = f.read()
                self.assertGreater(len(content), 0)

            # Check for expected content
            self.assertIn("name: Test Application", content)
            self.assertIn("version: 1.0.0", content)
            self.assertIn("enabled: true", content)

        finally:
            # Clean up
            if os.path.exists(temp_yaml_path):
                os.unlink(temp_yaml_path)

    def test_normalize_types_basic(self):
        """Test the normalize_types function with basic data types."""
        test_data = {
            "string": "test",
            "number": 42,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
        }

        result = normalize_types(test_data)

        # Should return the same data for basic types
        self.assertEqual(result["string"], "test")
        self.assertEqual(result["number"], 42)
        self.assertEqual(result["boolean"], True)
        self.assertEqual(result["list"], [1, 2, 3])
        self.assertEqual(result["dict"]["nested"], "value")

    def test_convert_function(self):
        """Test the convert function produces YAML output."""
        test_data = {"name": "test", "value": 123}

        result = convert_to_yaml(test_data)

        # Should be a string containing YAML
        self.assertIsInstance(result, str)
        self.assertIn("name: test", result)
        self.assertIn("value: 123", result)


class TestYamlPlist(unittest.TestCase):
    """Test YAML to plist conversion functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.sample_yaml = self.test_data_dir / "sample.yaml"

    def test_yaml_to_plist_conversion(self):
        """Test basic YAML to plist conversion."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:
            temp_plist_path = temp_plist.name

        try:
            # Convert yaml to plist
            yaml_plist(str(self.sample_yaml), temp_plist_path)

            # Check that output file was created
            self.assertTrue(os.path.exists(temp_plist_path))

            # Check that output file has content
            with open(temp_plist_path, "r") as f:
                content = f.read()
                self.assertGreater(len(content), 0)

            # Check for expected plist structure
            self.assertIn('<?xml version="1.0"', content)
            self.assertIn("<!DOCTYPE plist", content)
            self.assertIn('<plist version="1.0">', content)
            self.assertIn("<key>name</key>", content)
            self.assertIn("<string>Test Application</string>", content)

        finally:
            # Clean up
            if os.path.exists(temp_plist_path):
                os.unlink(temp_plist_path)


class TestJsonPlist(unittest.TestCase):
    """Test JSON to plist conversion functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.sample_json = self.test_data_dir / "sample.json"

    def test_json_to_plist_conversion(self):
        """Test basic JSON to plist conversion."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:
            temp_plist_path = temp_plist.name

        try:
            # Convert json to plist
            json_plist(str(self.sample_json), temp_plist_path)

            # Check that output file was created
            self.assertTrue(os.path.exists(temp_plist_path))

            # Check that output file has content
            with open(temp_plist_path, "r") as f:
                content = f.read()
                self.assertGreater(len(content), 0)

            # Check for expected plist structure
            self.assertIn('<?xml version="1.0"', content)
            self.assertIn("<key>name</key>", content)
            self.assertIn("<string>Test Application</string>", content)

        finally:
            # Clean up
            if os.path.exists(temp_plist_path):
                os.unlink(temp_plist_path)

    def test_clean_nones_function(self):
        """Test the clean_nones function removes None values."""
        test_data = {
            "keep": "value",
            "remove": None,
            "nested": {"keep": "nested_value", "remove": None},
            "list": [1, None, 3, None],
        }

        result = clean_nones(test_data)

        # None values should be removed
        self.assertNotIn("remove", result)
        self.assertNotIn("remove", result["nested"])
        self.assertEqual(result["list"], [1, 3])

        # Non-None values should be kept
        self.assertEqual(result["keep"], "value")
        self.assertEqual(result["nested"]["keep"], "nested_value")


class TestRoundTripConversions(unittest.TestCase):
    """Test round-trip conversions to ensure data integrity."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.sample_plist = self.test_data_dir / "sample.plist"

    def test_plist_yaml_plist_roundtrip(self):
        """Test plist -> yaml -> plist conversion preserves data."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp_yaml, tempfile.NamedTemporaryFile(
            mode="w", suffix=".plist", delete=False
        ) as temp_plist:

            temp_yaml_path = temp_yaml.name
            temp_plist_path = temp_plist.name

        try:
            # Convert plist -> yaml -> plist
            plist_yaml(str(self.sample_plist), temp_yaml_path)
            yaml_plist(temp_yaml_path, temp_plist_path)

            # Both files should exist and have content
            self.assertTrue(os.path.exists(temp_yaml_path))
            self.assertTrue(os.path.exists(temp_plist_path))

            with open(temp_plist_path, "r") as f:
                final_content = f.read()

            # Should contain the key elements from original
            self.assertIn("<key>name</key>", final_content)
            self.assertIn("<string>Test Application</string>", final_content)
            self.assertIn("<key>enabled</key>", final_content)
            self.assertIn("<true/>", final_content)

        finally:
            # Clean up
            for path in [temp_yaml_path, temp_plist_path]:
                if os.path.exists(path):
                    os.unlink(path)


if __name__ == "__main__":
    unittest.main()
