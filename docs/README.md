# py-clean-cli

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

py-clean-cli is a lightweight framework for building well-documented, decorator-based Python command-line interfaces (CLIs).

## Overview

py-clean-cli provides a simple structure to create Python CLIs using decorators to register commands and dataclass-based argument models. The library favors clear documentation and example-driven usage.

## Key Features

- **Decorator-based command registration** (`@command`)
- **Dataclass models** for command arguments (`CommandArgsModel`) with `simple_parsing` support
- **Command discovery and registration** helpers across packages
- **Singleton pattern** `CommandRegistryHelper` with backward-compatible global `COMMAND_REGISTRY`
- **Google-style docstrings** and English-only code for automated documentation
- **Runnable examples** included in `scripts/examples/`

## What's Included

- Core library to register and run commands using the `@command` decorator
- Argument modeling using `dataclasses` and `simple_parsing` via `CommandArgsModel`
- Helpers for command discovery and registration (`CommandRegistryHelper`) implemented with a singleton pattern and backward-compatible global registry
- Runnable examples in `scripts/examples/use_commands.py` demonstrating basic and advanced command usage
- Google-style docstrings and English-only code/comments to support automated documentation and consistent style

## Installation

This project is provided as source. To install in editable mode (dev):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Quick Start

Run the hello example:

```powershell
python -m scripts.examples.use_commands hello --name "World" --greet "Hi" --upper
```

## Usage

Run the packaged examples module to explore available commands:

```powershell
python -m scripts.examples.use_commands --help
```

## Examples

### Greet someone:

```powershell
python -m scripts.examples.use_commands hello --name "World" --greet "Hi" --upper
```

### User create (dry-run):

```powershell
python -m scripts.examples.use_commands user create --email "test@example.com" --username "testuser" --dry_run
```

Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Run tests and linters (if any) and open a PR describing your changes.

License

See `docs/LICENSE` for license details.

Contact

For questions or support, open an issue in the project repository or contact the maintainer.
