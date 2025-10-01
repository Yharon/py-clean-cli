"""
Tests for CommandArgsModel and CommandArgsAbstract classes.

This module tests the base command model functionality including
abstract methods, default attributes, and inheritance behavior.
"""

from dataclasses import dataclass

import pytest

from py_clean_cli.models import CommandArgsModel
from py_clean_cli.models.command_model import CommandArgsAbstract


class TestCommandArgsAbstract:
    """Test suite for CommandArgsAbstract base class."""

    def test_is_abstract(self):
        """Test that CommandArgsAbstract is an abstract base class."""
        from abc import ABC

        assert issubclass(CommandArgsAbstract, ABC)

    def test_cannot_instantiate_directly(self):
        """Test that CommandArgsAbstract cannot be instantiated directly."""
        with pytest.raises(TypeError):
            # Should raise TypeError because exec() is abstract
            CommandArgsAbstract()

    def test_has_default_attributes(self):
        """Test that abstract class defines default attributes."""
        @dataclass
        class ConcreteCommand(CommandArgsAbstract):
            def exec(self) -> None:
                pass

        cmd = ConcreteCommand()

        # Check default attributes exist
        assert hasattr(cmd, "verbose")
        assert hasattr(cmd, "log_error")
        assert hasattr(cmd, "log_level")

        # Check default values
        assert cmd.verbose is False
        assert cmd.log_error is False
        assert cmd.log_level == "INFO"

    def test_default_attributes_can_be_overridden(self):
        """Test that default attributes can be overridden during instantiation."""
        @dataclass
        class ConcreteCommand(CommandArgsAbstract):
            def exec(self) -> None:
                pass

        cmd = ConcreteCommand(verbose=True, log_error=True, log_level="DEBUG")

        assert cmd.verbose is True
        assert cmd.log_error is True
        assert cmd.log_level == "DEBUG"

    def test_exec_is_abstract(self):
        """Test that exec() method is abstract."""
        @dataclass
        class IncompleteCommand(CommandArgsAbstract):
            pass  # Missing exec() implementation

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteCommand()

    def test_subclass_must_implement_exec(self):
        """Test that subclass must implement exec() method."""
        @dataclass
        class ValidCommand(CommandArgsAbstract):
            def exec(self) -> None:
                """Valid implementation."""
                print("Executing command")

        # Should not raise error
        cmd = ValidCommand()
        assert callable(cmd.exec)


class TestCommandArgsModel:
    """Test suite for CommandArgsModel class."""

    def test_inherits_from_abstract(self):
        """Test that CommandArgsModel inherits from CommandArgsAbstract."""
        assert issubclass(CommandArgsModel, CommandArgsAbstract)

    def test_has_class_variables(self):
        """Test that CommandArgsModel defines command_name and command_help."""
        assert hasattr(CommandArgsModel, "command_name")
        assert hasattr(CommandArgsModel, "command_help")

        # Check default values
        assert CommandArgsModel.command_name == ""
        assert CommandArgsModel.command_help == ""

    def test_class_variables_are_class_vars(self):
        """Test that command_name and command_help are ClassVars."""
        from typing import get_type_hints, ClassVar
        import inspect

        # ClassVar attributes are class-level only, not instance attributes
        # Verify they exist at class level
        assert hasattr(CommandArgsModel, "command_name")
        assert hasattr(CommandArgsModel, "command_help")

        # Verify instances don't get these as instance attributes
        @dataclass
        class TestCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        instance = TestCommand()
        assert "command_name" not in instance.__dict__
        assert "command_help" not in instance.__dict__

    def test_cannot_instantiate_without_exec_implementation(self):
        """Test that CommandArgsModel cannot be instantiated without exec()."""
        with pytest.raises(NotImplementedError, match="must implement the `exec\\(\\)` method"):
            cmd = CommandArgsModel()
            cmd.exec()

    def test_subclass_can_be_instantiated(self):
        """Test that a proper subclass can be instantiated."""
        @dataclass
        class MyCommand(CommandArgsModel):
            name: str = "test"

            def exec(self) -> None:
                print(f"Executing {self.name}")

        cmd = MyCommand(name="custom")
        assert cmd.name == "custom"
        assert cmd.verbose is False
        assert cmd.log_level == "INFO"

    def test_subclass_inherits_default_attributes(self):
        """Test that subclass inherits verbose, log_error, log_level."""
        @dataclass
        class InheritCommand(CommandArgsModel):
            custom_field: str = "custom"

            def exec(self) -> None:
                pass

        cmd = InheritCommand(verbose=True, log_error=True, log_level="DEBUG")

        assert cmd.verbose is True
        assert cmd.log_error is True
        assert cmd.log_level == "DEBUG"
        assert cmd.custom_field == "custom"

    def test_command_metadata_can_be_set(self):
        """Test that command_name and command_help can be set on subclass."""
        @dataclass
        class MetadataCommand(CommandArgsModel):
            def exec(self) -> None:
                pass

        MetadataCommand.command_name = "test_name"
        MetadataCommand.command_help = "test_help"

        assert MetadataCommand.command_name == "test_name"
        assert MetadataCommand.command_help == "test_help"

    def test_different_subclasses_have_independent_metadata(self):
        """Test that different subclasses can have different metadata."""
        @dataclass
        class Command1(CommandArgsModel):
            def exec(self) -> None:
                pass

        @dataclass
        class Command2(CommandArgsModel):
            def exec(self) -> None:
                pass

        Command1.command_name = "cmd1"
        Command1.command_help = "Command 1"

        Command2.command_name = "cmd2"
        Command2.command_help = "Command 2"

        assert Command1.command_name == "cmd1"
        assert Command2.command_name == "cmd2"
        assert Command1.command_help != Command2.command_help

    def test_exec_can_be_called(self):
        """Test that exec() method can be called on subclass instance."""
        executed = False

        @dataclass
        class ExecutableCommand(CommandArgsModel):
            def exec(self) -> None:
                nonlocal executed
                executed = True

        cmd = ExecutableCommand()
        cmd.exec()

        assert executed is True

    def test_exec_can_return_value(self):
        """Test that exec() can return a value (even though type hint says None)."""
        @dataclass
        class ReturnCommand(CommandArgsModel):
            value: int = 42

            def exec(self):
                return self.value * 2

        cmd = ReturnCommand(value=10)
        result = cmd.exec()

        assert result == 20

    def test_dataclass_features_work(self):
        """Test that dataclass features work with CommandArgsModel."""
        @dataclass
        class DataclassCommand(CommandArgsModel):
            name: str = "default"
            count: int = 0

            def exec(self) -> None:
                pass

        cmd1 = DataclassCommand()
        cmd2 = DataclassCommand(name="custom", count=5)

        # Test default values
        assert cmd1.name == "default"
        assert cmd1.count == 0

        # Test custom values
        assert cmd2.name == "custom"
        assert cmd2.count == 5

        # Test they are different instances
        assert cmd1 is not cmd2

    def test_kw_only_inheritance(self):
        """Test that kw_only behavior is inherited from abstract class."""
        @dataclass
        class KwOnlyCommand(CommandArgsModel):
            name: str = "test"

            def exec(self) -> None:
                pass

        # Should work with keyword arguments
        cmd = KwOnlyCommand(name="custom", verbose=True)
        assert cmd.name == "custom"
        assert cmd.verbose is True
