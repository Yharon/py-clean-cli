"""
Tests for CommandRegistryHelper class.

This module tests the singleton pattern, command registration,
retrieval, and cache management functionality.
"""

from dataclasses import dataclass

import pytest

from py_clean_cli.helpers import COMMAND_REGISTRY
from py_clean_cli.helpers.command_registry_helper import CommandRegistryHelper
from py_clean_cli.models import CommandArgsModel


class TestCommandRegistryHelper:
    """Test suite for CommandRegistryHelper class."""

    def test_singleton_pattern(self):
        """Test that CommandRegistryHelper implements singleton pattern."""
        instance1 = CommandRegistryHelper()
        instance2 = CommandRegistryHelper()
        instance3 = CommandRegistryHelper.get_instance()

        assert instance1 is instance2
        assert instance2 is instance3
        assert id(instance1) == id(instance2) == id(instance3)

    def test_global_registry_is_singleton(self):
        """Test that COMMAND_REGISTRY is the singleton instance."""
        instance = CommandRegistryHelper.get_instance()
        assert COMMAND_REGISTRY is instance

    def test_register_command(self, sample_command_class):
        """Test registering a command in the registry."""
        COMMAND_REGISTRY.register(
            name="test_cmd",
            help_text="Test command",
            command_class=sample_command_class
        )

        # Verify command was registered
        assert "test_cmd" in COMMAND_REGISTRY._command_cache
        assert COMMAND_REGISTRY._command_cache["test_cmd"] is sample_command_class

        # Verify command metadata was set
        assert sample_command_class.command_name == "test_cmd"
        assert sample_command_class.command_help == "Test command"

    def test_register_multiple_commands(self, sample_command_class):
        """Test registering multiple commands."""
        @dataclass
        class AnotherCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        COMMAND_REGISTRY.register("cmd1", "Command 1", sample_command_class)
        COMMAND_REGISTRY.register("cmd2", "Command 2", AnotherCommand)

        assert len(COMMAND_REGISTRY._command_cache) == 2
        assert "cmd1" in COMMAND_REGISTRY._command_cache
        assert "cmd2" in COMMAND_REGISTRY._command_cache

    def test_register_overwrites_existing_command(self, sample_command_class):
        """Test that registering a command with same name overwrites it."""
        @dataclass
        class NewCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        COMMAND_REGISTRY.register("duplicate", "First", sample_command_class)
        COMMAND_REGISTRY.register("duplicate", "Second", NewCommand)

        # Should have the second command
        assert COMMAND_REGISTRY._command_cache["duplicate"] is NewCommand
        assert NewCommand.command_help == "Second"

    def test_get_command_existing(self, sample_command_class):
        """Test retrieving an existing command."""
        COMMAND_REGISTRY.register("get_test", "Get test", sample_command_class)

        retrieved = COMMAND_REGISTRY.get_command("get_test")

        assert retrieved is sample_command_class
        assert retrieved.command_name == "get_test"

    def test_get_command_non_existing(self):
        """Test retrieving a non-existing command returns None."""
        result = COMMAND_REGISTRY.get_command("non_existing_command")
        assert result is None

    def test_get_all_commands_empty(self):
        """Test getting all commands when registry is empty."""
        commands = COMMAND_REGISTRY.get_all_commands()

        assert isinstance(commands, list)
        assert len(commands) == 0

    def test_get_all_commands_multiple(self, sample_command_class):
        """Test getting all commands when multiple are registered."""
        @dataclass
        class Command1(CommandArgsModel):
            def exec(self) -> None:
                pass

        @dataclass
        class Command2(CommandArgsModel):
            def exec(self) -> None:
                pass

        COMMAND_REGISTRY.register("cmd1", "Command 1", Command1)
        COMMAND_REGISTRY.register("cmd2", "Command 2", Command2)
        COMMAND_REGISTRY.register("cmd3", "Command 3", sample_command_class)

        commands = COMMAND_REGISTRY.get_all_commands()

        assert len(commands) == 3
        assert Command1 in commands
        assert Command2 in commands
        assert sample_command_class in commands

    def test_clear_registry(self, sample_command_class):
        """Test clearing the command registry."""
        # Register some commands
        COMMAND_REGISTRY.register("cmd1", "Command 1", sample_command_class)
        COMMAND_REGISTRY.register("cmd2", "Command 2", sample_command_class)

        assert len(COMMAND_REGISTRY._command_cache) == 2

        # Clear registry
        COMMAND_REGISTRY.clear_registry()

        assert len(COMMAND_REGISTRY._command_cache) == 0
        assert COMMAND_REGISTRY.get_all_commands() == []

    def test_registry_isolation_between_tests(self, sample_command_class):
        """
        Test that registry is properly isolated between tests.

        This test verifies that the reset_registry fixture works correctly.
        """
        # Registry should be empty at start due to fixture
        assert len(COMMAND_REGISTRY._command_cache) == 0

        # Register a command
        COMMAND_REGISTRY.register("isolated", "Isolated", sample_command_class)
        assert len(COMMAND_REGISTRY._command_cache) == 1
