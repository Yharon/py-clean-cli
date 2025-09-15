from sys import path as sys_path
from pathlib import Path
from typing import Optional, List
from inspect import getmodule, getfile
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from logging import getLogger

# Initialize logger
LOGGER = getLogger(__name__)

PROJECT_ROOT = str(Path.cwd())
if PROJECT_ROOT not in sys_path:
    sys_path.insert(0, PROJECT_ROOT)


def discover_commands(package_path: str) -> None:
    """
    Dynamically discovers and loads commands from a package.

    This function recursively searches through the specified package directory
    for Python files, importing each one to make commands available to the CLI.

    Args:
        package_path (str): Path to the package directory containing commands.
    """
    LOGGER.debug(f"Discovering commands in package: {package_path}")
    python_files = _find_python_files(package_path)

    for file in python_files:
        _import_module_from_file(file)


def _find_python_files(package_path: str) -> List[Path]:
    """
    Recursively finds all Python files in the given package path.

    Args:
        package_path (str): Directory path to search for Python files.

    Returns:
        List[Path]: List of Path objects for Python files (excluding those starting with underscore)
    """
    package_dir = Path(package_path)
    LOGGER.debug(f"Searching for Python files in: {package_dir}")

    # Find all .py files, excluding those starting with underscore
    return [file for file in package_dir.rglob("*.py") if not file.name.startswith("_")]


def _import_module_from_file(file: Path) -> None:
    """
    Imports a Python module from a file path.

    Attempts standard import first, falls back to spec-based import if needed.

    Args:
        file (Path): Path to the Python file to import.
    """
    try:
        # Try standard relative import first
        rel_path = file.relative_to(Path(PROJECT_ROOT))
        parts = rel_path.with_suffix("").parts
        module_path = ".".join(parts)

        LOGGER.debug(f"Importing module: {module_path}")
        import_module(module_path)
        LOGGER.debug(f"Successfully imported: {module_path}")

    except (ImportError, ValueError) as e:
        LOGGER.warning(f"Error importing module {file.name}: {e}")

        # Try alternative import using spec
        try:
            module_name = file.stem
            spec = spec_from_file_location(module_name, file)

            if spec and spec.loader:
                module = module_from_spec(spec)
                spec.loader.exec_module(module)
                LOGGER.info(f"Module {module_name} imported successfully using spec")
            else:
                LOGGER.warning(f"Could not create spec for {file}")

        except Exception as e2:
            LOGGER.error(f"Failed to import {file.name} using spec: {e2}")
