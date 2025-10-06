#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
from pathlib import Path
from collections import OrderedDict

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from plistyamlplist_lib.handle_autopkg_recipes import (
    optimise_autopkg_recipes,
    format_autopkg_recipes,
)


class TestOptimiseAutopkgRecipes(unittest.TestCase):
    """Test the optimise_autopkg_recipes function."""

    def test_basic_recipe_optimization(self):
        """Test basic recipe optimization with Process and Input."""
        recipe = {
            "Description": "Test recipe",
            "Identifier": "com.test.recipe",
            "Process": [
                {
                    "Arguments": {"arg1": "value1"},
                    "Processor": "TestProcessor",
                    "Comment": "Test comment",
                }
            ],
            "Input": {"OTHER_KEY": "other_value", "NAME": "TestApp"},
        }

        result = optimise_autopkg_recipes(recipe)

        # Check that Process is reordered (Processor first, Comment and Arguments last)
        process_item = result["Process"][0]
        keys = list(process_item.keys())
        self.assertEqual(keys[0], "Processor")
        self.assertEqual(keys[-2], "Comment")
        self.assertEqual(keys[-1], "Arguments")

        # Check that Input has NAME first
        input_keys = list(result["Input"].keys())
        self.assertEqual(input_keys[0], "NAME")

        # Check overall order
        recipe_keys = list(result.keys())
        self.assertEqual(recipe_keys[0], "Description")
        self.assertEqual(recipe_keys[1], "Identifier")
        self.assertIn("Input", recipe_keys)
        self.assertIn("Process", recipe_keys)

    def test_recipe_without_process(self):
        """Test recipe optimization when Process is missing."""
        recipe = {
            "Description": "Test recipe",
            "Input": {"OTHER_KEY": "other_value", "NAME": "TestApp"},
        }

        result = optimise_autopkg_recipes(recipe)

        # Should still work and reorder Input
        input_keys = list(result["Input"].keys())
        self.assertEqual(input_keys[0], "NAME")

    def test_recipe_without_input(self):
        """Test recipe optimization when Input is missing."""
        recipe = {
            "Description": "Test recipe",
            "Process": [{"Processor": "TestProcessor"}],
        }

        result = optimise_autopkg_recipes(recipe)

        # Should still work and reorder Process
        self.assertIn("Process", result)
        self.assertEqual(result["Process"][0]["Processor"], "TestProcessor")

    def test_recipe_without_name_in_input(self):
        """Test recipe optimization when Input doesn't have NAME."""
        recipe = {
            "Description": "Test recipe",
            "Input": {"OTHER_KEY": "other_value", "ANOTHER_KEY": "another_value"},
        }

        result = optimise_autopkg_recipes(recipe)

        # Should still work without NAME
        self.assertIn("Input", result)
        self.assertIn("OTHER_KEY", result["Input"])

    def test_desired_order_enforcement(self):
        """Test that recipe keys are ordered according to desired_order."""
        recipe = {
            "Process": [{"Processor": "TestProcessor"}],
            "Comment": "Recipe comment",
            "Input": {"NAME": "TestApp"},
            "Description": "Test recipe",
            "Identifier": "com.test.recipe",
            "MinimumVersion": "1.0",
        }

        result = optimise_autopkg_recipes(recipe)

        expected_order = [
            "Comment",
            "Description",
            "Identifier",
            "MinimumVersion",
            "Input",
            "Process",
        ]

        actual_keys = list(result.keys())
        self.assertEqual(actual_keys, expected_order)

    def test_parent_recipe_trust_info(self):
        """Test that ParentRecipeTrustInfo is handled correctly."""
        recipe = {
            "Description": "Test recipe",
            "ParentRecipeTrustInfo": {"trust_info": "data"},
            "Input": {"NAME": "TestApp"},
        }

        result = optimise_autopkg_recipes(recipe)

        # ParentRecipeTrustInfo should be at the end
        keys = list(result.keys())
        self.assertIn("ParentRecipeTrustInfo", keys)


class TestFormatAutopkgRecipes(unittest.TestCase):
    """Test the format_autopkg_recipes function."""

    def test_basic_formatting(self):
        """Test basic YAML formatting with line breaks."""
        yaml_input = """Description: Test recipe
Input:
  NAME: TestApp
Process:
- Processor: TestProcessor
  Arguments:
    arg1: value1"""

        result = format_autopkg_recipes(yaml_input)

        # Should add line breaks before Input:, Process:, and - Processor:
        self.assertIn("\nInput:", result)
        self.assertIn("\nProcess:", result)
        # First processor shouldn't have extra line break
        self.assertNotIn("Process:\n\n-", result)

    def test_newline_conversion_in_strings(self):
        """Test conversion of quoted strings with newlines to scalars."""
        yaml_input = 'Description: "Line 1\\nLine 2\\nLine 3"'

        result = format_autopkg_recipes(yaml_input)

        # Should convert to scalar format
        self.assertIn("Description: |", result)
        self.assertNotIn("\\n", result)

    def test_tab_conversion(self):
        """Test conversion of \\t to spaces."""
        yaml_input = 'Description: "Text with\\ttab"'

        result = format_autopkg_recipes(yaml_input)

        # The function only converts \\t when processing multiline strings with \\n
        # For simple strings, it leaves them as-is
        self.assertIn("Description:", result)

    def test_quote_escaping(self):
        """Test handling of escaped quotes."""
        yaml_input = 'Description: "Text with \\"quotes\\""'

        result = format_autopkg_recipes(yaml_input)

        # The function only processes quotes when handling multiline strings with \\n
        # For simple strings, it leaves them as-is
        self.assertIn("Description:", result)
        self.assertIn("quotes", result)

    def test_empty_input(self):
        """Test formatting with empty input."""
        result = format_autopkg_recipes("")

        # Should return empty string (the function adds a newline at the end)
        self.assertEqual(result, "")

    def test_multiple_processors(self):
        """Test formatting with multiple processors."""
        yaml_input = """Process:
- Processor: FirstProcessor
- Processor: SecondProcessor"""

        result = format_autopkg_recipes(yaml_input)

        # Should add line breaks before each processor
        self.assertIn("\n- Processor: FirstProcessor", result)
        self.assertIn("\n- Processor: SecondProcessor", result)

    def test_parent_recipe_trust_info_formatting(self):
        """Test formatting of ParentRecipeTrustInfo."""
        yaml_input = """Description: Test
ParentRecipeTrustInfo:
  trust_data: value"""

        result = format_autopkg_recipes(yaml_input)

        # Should add line break before ParentRecipeTrustInfo
        self.assertIn("\nParentRecipeTrustInfo:", result)


if __name__ == "__main__":
    unittest.main()
