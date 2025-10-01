"""
Tests for CommandsManager class.

This module tests the singleton pattern per parser, command registration,
argument parsing, and command execution functionality.
"""

from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest
from simple_parsing import ArgumentParser

from py_clean_cli.helpers import COMMAND_REGISTRY
from py_clean_cli.models import CommandArgsModel
from py_clean_cli.services.managers import CommandsManager


@pytest.fixture
def parser():
    """Fixture providing a fresh ArgumentParser instance."""
    return ArgumentParser(prog="test_cli")


@pytest.fixture
def manager(parser):
    """Fixture providing a CommandsManager instance."""
    # Clear any existing instances
    CommandsManager._instances.clear()
    return CommandsManager.get_instance(parser)


@pytest.fixture
def mock_command_class():
    """Fixture providing a mock command class."""
    @dataclass
    class MockCommand(CommandArgsModel):
        test_arg: str = "default"
        command_name = "mock_cmd"
        command_help = "Mock command for testing"

        def exec(self) -> None:
            print(f"Executing with: {self.test_arg}")

    return MockCommand


class TestCommandsManagerSingleton:
    """Test suite for CommandsManager singleton pattern."""

    def test_singleton_per_parser(self):
        """Test that CommandsManager implements singleton per parser."""
        parser1 = ArgumentParser(prog="cli1")
        parser2 = ArgumentParser(prog="cli2")

        # Clear instances for clean test
        CommandsManager._instances.clear()

        manager1a = CommandsManager.get_instance(parser1)
        manager1b = CommandsManager.get_instance(parser1)
        manager2 = CommandsManager.get_instance(parser2)

        # Same parser should return same instance
        assert manager1a is manager1b
        assert id(manager1a) == id(manager1b)

        # Different parser should return different instance
        assert manager1a is not manager2
        assert id(manager1a) != id(manager2)

    def test_get_instance_creates_manager(self, parser):
        """Test that get_instance creates a new manager."""
        CommandsManager._instances.clear()

        manager = CommandsManager.get_instance(parser)

        assert isinstance(manager, CommandsManager)
        assert manager.parser is parser

    def test_direct_instantiation_uses_singleton(self, parser):
        """Test that direct instantiation also uses singleton pattern."""
        CommandsManager._instances.clear()

        manager1 = CommandsManager(parser)
        manager2 = CommandsManager(parser)

        assert manager1 is manager2


class TestCommandsManagerInitialization:
    """Test suite for CommandsManager initialization."""

    def test_post_init_creates_subparsers(self, manager):
        """Test that __post_init__ creates subparsers."""
        assert manager.subparsers is not None

    def test_initial_state(self, manager):
        """Test initial state of CommandsManager."""
        assert isinstance(manager.commands, dict)
        assert len(manager.commands) == 0
        assert isinstance(manager._registered_parsers, set)
        assert len(manager._registered_parsers) == 0


class TestCommandsManagerRegistration:
    """Test suite for command registration."""

    def test_register_command(self, manager, mock_command_class):
        """Test registering a single command."""
        manager.register_command(mock_command_class)

        assert "mock_cmd" in manager.commands
        assert manager.commands["mock_cmd"] is mock_command_class
        assert "mock_cmd" in manager._registered_parsers

    def test_register_command_returns_self(self, manager, mock_command_class):
        """Test that register_command returns self for chaining."""
        result = manager.register_command(mock_command_class)

        assert result is manager

    def test_register_command_twice_skips_second(self, manager, mock_command_class):
        """Test that registering same command twice skips the second registration."""
        manager.register_command(mock_command_class)
        initial_count = len(manager._registered_parsers)

        # Register again
        manager.register_command(mock_command_class)

        # Should not add duplicate
        assert len(manager._registered_parsers) == initial_count

    def test_register_multiple_commands(self, manager):
        """Test registering multiple different commands."""
        @dataclass
        class Command1(CommandArgsModel):
            command_name = "cmd1"
            command_help = "Command 1"

            def exec(self) -> None:
                pass

        @dataclass
        class Command2(CommandArgsModel):
            command_name = "cmd2"
            command_help = "Command 2"

            def exec(self) -> None:
                pass

        manager.register_command(Command1).register_command(Command2)

        assert len(manager.commands) == 2
        assert "cmd1" in manager.commands
        assert "cmd2" in manager.commands

    def test_register_all_commands_from_registry(self, manager):
        """Test registering all commands from global registry."""
        @dataclass
        class RegCommand1(CommandArgsModel):
            def exec(self) -> None:
                pass

        @dataclass
        class RegCommand2(CommandArgsModel):
            def exec(self) -> None:
                pass

        # Register in global registry
        COMMAND_REGISTRY.register("reg_cmd1", "Registry Command 1", RegCommand1)
        COMMAND_REGISTRY.register("reg_cmd2", "Registry Command 2", RegCommand2)

        manager.register_all_commands()

        assert len(manager.commands) >= 2
        assert "reg_cmd1" in manager.commands
        assert "reg_cmd2" in manager.commands

    def test_register_all_commands_returns_self(self, manager):
        """Test that register_all_commands returns self for chaining."""
        result = manager.register_all_commands()

        assert result is manager

    def test_register_all_commands_empty_registry(self, manager):
        """Test register_all_commands when registry is empty."""
        # Should not raise error
        manager.register_all_commands()

        assert len(manager.commands) == 0


class TestCommandsManagerRetrieval:
    """Test suite for command retrieval."""

    def test_get_command_class_existing(self, manager, mock_command_class):
        """Test retrieving an existing command class."""
        manager.register_command(mock_command_class)

        retrieved = manager.get_command_class("mock_cmd")

        assert retrieved is mock_command_class

    def test_get_command_class_from_global_registry(self, manager):
        """Test retrieving command from global registry if not in local."""
        @dataclass
        class GlobalCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        COMMAND_REGISTRY.register("global_cmd", "Global", GlobalCommand)

        # Not registered in manager yet
        assert "global_cmd" not in manager.commands

        # Should fetch from global registry and register
        retrieved = manager.get_command_class("global_cmd")

        assert retrieved is GlobalCommand
        assert "global_cmd" in manager.commands

    def test_get_command_class_non_existing(self, manager):
        """Test retrieving non-existing command raises ValueError."""
        with pytest.raises(ValueError, match="Unknown command: non_existing"):
            manager.get_command_class("non_existing")


class TestCommandsManagerExecution:
    """Test suite for command parsing and execution."""

    def test_parse_and_execute_success(self, manager, mock_command_class):
        """Test successful command parsing and execution."""
        manager.register_command(mock_command_class)

        with patch("sys.argv", ["test_cli", "mock_cmd", "--test_arg", "custom"]):
            with patch.object(mock_command_class, "exec") as mock_exec:
                # Need to create actual instance for parsing
                manager.parse_and_execute()

                # Verify command was parsed (exact assertion depends on implementation)
                # This is a basic check that no exception was raised

    def test_parse_and_execute_with_error_propagates(self, manager, mock_command_class):
        """Test that execution errors are propagated."""
        @dataclass
        class ErrorCommand(CommandArgsModel):
            command_name = "error_cmd"
            command_help = "Error command"

            def exec(self) -> None:
                raise RuntimeError("Command failed")

        manager.register_command(ErrorCommand)

        with patch("sys.argv", ["test_cli", "error_cmd"]):
            with pytest.raises(RuntimeError, match="Command failed"):
                manager.parse_and_execute()

    def test_method_chaining(self, manager):
        """Test that methods support chaining pattern."""
        @dataclass
        class ChainCommand1(CommandArgsModel):
            command_name = "chain1"
            command_help = "Chain 1"

            def exec(self) -> None:
                pass

        @dataclass
        class ChainCommand2(CommandArgsModel):
            command_name = "chain2"
            command_help = "Chain 2"

            def exec(self) -> None:
                pass

        # Should be able to chain
        result = manager.register_command(ChainCommand1).register_command(ChainCommand2)

        assert result is manager
        assert len(manager.commands) == 2
