"""
Tests for @command decorator.

This module tests the command decorator functionality including
registration, metadata assignment, and interaction with the registry.
"""

from dataclasses import dataclass

import pytest

from py_clean_cli.decorators import command
from py_clean_cli.helpers import COMMAND_REGISTRY
from py_clean_cli.models import CommandArgsModel


class TestCommandDecorator:
    """Test suite for @command decorator."""

    def test_decorator_registers_command(self):
        """Test that @command decorator registers command in registry."""
        @command(name="test_register", help_text="Test registration")
        @dataclass
        class TestCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        # Verify command was registered
        assert "test_register" in COMMAND_REGISTRY._command_cache
        assert COMMAND_REGISTRY.get_command("test_register") is TestCommand

    def test_decorator_sets_command_metadata(self):
        """Test that decorator sets command_name and command_help attributes."""
        @command(name="metadata_test", help_text="This is help text")
        @dataclass
        class MetadataCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        assert MetadataCommand.command_name == "metadata_test"
        assert MetadataCommand.command_help == "This is help text"

    def test_decorator_with_empty_help_text(self):
        """Test decorator works with empty help text."""
        @command(name="no_help")
        @dataclass
        class NoHelpCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        assert NoHelpCommand.command_name == "no_help"
        assert NoHelpCommand.command_help == ""
        assert COMMAND_REGISTRY.get_command("no_help") is NoHelpCommand

    def test_decorator_returns_class_unchanged(self):
        """Test that decorator returns the original class unchanged."""
        @dataclass
        class OriginalCommand(CommandArgsModel):
            value: int = 42

            def exec(self) -> None:
                pass

        decorated = command(name="unchanged", help_text="Test")(OriginalCommand)

        # Class should still be the same type
        assert decorated is OriginalCommand
        assert decorated.value == 42

    def test_decorator_with_multiple_commands(self):
        """Test decorating multiple commands."""
        @command(name="cmd1", help_text="Command 1")
        @dataclass
        class Command1(CommandArgsModel):
            def exec(self) -> None:
                pass

        @command(name="cmd2", help_text="Command 2")
        @dataclass
        class Command2(CommandArgsModel):
            def exec(self) -> None:
                pass

        @command(name="cmd3", help_text="Command 3")
        @dataclass
        class Command3(CommandArgsModel):
            def exec(self) -> None:
                pass

        # All commands should be registered
        assert len(COMMAND_REGISTRY.get_all_commands()) == 3
        assert COMMAND_REGISTRY.get_command("cmd1") is Command1
        assert COMMAND_REGISTRY.get_command("cmd2") is Command2
        assert COMMAND_REGISTRY.get_command("cmd3") is Command3

    def test_decorator_with_command_attributes(self):
        """Test decorator works with commands that have attributes."""
        @command(name="attr_cmd", help_text="Command with attributes")
        @dataclass
        class AttributeCommand(CommandArgsModel):
            name: str = "default"
            count: int = 0
            verbose: bool = False

            def exec(self) -> None:
                return f"{self.name} - {self.count}"

        # Verify command is registered and retains attributes
        cmd = COMMAND_REGISTRY.get_command("attr_cmd")
        assert cmd is AttributeCommand

        # Verify we can instantiate with attributes
        instance = AttributeCommand(name="test", count=5, verbose=True)
        assert instance.name == "test"
        assert instance.count == 5
        assert instance.verbose is True

    def test_decorator_preserves_inheritance(self):
        """Test that decorator preserves class inheritance."""
        @command(name="inherit_test", help_text="Inheritance test")
        @dataclass
        class InheritCommand(CommandArgsModel):
            custom_field: str = "custom"

            def exec(self) -> None:
                pass

        # Should still be instance of CommandArgsModel
        assert issubclass(InheritCommand, CommandArgsModel)

        instance = InheritCommand(custom_field="test")
        assert isinstance(instance, CommandArgsModel)
        assert isinstance(instance, InheritCommand)

    def test_decorator_with_duplicate_name_overwrites(self):
        """Test that decorating with duplicate name overwrites previous registration."""
        @command(name="duplicate", help_text="First command")
        @dataclass
        class FirstCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        @command(name="duplicate", help_text="Second command")
        @dataclass
        class SecondCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        # Should have the second command
        registered = COMMAND_REGISTRY.get_command("duplicate")
        assert registered is SecondCommand
        assert registered.command_help == "Second command"

    def test_decorator_integration_with_dataclass(self):
        """Test that @command works well with @dataclass decorator."""
        @command(name="integration", help_text="Integration test")
        @dataclass
        class IntegrationCommand(CommandArgsModel):
            field1: str = "default1"
            field2: int = 100

            def exec(self) -> None:
                return f"{self.field1}:{self.field2}"

        # Test dataclass features work
        cmd1 = IntegrationCommand()
        assert cmd1.field1 == "default1"
        assert cmd1.field2 == 100

        cmd2 = IntegrationCommand(field1="custom", field2=200)
        assert cmd2.field1 == "custom"
        assert cmd2.field2 == 200

        # Test they are different instances
        assert cmd1 is not cmd2
        assert cmd1.field1 != cmd2.field1
