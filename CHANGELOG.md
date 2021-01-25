# plistyamlplist Change Log

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## [unreleased]

## [v0.4.0] - 2020-12-15 - v0.4.0

- You can now use this tool to convert `json` > `plist`. Note that the `plist` format do not accept `null`/`None` values, so this script will extract any keys with `null`/`None` values before converting.
- Add the ability to just reference a folder if `JSON` is in the path.
- You can now use `_JSON` as well as `JSON` for the folder.

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

[unreleased]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.4.0...HEAD
[v0.4.0]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.3.1...v0.4.0
[v0.3.1]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.3...v0.3.1
[v0.3]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.2...v0.3
[v0.2]: https://github.com/grahampugh/plist-yaml-plist/compare/v0.1...v0.2
