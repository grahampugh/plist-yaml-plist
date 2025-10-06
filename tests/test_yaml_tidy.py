#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from plistyamlplist_lib.yaml_tidy import tidy_yaml
from plistyamlplist_lib import convert_to_yaml
from collections import OrderedDict


class TestYamlTidy(unittest.TestCase):
    """Test the yaml_tidy function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "test_data"

    def test_tidy_basic_yaml_file(self):
        """Test tidying a basic YAML file."""
        # Create a temporary YAML file
        yaml_content = """name: Test App
version: 1.0.0
settings:
  debug: true
  timeout: 30"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp_yaml:
            temp_yaml.write(yaml_content)
            temp_yaml_path = temp_yaml.name

        try:
            # Tidy the YAML file (in-place)
            tidy_yaml(temp_yaml_path)

            # Check that file still exists and has content
            self.assertTrue(os.path.exists(temp_yaml_path))

            with open(temp_yaml_path, "r") as f:
                result = f.read()
                self.assertGreater(len(result), 0)
                self.assertIn("name: Test App", result)

        finally:
            # Clean up
            if os.path.exists(temp_yaml_path):
                os.unlink(temp_yaml_path)

    def test_tidy_with_output_path(self):
        """Test tidying with a different output path."""
        yaml_content = """name: Test App
version: 1.0.0"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp_input, tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp_output:

            temp_input.write(yaml_content)
            temp_input_path = temp_input.name
            temp_output_path = temp_output.name

        try:
            # Tidy to different output file
            tidy_yaml(temp_input_path, temp_output_path)

            # Check that output file exists and has content
            self.assertTrue(os.path.exists(temp_output_path))

            with open(temp_output_path, "r") as f:
                result = f.read()
                self.assertIn("name: Test App", result)

        finally:
            # Clean up
            for path in [temp_input_path, temp_output_path]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_tidy_non_yaml_file(self):
        """Test that non-YAML files are skipped."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as temp_file:
            temp_file.write("not yaml content")
            temp_file_path = temp_file.name

        try:
            # Should skip non-YAML files
            tidy_yaml(temp_file_path)

            # File should remain unchanged
            with open(temp_file_path, "r") as f:
                content = f.read()
                self.assertEqual(content, "not yaml content")

        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_tidy_nonexistent_file(self):
        """Test handling of nonexistent files."""
        # Should handle gracefully without crashing
        tidy_yaml("/nonexistent/path/file.yaml")
        # No assertion needed - just checking it doesn't crash

    def test_tidy_autopkg_recipe(self):
        """Test tidying an AutoPkg recipe file."""
        recipe_content = """Description: Test AutoPkg Recipe
Identifier: com.test.recipe
Input:
  OTHER_KEY: other_value
  NAME: TestApp
Process:
- Arguments:
    arg1: value1
  Processor: TestProcessor
  Comment: Test comment"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".recipe.yaml", delete=False
        ) as temp_recipe:
            temp_recipe.write(recipe_content)
            temp_recipe_path = temp_recipe.name

        try:
            # Tidy the recipe
            tidy_yaml(temp_recipe_path)

            # Check that file was processed
            self.assertTrue(os.path.exists(temp_recipe_path))

            with open(temp_recipe_path, "r") as f:
                result = f.read()
                # Should contain the basic elements
                self.assertIn("Description:", result)
                self.assertIn("TestApp", result)

        finally:
            # Clean up
            if os.path.exists(temp_recipe_path):
                os.unlink(temp_recipe_path)


# Note: convert_to_yaml function is tested comprehensively in test_plist_yaml.py
# Note: Comprehensive tests for represent_ordereddict are now in test_shared_utils.py


if __name__ == "__main__":
    unittest.main()
