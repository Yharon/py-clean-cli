# py-clean-cli

py-clean-cli is a lightweight framework for building well-documented, decorator-based Python command-line interfaces (CLIs).

What's included

- Core library to register and run commands using the `@command` decorator.
- Argument modeling using `dataclasses` and `simple_parsing` via `CommandArgsModel`.
- Helpers for command discovery and registration (`CommandRegistryHelper`) implemented with a singleton pattern and backward-compatible global registry.
- Runnable examples in `scripts/examples/use_commands.py` demonstrating basic and advanced command usage.
- Google-style docstrings and English-only code/comments to support automated documentation and consistent style.

Quick start

1. Run the hello example:

```powershell
python -m scripts.examples.use_commands hello --name "World"
```

1. Run a user create dry-run:

```powershell
python -m scripts.examples.use_commands user create --email "test@example.com" --username "testuser" --dry_run
```

1. Package CLI entrypoint:

- Use `package_cli()` from the library or the project's entrypoint module to expose the CLI for distribution.


Where to look next

- `docs/CHANGELOG.md` — changelog and release history.
- `scripts/examples/` — runnable examples to test and explore features.
- `src/py_clean_cli/` — core implementation: decorators, helpers, models and services.

License

- See `docs/LICENSE` for license terms.

If you'd like a longer README (badges, CI, contribution guidelines), tell me what to include and I will expand it.
