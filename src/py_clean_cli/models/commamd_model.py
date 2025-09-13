from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from simple_parsing import choice, field


@dataclass
class CommandArgsAbstract(ABC):
    """
    Abstract base class for command arguments.

    This class defines the common interface and default arguments
    that all command implementations should inherit from.

    Attributes:
        verbose: Enable verbose output logging.
        log_error: Enable error logging.
        log_level: Set the logging level (DEBUG or INFO).
    """

    verbose: bool = field(
        default=False,
        alias=["-v"],
        help="Enable verbose output logging."
    )
    log_error: bool = field(
        default=False,
        alias=["-le"],
        help="Enable error logging."
    )
    log_level: str = field(
        default="INFO", 
        metadata={"choices": ["DEBUG", "INFO"]}, 
        alias=["-ll"],
        help="Set the logging level (DEBUG or INFO)."
    )

    @abstractmethod
    def exec(self) -> None:
        """
        Execute the command logic.

        This method must be implemented by all subclasses to define
        the specific behavior of each command.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses must implement the `exec()` method.")


@dataclass
class CommandArgsModel(CommandArgsAbstract):
    """
    Concrete implementation of CommandArgsAbstract.

    This class provides the base structure for command implementations
    with metadata attributes for command identification.

    Class Attributes:
        command_name: The name identifier for the command.
        command_help: Help text description for the command.
    """

    command_name: ClassVar[str] = ""
    command_help: ClassVar[str] = ""
