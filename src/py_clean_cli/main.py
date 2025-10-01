from pathlib import Path
from sys import argv as sys_argv
from typing import Optional
from logging import getLogger, DEBUG, Logger
from inspect import getmodule, getfile, stack

from simple_parsing import ArgumentParser

from py_clean_cli.helpers import discover_commands
from py_clean_cli.services import CommandsManager

# 💡 NOTE: Using logger instance (not direct imports) for better namespace control in library code
LOGGER: Logger = getLogger(__name__)


def package_cli(package_path: Optional[str] = None) -> None:
    """
    Set up the CLI for the package.

    Args:
        package_path (Optional[str]): Path to the package directory. If None, attempts to
            determine it from the calling module.

    Raises:
        ValueError: If the package path cannot be determined or is not a valid directory.
    """

    if '--verbose' in sys_argv:
        LOGGER.setLevel(DEBUG)
        LOGGER.debug("`--verbose` mode enabled. Log level set to DEBUG.")

    if package_path is None:
        # Get the frame of the caller (1 level up in the stack)
        caller_frame = stack()[1]
        caller_module = getmodule(caller_frame[0])
        if caller_module is None:
            raise ValueError("Could not determine the caller module.")
        module_file = getfile(caller_module)
        package_path = str(Path(module_file).parent)

    if not Path(package_path).is_dir():
        raise ValueError(f"The provided package_path '{package_path}' is not a valid directory.")

    # Log information about the package
    module_name = Path(package_path).name
    LOGGER.debug(f"Called from module: {module_name}")
    LOGGER.debug(f"Module file path: {package_path}")

    # Check if it's a valid Python package (has __init__.py)
    init_file = Path(package_path) / "__init__.py"
    if not init_file.exists():
        LOGGER.warning(
            f"The directory '{package_path}' does not contain __init__.py file. "
            "It may not be a valid Python package."
        )
    else:
        LOGGER.debug(
            f"Confirmed: '{package_path}' is a valid Python package with __init__.py file."
        )

    discover_commands(package_path)
    parser = ArgumentParser(prog=module_name)
    manager = CommandsManager.get_instance(parser)

    manager.register_all_commands()
    manager.parse_and_execute()
