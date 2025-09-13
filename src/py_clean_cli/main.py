from pathlib import Path
from typing import Optional
from logging import getLogger
from inspect import getmodule, getfile, stack

from simple_parsing import ArgumentParser

from py_clean_cli.helpers import discover_commands
from py_clean_cli.services import CommandsManager


LOGGER = getLogger(__name__)


def package_cli(package_path: Optional[str] = None):
    """
    Set up the CLI for the package.

    Args:
        package_path (Optional[str]): Path to the package directory. If None, attempts to
            determine it from the calling module.

    Raises:
        ValueError: If the package path cannot be determined or is not a valid directory.
    """
    if package_path is None:
        # Get the frame of the caller (1 level up in the stack)
        caller_frame = stack()[1]
        caller_module = getmodule(caller_frame[0])

        if caller_module is not None:
            module_file = getfile(caller_module)
            package_path = str(Path(module_file).parent)

            # Log information about the caller
            module_name = caller_module.__name__
            LOGGER.debug(f"Called from module: {module_name}")
            LOGGER.debug(f"Module file path: {module_file}")
            LOGGER.debug(f"Using package path: {package_path}")

    # Validate if the path is a directory
    if package_path is None or not Path(package_path).is_dir():
        raise ValueError(
            f"The provided package_path '{package_path}' is not a valid directory."
        )

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

    parser = ArgumentParser()
    factory = CommandsManager.get_instance(parser)

    factory.register_all_commands()
    factory.parse_and_execute()
