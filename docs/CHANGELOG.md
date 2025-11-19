# Changelog

**Last modified: 2025-11-19**

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-11-19

### Added
- Initial public release
- MIT License
- Pre-commit hooks with Trivy security scanning (fs + config)
- `Akamai` base API client with EdgeGrid authentication
- `search-asw` CLI tool for searching account switch keys
- Support for Python 3.9+

### Changed
- Renamed from `akamai-utils` to `akamai-wrapper-pub`
- Cleaned documentation for public consumption
- Refactored error handling in API client (DRY principle)

### Security
- Added Trivy vulnerability scanning
- Removed internal references and sensitive data
