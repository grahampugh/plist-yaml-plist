#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from plistlib import dump

from plistyamlplist_lib.version import __version__

VERSION = __version__

BUILDINFO = "pkg/plistyamlplist/build-info.plist"
pl = dict(
    distribution_style=False,
    identifier="com.github.grahampugh.plistyamlplist",
    install_location="/",
    name=f"plistyamlplist-{VERSION}.pkg",
    ownership="recommended",
    postinstall_action="none",
    suppress_bundle_relocation=True,
    version=VERSION,
)
with open(BUILDINFO, "wb") as fp:
    dump(pl, fp)
    print(f"Wrote {VERSION} to: {BUILDINFO}")
