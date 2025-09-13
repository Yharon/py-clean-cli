"""
Sets up a standardized .gitignore in .config folder:
    
1. Removes existing .gitignore in root (if present)
2. Creates .config directory (if needed)
3. Creates or updates .config/.gitignore
4. Configures git to use this location
"""
from pathlib import Path
from sys import path as sys_path
from dataclasses import dataclass, field
from subprocess import run as subprocess_run
from typing import Iterator, Any, Optional, Self
from textwrap import dedent
from logging import DEBUG

PROJECT_ROOT = str(Path.cwd())
if PROJECT_ROOT not in sys_path:
    sys_path.insert(0, PROJECT_ROOT)


from simple_parsing import field

from py_clean_cli import command, CommandArgsModel
from scripts import LOGGER_CLI

logging = LOGGER_CLI


GITIGNORE_TEMPLATE = dedent("""
    # environment variables
    .env
    env
    .configs/.env

    # .vscode settings
    .vscode/settings.json

    # ChromaDB local database and files
    .configs/memorys_ia_db/

    # Byte-compiled / optimized / DLL files
    __pycache__/
    *.py[cod]
    *.pyd

    # Distribution / packaging
    env/
    build/
    dist/

    # Installer logs
    logs/
    develop-eggs/
    .eggs/
    *.egg-info/
    .installed.cfg
    *.egg

    # Mock files
    docs/.mocks/

""")


@dataclass
class GitignoreSetup:
    """
    Class to setup .gitignore in .config directory
    """
    config_dir: str = field(default=".config", init=True)
    old_gitignore: str = field(default=".gitignore", init=True)
    _new_gitignore: str = field(init=False)

    def __post_init__(self):
        self._old_gitignore_path = Path(PROJECT_ROOT) / self.old_gitignore
        self._config_dir_path = Path(PROJECT_ROOT) / self.config_dir
        self._new_gitignore_path = self._config_dir_path / ".gitignore"

    def remove_old_gitignore(self):
        if self._old_gitignore_path.exists():
            LOGGER_CLI.debug(f"Removing existing {self.old_gitignore} file")
            self._old_gitignore_path.unlink()
            return f"Removed {self.old_gitignore}"
        return f"{self.old_gitignore} not found, skipping removal"

    def create_config_dir(self):
        if not self._config_dir_path.exists():
            LOGGER_CLI.debug(f"Creating directory {self._config_dir_path}")
            self._config_dir_path.mkdir(exist_ok=True)
            return f"Created directory {self._config_dir_path}"
        return f"Directory {self._config_dir_path} already exists"

    def create_or_update_gitignore(self) -> str:
        if self._new_gitignore_path.exists():
            LOGGER_CLI.debug(f"Using existing {self._new_gitignore_path}")
            return f"Using existing {self._new_gitignore_path}"
        else:
            LOGGER_CLI.debug(f"Creating new {self._new_gitignore_path}")
            with open(self._new_gitignore_path, "w") as f:
                f.write(GITIGNORE_TEMPLATE)
            return f"Created new {self._new_gitignore_path}"

    def update_git_config(self) -> str:
        LOGGER_CLI.debug("Updating git configuration to use .config/.gitignore")
        subprocess_run(["git", "config", "core.excludesFile", ".config/.gitignore"], check=True)
        return "Git is now configured to use .config/.gitignore"

    def setup_all(self):
        self.remove_old_gitignore()
        self.create_config_dir()
        self.create_or_update_gitignore()
        self.update_git_config()

    @classmethod
    def auto_execute_all_methods(cls, instance: Optional[Self] = None) -> Iterator[Any]:
        """
        Class method that automatically executes all non-private methods in a class instance.

        Args:
            instance (Self): An instance of GitignoreSetup. If None, creates a new instance.

        Yields:
            The result of each method call

        Example:
            # As a class method creating its own instance
            >>> for result in GitignoreSetup.auto_execute_all_methods():
            >>>     print(result)

            # Or with an existing instance
            >>> setup = GitignoreSetup()
            >>> for result in GitignoreSetup.auto_execute_all_methods(setup):
            >>>     print(result)
        """
        if instance is None:
            instance = cls()

        # Get all attributes that are methods
        for attr_name in dir(instance):
            # Skip special/private methods and this method itself
            if attr_name.startswith('_') or attr_name == 'auto_execute_all_methods':
                continue

            attr = getattr(instance, attr_name)
            if callable(attr) and not isinstance(attr, type):
                try:
                    result = attr()
                    yield result
                except Exception as e:
                    yield f"Error in {attr_name}: {str(e)}"


@command(name="gitignore", help_text="Setup .gitignore in .config directory")
@dataclass
class SetupGitignoreCommand(CommandArgsModel):
    """
    Command to setup .gitignore in .config directory
    """

    config_dir: str = field(
        default=".config",
        help="Directory to store the .gitignore file",
        alias=["-c"],
    )

    def exec(self) -> None:
        """
        Execute the gitignore setup command.
        """
        if self.verbose:
            LOGGER_CLI.setLevel(DEBUG)
        setup = GitignoreSetup(self.config_dir)
        for result in GitignoreSetup.auto_execute_all_methods(setup):
            LOGGER_CLI.debug(result)

        LOGGER_CLI.info("Done! Git is now configured to use .config/.gitignore")
