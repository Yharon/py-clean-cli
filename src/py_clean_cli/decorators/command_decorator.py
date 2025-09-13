from py_clean_cli.helpers import COMMAND_REGISTRY


def command(name: str, help_text: str = ""):
    """
    Decorator to register a command class in the global command registry.
    """
    def decorator(cls):
        print(f"Registering command '{name}' in the decorator")
        COMMAND_REGISTRY.register(name, help_text, cls)
        return cls
    return decorator
