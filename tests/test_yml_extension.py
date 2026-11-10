#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Regression test: files ending in `.yml` must be treated as YAML input,
just like `.yaml` files (the usage text promises both)."""

import gc
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plistyamlplist_lib.yaml_plist import yaml_plist  # noqa: E402
import plistyamlplist  # noqa: E402


class TestYmlExtension(unittest.TestCase):
    def test_yml_file_converts_to_plist(self):
        with tempfile.TemporaryDirectory() as tmp:
            in_path = os.path.join(tmp, "sample.yml")
            out_path = os.path.join(tmp, "sample.plist")
            with open(in_path, "w", encoding="utf-8") as fp:
                fp.write("key1: value1\nkey2: 42\n")
            yaml_plist(in_path, out_path)
            self.assertTrue(os.path.isfile(out_path))
            with open(out_path, encoding="utf-8") as fp:
                contents = fp.read()
            self.assertIn("key1", contents)
            # yaml_plist() never closes its file handles (pre-existing); make
            # sure they are released so TemporaryDirectory cleanup works on
            # Windows, where open files cannot be unlinked.
            gc.collect()

    def test_main_routes_yml_as_yaml(self):
        # main() must not reject a .yml file as "not PLIST, JSON or YAML"
        seen = []

        def fake_yaml_plist(in_path, out_path):
            seen.append((in_path, out_path))

        real = plistyamlplist.yaml_plist
        plistyamlplist.yaml_plist = fake_yaml_plist
        old_argv = sys.argv
        try:
            sys.argv = ["plistyamlplist.py", "sample.yml", "out.plist"]
            plistyamlplist.main()
        except SystemExit as e:
            self.assertNotEqual(e.code, 1)
        finally:
            sys.argv = old_argv
            plistyamlplist.yaml_plist = real
        self.assertEqual(len(seen), 1)


if __name__ == "__main__":
    unittest.main()
