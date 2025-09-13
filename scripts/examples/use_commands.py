"""
Examples of CLI commands using py-clean-cli library.

This module demonstrates how to create and structure CLI commands using the
py-clean-cli library. It includes two examples: a simple greeting command and
a more complex user management command.

Usage:
    python -m scripts.examples.use_commands hello --name "World"
    python -m scripts.examples.use_commands user create --email "test@example.com" --username "testuser" --verbose
"""

from dataclasses import dataclass
from logging import getLogger
from typing import Optional

from simple_parsing import field

from py_clean_cli import command, CommandArgsModel

# Initialize module logger
LOGGER = getLogger(__name__)


# Example 1: Simple Hello World Command
@command(name="hello", help_text="Greet someone with a personalized message")
@dataclass
class HelloCommand(CommandArgsModel):
    """
    Simple greeting command that demonstrates basic command structure.

    This example shows:
    - Basic command registration using the @command decorator
    - Simple argument handling with field() decorator
    - Basic execution logic in the exec() method
    """

    name: str = field(default="World", help="Name of the person to greet")

    greeting: str = field(
        default="Hello", help="Greeting message to use", alias=["-g", "--greet"]
    )

    uppercase: bool = field(
        default=False, help="Convert the greeting to uppercase", alias=["-u", "--upper"]
    )

    def exec(self) -> None:
        """
        Execute the hello command.

        Generates and displays a personalized greeting message based on
        the provided arguments.
        """
        message = f"{self.greeting}, {self.name}!"

        if self.uppercase:
            message = message.upper()

        if self.verbose:
            LOGGER.info(
                f"Generating greeting with parameters: name='{self.name}', greeting='{self.greeting}', uppercase={self.uppercase}"
            )

        print(message)

        if self.log_level == "DEBUG":
            LOGGER.debug("Hello command execution completed successfully")


# Example 2: User Management Command
@command(name="user", help_text="Manage user accounts with create and list operations")
@dataclass
class UserCommand(CommandArgsModel):
    """
    Complex user management command that demonstrates advanced features.

    This example shows:
    - Multiple argument types (required, optional, choices)
    - Advanced field configurations with aliases and validation
    - Logging integration with different levels
    - Error handling and validation
    """

    operation: str = field(
        help="Operation to perform on user accounts",
        metadata={"choices": ["create", "list", "delete"]},
        alias=["-o"],
    )

    email: Optional[str] = field(
        default=None,
        help="User email address (required for create operation)",
        alias=["-e"],
    )

    username: Optional[str] = field(
        default=None,
        help="Username for the account (required for create operation)",
        alias=["-uname"],
    )

    role: str = field(
        default="user",
        help="User role assignment",
        metadata={"choices": ["admin", "user", "guest"]},
        alias=["-r"],
    )

    dry_run: bool = field(
        default=False,
        help="Perform a dry run without making actual changes",
        alias=["-dr"],
    )

    def exec(self) -> None:
        """
        Execute the user management command.

        Handles different user operations based on the specified operation type.
        Includes validation, logging, and error handling.

        Raises:
            ValueError: If required arguments are missing or invalid.
        """
        if self.verbose:
            LOGGER.info(f"Executing user command with operation: {self.operation}")

        if self.operation == "create":
            self._handle_create_operation()
        elif self.operation == "list":
            self._handle_list_operation()
        elif self.operation == "delete":
            self._handle_delete_operation()
        else:
            raise ValueError(f"Unknown operation: {self.operation}")

    def _handle_create_operation(self) -> None:
        """
        Handle user creation operation.

        Validates required fields and creates a new user account.

        Raises:
            ValueError: If required fields (email, username) are missing.
        """
        LOGGER.debug("Processing user creation request")

        # Validate required fields
        if not self.email:
            raise ValueError("Email is required for user creation")
        if not self.username:
            raise ValueError("Username is required for user creation")

        if self.dry_run:
            LOGGER.info("DRY RUN: Would create user with following details:")
            print(f"  Email: {self.email}")
            print(f"  Username: {self.username}")
            print(f"  Role: {self.role}")
        else:
            LOGGER.info(
                f"Creating new user: {self.username} ({self.email}) with role: {self.role}"
            )
            # 💡 NOTE: Here you would implement actual user creation logic
            print(f"✅ User '{self.username}' created successfully!")

        if self.log_level == "DEBUG":
            LOGGER.debug("User creation operation completed")

    def _handle_list_operation(self) -> None:
        """
        Handle user listing operation.

        Displays a list of existing users (mock data for demonstration).
        """
        LOGGER.debug("Processing user listing request")

        # 💡 NOTE: Mock data for demonstration purposes
        mock_users = [
            {"username": "admin", "email": "admin@example.com", "role": "admin"},
            {"username": "john_doe", "email": "john@example.com", "role": "user"},
            {"username": "guest_user", "email": "guest@example.com", "role": "guest"},
        ]

        if self.verbose:
            LOGGER.info(f"Listing {len(mock_users)} users")

        print("📋 User List:")
        print("-" * 60)
        print(f"{'Username':<15} {'Email':<25} {'Role':<10}")
        print("-" * 60)

        for user in mock_users:
            print(f"{user['username']:<15} {user['email']:<25} {user['role']:<10}")

        if self.log_level == "DEBUG":
            LOGGER.debug("User listing operation completed")

    def _handle_delete_operation(self) -> None:
        """
        Handle user deletion operation.

        Validates username requirement and performs user deletion.

        Raises:
            ValueError: If username is not provided.
        """
        LOGGER.debug("Processing user deletion request")

        if not self.username:
            raise ValueError("Username is required for user deletion")

        if self.dry_run:
            LOGGER.info(f"DRY RUN: Would delete user: {self.username}")
            print(f"⚠️  DRY RUN: Would delete user '{self.username}'")
        else:
            LOGGER.warning(f"Deleting user: {self.username}")
            # 💡 NOTE: Here you would implement actual user deletion logic
            print(f"🗑️  User '{self.username}' deleted successfully!")

        if self.log_level == "DEBUG":
            LOGGER.debug("User deletion operation completed")


if __name__ == "__main__":
    # 💡 NOTE: This allows the module to be run directly for testing
    from py_clean_cli import package_cli

    print("🚀 Running py-clean-cli examples...")
    print("Available commands: hello, user")
    print()

    package_cli()
