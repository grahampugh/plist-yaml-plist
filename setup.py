from setuptools import setup, find_packages

setup(
    name="plistyamlplist",
    version="0.4.0",
    packages=find_packages(include=["plistyamlplist_lib", "plistyamlplist_lib.*"]),
    install_requires=["pyyaml"],
)
