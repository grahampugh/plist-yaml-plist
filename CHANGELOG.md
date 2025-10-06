# plistyamlplist Change Log

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## [unreleased]

- Added unit tests to project.

## [v0.6.4] - 2022-06-21 - v0.6.4

- Fixed the installation of ruamel.yaml if not already present.
- Limit the ruamel.yaml version to less than 0.18.0, because newer versions are completely changed so will need more work to fix. Note that if you already have a newer version of ruamel.yaml in the python that you are using, it is advised to run the following command to remove it, after which running this script will reinstall a working version:

```
/path/to/your/python -m pip uninstall ruamel.yaml
```

## [v0.6.3] - 2022-06-21 - v0.6.3

- Fixed running on folders without a destination when converting from YAML to PLIST or vice versa.

## [v0.6.1] - 2021-04-26 - v0.6.1

- Adding `ParentRecipeTrustInfo` to the `desired_order` dict so that when autopkg recipes are converted or tidied, the Trust Info is retained. Also adding this to the processors which gain a new line before them for readability (#10 - thanks to @smithjw).

## [v0.6.0] - 2021-02-23 - v0.6.0

- When converting an AutoPkg recipe to `yaml` format, specific formatting is carried out:
  - The different process dictionaries are ordered by Processor, Comment, Arguments.
  - The Input dictionary is ordered such that NAME is always at the top.
  - The items are ordered thus: Comment, Description, Identifier, ParentRecipe, MinimumVersion, Input, Process
  - Blank lines are added for human readability. Specifically these are added above Input and Process dictionaries, and between each Processor dictionary.
- You can use `yaml_tidy.py` to reformat existing `.recipe.yaml` files as above.
- An entire directory structure can have `.recipe.yaml` files reformatted as above using the command `plistyamlplist /path/to/YAML --tidy`. Any directory with a `YAML` or `_YAML` folder in it will be processed, including subdirectories.

## [v0.5.0] - 2021-02-11 - v0.5.0

- Switched from `pyyaml` to `ruamel.yaml`.

## [v0.4.0] - 2021-02-10 - v0.4.0

- You can now use this tool to convert `json` > `plist`. Note that the `plist` format do not accept `null`/`None` values, so this script will extract any keys with `null`/`None` values before converting.
- Add the ability to just reference a folder if `JSON` is in the path.
- You can now use `_JSON` as well as `JSON` for the folder.
- `pyyaml` is installed automatically if not already installed.

## [v0.3.1] - 2020-12-15 - v0.3.1

- Add the ability to just reference a folder if `YAML` is in the path.
- You can now use `_YAML` as well as `YAML` for the folder.

## [v0.3] - 2020-09-14 - v0.3

- Added the ability to convert an entire directory of `.yaml` files at once using the syntax:

  ```
  plistyamlplist /path/to/YAML/\*.yaml
  ```

## [v0.2] - 2020-03-06 - v0.2

- Merged in changes from @homebysix.

## v0.1 - 2020-03-06 - v0.1

- Initial Release (though the tool has been around for some time).

[unreleased]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.6.4...HEAD
[v0.6.4]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.6.3...v0.6.4
[v0.6.3]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.6.1...v0.6.3
[v0.6.1]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.6.0...v0.6.1
[v0.6.0]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.5.0...v0.6.0
[v0.5.0]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.4.0...v0.5.0
[v0.4.0]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.3.1...v0.4.0
[v0.3.1]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.3...v0.3.1
[v0.3]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.2...v0.3
[v0.2]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.1...v0.2
