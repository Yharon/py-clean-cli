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

- Finalized project documentation and examples, including `scripts/examples/use_commands.py` demonstrating `hello` and `user` commands.
- Validation to ensure the provided package path is a valid Python package (checks for `__init__.py`).
- `CommandRegistryHelper` implemented with a singleton pattern using `__new__` and a `get_instance()` class method; backward compatibility kept via the global `COMMAND_REGISTRY`.

### Changed

- Translated CLI source code, comments, and user-facing messages to English.
- Expanded and standardized Google-style docstrings (Args, Returns, Raises) across the codebase.
- Codebase standardized to English-only coding standards and improved overall consistency.

### Fixed

- No user-facing bug fixes in this finalization release.

### Notes

- This release finalizes documentation, examples, and internal refactors completed during the 1.0.0 development cycle. See `[1.0.0] - 2025-09-05` for the initial release notes.

## [1.0.0] - 2025-09-05

### Added

- Initial release
