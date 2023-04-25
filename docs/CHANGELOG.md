# Changelog

## [0.2.1] - 2023-04-26

### Added

### Changed

### Fixed
    - Changed hardcoded patterns to regexp
    - Grab tag_name if release is None

## [0.2.0] - 2023-04-25

### Added
    - Add support for scanning helm chart
    - Can provide GITHUB_TOKEN to extend api rate 60 => 5000 per hour
    - Support for list indexes in yaml path

### Changed
    - Make some config fields optional (specified in readme)
    - Basic refactoring (docstrings, code re-usability)

### Fixed 

## [0.1.0] - 2023-04-10

### Added
    - Inital project creation
    - Scrape version and release notes from github
    - Check local version based on YAML path
    - Support for PR/MR in gitlab, github, bitbucket
    - Slack notifications

### Changed

### Fixed 