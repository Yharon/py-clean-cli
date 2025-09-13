from functools import lru_cache
from dataclasses import dataclass, field as dc_field
from typing import Any, Dict, Type, ClassVar,Set

from simple_parsing import ArgumentParser

from py_clean_cli.helpers import COMMAND_REGISTRY
from py_clean_cli.models import CommandArgsModel


@dataclass
class CommandsFactory:
    """
    Commands factory that manages registration and execution.

    This factory class handles command registration, parsing, and execution
    using a singleton pattern per parser instance.

    Attributes:
        parser: The main argument parser instance.
        subparsers: Subparser for handling multiple commands.
        commands: Dictionary mapping command names to their classes.
        _registered_parsers: Set of already registered parser names.
    """

    _instances: ClassVar[Dict[int, "CommandsFactory"]] = {}

    parser: ArgumentParser
    subparsers: Any = None
    commands: Dict[str, Type[CommandArgsModel]] = dc_field(default_factory=dict)
    _registered_parsers: Set[str] = dc_field(default_factory=set, init=False)

    def __post_init__(self):
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)

    def __new__(cls, parser: ArgumentParser):
        """
        Implement singleton pattern per parser instance.

        Args:
            parser: The ArgumentParser instance to use.

        Returns:
            CommandsFactory: The singleton instance for the given parser.
        """
        parser_id = id(parser)
        if parser_id not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[parser_id] = instance
        return cls._instances[parser_id]

    @classmethod
    def get_instance(cls, parser: ArgumentParser) -> "CommandsFactory":
        """
        Get or create a factory instance (singleton per parser).

        Args:
            parser (ArgumentParser): The ArgumentParser instance to use.

        Returns:
            CommandsFactory: The singleton instance for the given parser.
        """
        return cls(parser=parser)

    def register_command(
        self, command_class: Type[CommandArgsModel]
    ) -> "CommandsFactory":
        """
        Register a command using its internal metadata (with cache).

        The command will not be registered again if already present.

        Args:
            command_class (Type[CommandArgsModel]): The command class to register.

        Returns:
            CommandsFactory: Self for method chaining.
        """
        name = command_class.command_name
        if name in self._registered_parsers:
            return self

        help_text = command_class.command_help
        subparser = self.subparsers.add_parser(name=name, help=help_text)
        subparser.add_arguments(command_class, dest=name)
        self.commands[name] = command_class
        self._registered_parsers.add(name)
        return self

    def register_all_commands(self) -> "CommandsFactory":
        """
        Automatically register all commands from the global registry.

        Returns:
            CommandsFactory: Self for method chaining.
        """
        all_commands = COMMAND_REGISTRY.get_all_commands()
        print(f"Commands found in registry: {len(all_commands)}")
        for cmd_class in all_commands:
            print(f"Registering command: {cmd_class.command_name}")
            self.register_command(cmd_class)
        return self

    @lru_cache(maxsize=32)
    def get_command_class(self, command_name: str) -> Type[CommandArgsModel]:
        """
        Get a command class by name (with cache).

        Args:
            command_name (str): The name of the command to retrieve.

        Returns:
            Type[CommandArgsModel]: The command class.

        Raises:
            ValueError: If the command is unknown.
        """
        if command_name not in self.commands:
            cmd_class = COMMAND_REGISTRY.get_command(command_name)
            if cmd_class:
                self.register_command(cmd_class)
            else:
                raise ValueError(f"Unknown command: {command_name}")
        return self.commands[command_name]

    def parse_and_execute(self) -> None:
        """
        Parse arguments, instantiate the appropriate command and execute it.

        This method handles the complete flow from argument parsing to
        command execution.
        """
        args = self.parser.parse_args()
        command_name = args.command
        command_config = args.__dict__[command_name]
        command_config.exec()
