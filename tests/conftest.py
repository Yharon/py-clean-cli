"""
Pytest configuration and shared fixtures for py-clean-cli tests.
"""

from pathlib import Path
from sys import path as sys_path

import pytest

# Add project root to path
PROJECT_ROOT = str(Path(__file__).parent.parent)
if PROJECT_ROOT not in sys_path:
    sys_path.insert(0, PROJECT_ROOT)


@pytest.fixture(autouse=True)
def reset_registry():
    """
    Reset the command registry before each test.

    This ensures test isolation by clearing any commands registered
    in previous tests.
    """
    from py_clean_cli.helpers import COMMAND_REGISTRY

    # Store original state
    original_cache = COMMAND_REGISTRY._command_cache.copy()

    # Clear for test
    COMMAND_REGISTRY.clear_registry()

    yield

    # Restore original state
    COMMAND_REGISTRY._command_cache = original_cache


@pytest.fixture
def sample_command_class():
    """
    Fixture providing a sample command class for testing.

    Returns:
        Type[CommandArgsModel]: A basic command class for testing.
    """
    from dataclasses import dataclass
    from py_clean_cli.models import CommandArgsModel

    @dataclass
    class SampleCommand(CommandArgsModel):
        """Sample command for testing."""

        name: str = "test"

        def exec(self) -> None:
            """Execute sample command."""
            print(f"Executing sample command with name: {self.name}")

    return SampleCommand


@pytest.fixture
def temp_python_file(tmp_path):
    """
    Fixture providing a temporary Python file with a command.

    Args:
        tmp_path: pytest tmp_path fixture

    Returns:
        Path: Path to the temporary Python file.
    """
    test_file = tmp_path / "test_command.py"
    test_file.write_text('''
from dataclasses import dataclass
from py_clean_cli import command, CommandArgsModel

@command(name="temp_test", help_text="Temporary test command")
@dataclass
class TempCommand(CommandArgsModel):
    """Temporary command for testing."""

    def exec(self) -> None:
        """Execute temp command."""
        print("Temp command executed")
''')
    return test_file
