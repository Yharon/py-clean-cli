"""
Tests for discover_commands helper functions.

This module tests command discovery, Python file finding,
and module importing functionality.
"""

from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from py_clean_cli.helpers import COMMAND_REGISTRY
from py_clean_cli.helpers.discover_commands_helper import (
    discover_commands,
    _find_python_files,
    _import_module_from_file,
)


class TestFindPythonFiles:
    """Test suite for _find_python_files function."""

    def test_find_files_in_empty_directory(self, tmp_path):
        """Test finding Python files in an empty directory."""
        files = _find_python_files(str(tmp_path))

        assert isinstance(files, list)
        assert len(files) == 0

    def test_find_single_python_file(self, tmp_path):
        """Test finding a single Python file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test file")

        files = _find_python_files(str(tmp_path))

        assert len(files) == 1
        assert test_file in files

    def test_find_multiple_python_files(self, tmp_path):
        """Test finding multiple Python files."""
        file1 = tmp_path / "test1.py"
        file2 = tmp_path / "test2.py"
        file3 = tmp_path / "test3.py"

        file1.write_text("# Test 1")
        file2.write_text("# Test 2")
        file3.write_text("# Test 3")

        files = _find_python_files(str(tmp_path))

        assert len(files) == 3
        assert file1 in files
        assert file2 in files
        assert file3 in files

    def test_excludes_files_starting_with_underscore(self, tmp_path):
        """Test that files starting with underscore are excluded."""
        regular_file = tmp_path / "regular.py"
        init_file = tmp_path / "__init__.py"
        private_file = tmp_path / "_private.py"
        dunder_file = tmp_path / "__main__.py"

        regular_file.write_text("# Regular")
        init_file.write_text("# Init")
        private_file.write_text("# Private")
        dunder_file.write_text("# Dunder")

        files = _find_python_files(str(tmp_path))

        assert regular_file in files
        assert init_file not in files
        assert private_file not in files
        assert dunder_file not in files

    def test_finds_files_in_subdirectories(self, tmp_path):
        """Test finding Python files recursively in subdirectories."""
        subdir1 = tmp_path / "sub1"
        subdir2 = tmp_path / "sub2"
        nested = subdir1 / "nested"

        subdir1.mkdir()
        subdir2.mkdir()
        nested.mkdir(parents=True)

        file1 = tmp_path / "root.py"
        file2 = subdir1 / "sub1.py"
        file3 = subdir2 / "sub2.py"
        file4 = nested / "nested.py"

        file1.write_text("# Root")
        file2.write_text("# Sub1")
        file3.write_text("# Sub2")
        file4.write_text("# Nested")

        files = _find_python_files(str(tmp_path))

        assert len(files) == 4
        assert file1 in files
        assert file2 in files
        assert file3 in files
        assert file4 in files

    def test_ignores_non_python_files(self, tmp_path):
        """Test that non-Python files are ignored."""
        py_file = tmp_path / "test.py"
        txt_file = tmp_path / "test.txt"
        md_file = tmp_path / "readme.md"
        no_ext = tmp_path / "noextension"

        py_file.write_text("# Python")
        txt_file.write_text("Text")
        md_file.write_text("# Markdown")
        no_ext.write_text("No extension")

        files = _find_python_files(str(tmp_path))

        assert len(files) == 1
        assert py_file in files


class TestImportModuleFromFile:
    """Test suite for _import_module_from_file function."""

    def test_import_valid_module(self, tmp_path):
        """Test importing a valid Python module."""
        test_file = tmp_path / "valid_module.py"
        test_file.write_text("""
def test_function():
    return "Hello from module"
""")

        # Should not raise error
        _import_module_from_file(test_file)

    def test_import_module_with_command(self, tmp_path):
        """Test importing a module that registers a command."""
        test_file = tmp_path / "command_module.py"
        test_file.write_text("""
from dataclasses import dataclass
from py_clean_cli import command, CommandArgsModel

@command(name="imported_cmd", help_text="Imported command")
@dataclass
class ImportedCommand(CommandArgsModel):
    def exec(self) -> None:
        print("Imported command executed")
""")

        # Clear registry before import
        COMMAND_REGISTRY.clear_registry()

        _import_module_from_file(test_file)

        # Verify command was registered
        assert "imported_cmd" in COMMAND_REGISTRY._command_cache

    def test_import_module_with_syntax_error_logs_warning(self, tmp_path, caplog):
        """Test that importing module with syntax error logs warning."""
        test_file = tmp_path / "syntax_error.py"
        test_file.write_text("""
def broken_function(
    # Missing closing parenthesis
""")

        # Should not raise error, but log warning/error
        _import_module_from_file(test_file)

        # Check that error was logged
        assert any("syntax_error" in record.message.lower() for record in caplog.records)

    def test_import_module_with_import_error_tries_fallback(self, tmp_path, caplog):
        """Test that import error triggers fallback spec-based import."""
        test_file = tmp_path / "import_error.py"
        test_file.write_text("""
import non_existent_module
""")

        # Should not raise error, but log warning
        _import_module_from_file(test_file)

        # Should have logged warnings about import failure
        assert any("import" in record.message.lower() for record in caplog.records)


class TestDiscoverCommands:
    """Test suite for discover_commands function."""

    def test_discover_commands_in_directory(self, tmp_path):
        """Test discovering commands in a directory with multiple files."""
        # Create multiple command files
        file1 = tmp_path / "cmd1.py"
        file2 = tmp_path / "cmd2.py"

        file1.write_text("""
from dataclasses import dataclass
from py_clean_cli import command, CommandArgsModel

@command(name="discovered_cmd1", help_text="Discovered command 1")
@dataclass
class DiscoveredCommand1(CommandArgsModel):
    def exec(self) -> None:
        pass
""")

        file2.write_text("""
from dataclasses import dataclass
from py_clean_cli import command, CommandArgsModel

@command(name="discovered_cmd2", help_text="Discovered command 2")
@dataclass
class DiscoveredCommand2(CommandArgsModel):
    def exec(self) -> None:
        pass
""")

        # Clear registry
        COMMAND_REGISTRY.clear_registry()

        # Discover commands
        discover_commands(str(tmp_path))

        # Verify both commands were registered
        commands = COMMAND_REGISTRY.get_all_commands()
        assert len(commands) == 2
        assert COMMAND_REGISTRY.get_command("discovered_cmd1") is not None
        assert COMMAND_REGISTRY.get_command("discovered_cmd2") is not None

    def test_discover_commands_empty_directory(self, tmp_path):
        """Test discovering commands in an empty directory."""
        COMMAND_REGISTRY.clear_registry()

        # Should not raise error
        discover_commands(str(tmp_path))

        # Should have no commands
        assert len(COMMAND_REGISTRY.get_all_commands()) == 0

    def test_discover_commands_with_subdirectories(self, tmp_path):
        """Test discovering commands in nested directories."""
        subdir = tmp_path / "commands"
        subdir.mkdir()

        cmd_file = subdir / "nested_cmd.py"
        cmd_file.write_text("""
from dataclasses import dataclass
from py_clean_cli import command, CommandArgsModel

@command(name="nested_cmd", help_text="Nested command")
@dataclass
class NestedCommand(CommandArgsModel):
    def exec(self) -> None:
        pass
""")

        COMMAND_REGISTRY.clear_registry()

        discover_commands(str(tmp_path))

        # Should find nested command
        assert COMMAND_REGISTRY.get_command("nested_cmd") is not None

    def test_discover_commands_skips_underscore_files(self, tmp_path):
        """Test that discover_commands skips files starting with underscore."""
        regular = tmp_path / "regular.py"
        underscore = tmp_path / "_private.py"

        regular.write_text("""
from dataclasses import dataclass
from py_clean_cli import command, CommandArgsModel

@command(name="regular_cmd", help_text="Regular command")
@dataclass
class RegularCommand(CommandArgsModel):
    def exec(self) -> None:
        pass
""")

        underscore.write_text("""
from dataclasses import dataclass
from py_clean_cli import command, CommandArgsModel

@command(name="private_cmd", help_text="Private command")
@dataclass
class PrivateCommand(CommandArgsModel):
    def exec(self) -> None:
        pass
""")

        COMMAND_REGISTRY.clear_registry()

        discover_commands(str(tmp_path))

        # Should only find regular command
        assert COMMAND_REGISTRY.get_command("regular_cmd") is not None
        assert COMMAND_REGISTRY.get_command("private_cmd") is None

    def test_discover_commands_handles_errors_gracefully(self, tmp_path, caplog):
        """Test that discover_commands handles import errors gracefully."""
        good_file = tmp_path / "good.py"
        bad_file = tmp_path / "bad.py"

        good_file.write_text("""
from dataclasses import dataclass
from py_clean_cli import command, CommandArgsModel

@command(name="good_cmd", help_text="Good command")
@dataclass
class GoodCommand(CommandArgsModel):
    def exec(self) -> None:
        pass
""")

        bad_file.write_text("""
import non_existent_module
from py_clean_cli import command, CommandArgsModel
""")

        COMMAND_REGISTRY.clear_registry()

        # Should not raise error
        discover_commands(str(tmp_path))

        # Should have imported the good file
        assert COMMAND_REGISTRY.get_command("good_cmd") is not None
