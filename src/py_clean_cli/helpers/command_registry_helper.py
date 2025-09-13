"""
Global registry for CLI commands.
"""

from dataclasses import dataclass, field as dc_field
from typing import Dict, Type, List, Optional, Any, ClassVar


@dataclass
class CommandRegistryHelper:
    """
    Command registry with cache using singleton pattern.

    This registry ensures a single instance exists to manage all CLI commands
    throughout the application lifecycle.
    """

    _instance: ClassVar[Optional["CommandRegistryHelper"]] = None
    _command_cache: Dict[str, Type[Any]] = dc_field(default_factory=dict, init=False)

    def __new__(cls) -> "CommandRegistryHelper":
        """
        Implement singleton pattern to ensure only one registry exists.

        Returns:
            CommandRegistryHelper: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "CommandRegistryHelper":
        """
        Get the singleton instance of the command registry.

        Returns:
            CommandRegistryHelper: The singleton registry instance.
        """
        return cls()

    def register(self, name: str, help_text: str, command_class: Type[Any]) -> None:
        """
        Register a command in the registry.

        Args:
            name (str): Command name.
            help_text (str): Help text for the command.
            command_class (Type[Any]): Class that implements the command.
        """
        command_class.command_name = name
        command_class.command_help = help_text
        self._command_cache[name] = command_class

    def get_all_commands(self) -> List[Type[Any]]:
        """
        Returns all registered commands.

        Returns:
            List[Type[Any]]: List of all registered command classes.
        """
        return list(self._command_cache.values())

    def get_command(self, name: str) -> Optional[Type[Any]]:
        """
        Get a command by name.

        Args:
            name (str): The name of the command to retrieve.

        Returns:
            Optional[Type[Any]]: The command class if found, None otherwise.
        """
        return self._command_cache.get(name)

    def clear_registry(self) -> None:
        """
        Clear the command registry.
        """
        self._command_cache.clear()


# 💡 NOTE: Global convenience variable for backward compatibility
COMMAND_REGISTRY = CommandRegistryHelper.get_instance()
