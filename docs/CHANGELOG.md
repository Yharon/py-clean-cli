---
name: "📝 Changelog"
about: "Keep your changelog up to date"
title: "[CHANGELOG] "
labels: "changelog"
assignees: ''
---

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- Added validation to check if the provided package path is a valid Python package with __init__.py file

### Fixed

-

### Changed

- Translated all Portuguese content in `commands_factory.py` to English including docstrings, comments, print messages, and error messages
- Enhanced documentation with detailed Google Style docstrings including Args, Returns, and Raises sections
- Improved code consistency by following English-only coding standards
- Implemented singleton pattern in `CommandRegistryHelper` using `__new__` method
- Added `get_instance()` class method for obtaining singleton registry instance
- Enhanced documentation with detailed docstrings explaining singleton behavior
- Maintained backward compatibility with global `COMMAND_REGISTRY` variable

### Fixed

-

### Identified Issues (Unresolved)

## [1.0.0] - 2025-09-05

### Added

- Initial release
