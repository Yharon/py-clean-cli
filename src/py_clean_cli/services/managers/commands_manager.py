from functools import lru_cache
from dataclasses import dataclass, field as dc_field
from logging import getLogger, Logger
from typing import Any, Dict, Type, ClassVar, Set

from simple_parsing import ArgumentParser

from py_clean_cli.helpers import COMMAND_REGISTRY
from py_clean_cli.models import CommandArgsModel

# 💡 NOTE: Using logger instance (not direct imports) for better namespace control in library code
LOGGER: Logger = getLogger(__name__)


@dataclass
class CommandsManager:
    """
    Commands manager that handles registration and execution of CLI commands.

    This manager class maintains a registry of commands, handles argument parsing,
    and manages the execution flow using a singleton pattern per parser instance.

    Attributes:
        parser: The main argument parser instance.
        subparsers: Subparser for handling multiple commands.
        commands: Dictionary mapping command names to their classes.
        _registered_parsers: Set of already registered parser names.
    """

    _instances: ClassVar[Dict[int, "CommandsManager"]] = {}

    parser: ArgumentParser
    subparsers: Any = None
    commands: Dict[str, Type[CommandArgsModel]] = dc_field(default_factory=dict)
    _registered_parsers: Set[str] = dc_field(default_factory=set, init=False)

    def __post_init__(self):
        """
        Initialize the subparsers after instance creation.
        """
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        LOGGER.debug("Initialized subparsers for command handling")

    def __new__(cls, parser: ArgumentParser):
        """
        Implement singleton pattern per parser instance.
        """
        parser_id = id(parser)
        if parser_id not in cls._instances:
            LOGGER.debug(
                "Creating new CommandsManager instance for parser ID: " f"{parser_id}"
            )
            instance = super().__new__(cls)
            cls._instances[parser_id] = instance
        else:
            LOGGER.debug(
                "Reusing existing CommandsManager instance for parser ID: "
                f"{parser_id}"
            )
        return cls._instances[parser_id]

    @classmethod
    def get_instance(cls, parser: ArgumentParser) -> "CommandsManager":
        """
        Get or create a manager instance (singleton per parser).

        Args:
            parser (ArgumentParser): The ArgumentParser instance to use.

        Returns:
            CommandsManager: The singleton instance for the given parser.
        """
        return cls(parser=parser)

    def register_command(
        self, command_class: Type[CommandArgsModel]
    ) -> "CommandsManager":
        """
        Register a command in the manager using its internal metadata.

        The command will not be registered again if already present.

        Args:
            command_class (Type[CommandArgsModel]): The command class to register.

        Returns:
            CommandsManager: Self for method chaining.
        """
        name = command_class.command_name
        if name in self._registered_parsers:
            LOGGER.debug(f"Command '{name}' already registered, skipping")
            return self

        help_text = command_class.command_help
        LOGGER.debug(f"Registering command '{name}' with help: '{help_text}'")

        subparser = self.subparsers.add_parser(name=name, help=help_text)
        subparser.add_arguments(command_class, dest=name)
        self.commands[name] = command_class
        self._registered_parsers.add(name)
        LOGGER.debug(f"Command '{name}' successfully registered")
        return self

    def register_all_commands(self) -> "CommandsManager":
        """
        Register all available commands from the global registry.

        Returns:
            CommandsManager: Self for method chaining.
        """
        all_commands = COMMAND_REGISTRY.get_all_commands()
        LOGGER.debug(f"Found {len(all_commands)} commands in registry")

        if not all_commands:
            LOGGER.warning(
                "No commands found in registry. CLI will have no available commands."
            )

        for cmd_class in all_commands:
            LOGGER.debug(f"Registering command: {cmd_class.command_name}")
            self.register_command(cmd_class)

        LOGGER.debug(f"Total registered commands: {len(self._registered_parsers)}")
        return self

    @lru_cache(maxsize=32)
    def get_command_class(self, command_name: str) -> Type[CommandArgsModel]:
        """
        Retrieve a command class by name (with cache).

        Args:
            command_name (str): The name of the command to retrieve.

        Returns:
            Type[CommandArgsModel]: The command class.

        Raises:
            ValueError: If the command is unknown.
        """
        if command_name not in self.commands:
            LOGGER.debug(
                f"Command '{command_name}' not in local registry, checking global registry"
            )
            cmd_class = COMMAND_REGISTRY.get_command(command_name)
            if cmd_class:
                LOGGER.debug(
                    f"Found command '{command_name}' in global registry, registering"
                )
                self.register_command(cmd_class)
            else:
                LOGGER.error(f"Unknown command: {command_name}")
                raise ValueError(f"Unknown command: {command_name}")
        return self.commands[command_name]

    def parse_and_execute(self) -> None:
        """
        Parse arguments, instantiate the appropriate command and execute it.

        This method handles the complete flow from argument parsing to
        command execution.
        """
        try:
            args = self.parser.parse_args()

            command_name = args.command
            LOGGER.debug(f"Executing command: {command_name}")

            command_config = args.__dict__[command_name]
            LOGGER.debug(f"Command configuration: {command_config}")

            command_config.exec()
            LOGGER.debug(f"Command '{command_name}' execution completed")

        except Exception as e:
            LOGGER.error(f"Error during command execution: {e}")
            raise
