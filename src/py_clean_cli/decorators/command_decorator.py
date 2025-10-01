from logging import getLogger, Logger

from py_clean_cli.helpers import COMMAND_REGISTRY

# 💡 NOTE: Using logger instance (not direct imports) for better namespace control in library code
LOGGER: Logger = getLogger(__name__)


def command(name: str, help_text: str = ""):
    """
    Decorator to register a command class in the global command registry.

    Args:
        name (str): The name of the command.
        help_text (str): Help text for the command.

    Returns:
        Callable: The decorator function.
    """
    def decorator(cls):
        LOGGER.debug(f"Registering command '{name}' in the decorator")
        COMMAND_REGISTRY.register(name, help_text, cls)
        return cls
    return decorator
