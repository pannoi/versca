# Changelog

## [0.2.4] - 2023-05-10

### Added
  - Scan tags if there are not releases in OSS

### Changed

### Fixed
  - Support `v` prefix with suffix in release version
  - Store in local_path, not in tool_name

## [0.2.3] - 2023-05-10

### Added
  - Slack notification on fail

### Changed

### Fixed
  - Keep scanning, if one tool scan failed
  - Check if slack/autoMR are defined in configuration
  - Delete src branch usage

## [0.2.2] - 2023-04-27

### Added
  - Bot parameter to delete src branch after merge

### Changed
  - Support for version with prefixes (F.E. Docker images)
  - Increase yaml path max depth from 5 to 7

### Fixed
  - Fix logging comments to proper datatypes

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